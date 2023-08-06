import logging
import pandas as pd
import plistlib
from imessage_extractor.src.chatdb.chatdb import ChatDb
from imessage_extractor.src.helpers.verbosity import code
from imessage_extractor.src.staging.common import columns_match_expectation
from datetime import datetime
from imessage_extractor.src.staging.common import pytypedstream, parse_type_from_typedstream, chatdb_format_date_to_epoch_seconds


def refresh_message_text_edit_history(chatdb: 'ChatDb',
                                      table_name: str,
                                      columnspec: dict,
                                      logger: logging.Logger) -> None:
    """
    With the introduction of macOS Ventura, the message edit history is stored
    as a binary plist in the `message_summary_info` blob column. Parse the edit
    history per message from this column.
    """
    logger.info(f'Refreshing table {code(table_name)}', arrow='black')

    df_message_summary_info = pd.read_sql("""
    select ROWID, message_summary_info
    from message
    where date_edited > 0
      and message_summary_info is not null
    order by ROWID desc""", chatdb.sqlite_con)

    df_parsed = pd.DataFrame({k: pd.Series(dtype=v) for k, v in columnspec.items()})

    for i, row in df_message_summary_info.iterrows():
        rowid = row['ROWID']
        message_summary_info_bytes = row['message_summary_info']
        plist = plistlib.loads(message_summary_info_bytes)

        if 'ec' in plist.keys():
            plist_items = plist['ec']['0']
            for i, item in enumerate(plist_items):
                ts_edited = item['d']*1000000000
                ts_edited = chatdb_format_date_to_epoch_seconds(ts_edited)
                ts_edited = datetime.fromtimestamp(ts_edited)
                text_bin = item['t']
                text_typestream = pytypedstream(text_bin)
                ns_string_lst = parse_type_from_typedstream(text_typestream, 'NSString')
                if len(ns_string_lst) != 1:
                    raise Exception(f'Error parsing NSString from message_summary_info for message ID {rowid}')
                else:
                    message_text = ns_string_lst[0]

                df_parsed.loc[len(df_parsed)] = [rowid, message_text, ts_edited]

    columns_match_expectation(df_parsed, table_name, columnspec)
    (
        df_parsed
        .sort_values(['message_id', 'ts_edited'])
        .to_sql(name=table_name,
                con=chatdb.sqlite_con,
                schema='main',
                index=False,
                if_exists='replace')
    )

    logger.debug(f'Built table {code(table_name)}', arrow='black')
