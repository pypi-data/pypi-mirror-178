import logging
import pandas as pd
import json
from imessage_extractor.src.chatdb.chatdb import ChatDb
from imessage_extractor.src.helpers.verbosity import code
from imessage_extractor.src.staging.common import columns_match_expectation


def refresh_message_text_edit_history_json(chatdb: 'ChatDb',
                                           table_name: str,
                                           columnspec: dict,
                                           logger: logging.Logger) -> None:
    """
    With the introduction of macOS Ventura, the message edit history is stored
    as a binary plist in the `message_summary_info` blob column. The staging
    table `message_text_edit_history` is responsible for storing the parsed
    edit history.

    This table is responsible for transforming that table into a one-row-per-message
    table with an `edit_history` column as a JSON-formatted edit history.

    {
        0: {
            "text": "...".
            "ts_edited": "..."
        },
        ...
    }
    """
    logger.info(f'Refreshing table {code(table_name)}', arrow='black')

    df_edit_history = pd.read_sql('select * from message_text_edit_history', chatdb.sqlite_con)
    df_json = pd.DataFrame({k: pd.Series(dtype=v) for k, v in columnspec.items()})

    unique_message_ids = df_edit_history['message_id'].unique().tolist()

    for message_id in unique_message_ids:
        rows = df_edit_history.loc[df_edit_history['message_id'] == message_id].reset_index(drop=True)
        edit_history = {}
        for i, row in rows.iterrows():
            edit_history_dct = dict(text=row['text'], ts_edited=row['ts_edited'])
            edit_history[i] = edit_history_dct

        df_json.loc[len(df_json)] = [message_id, json.dumps(edit_history)]

    columns_match_expectation(df_json, table_name, columnspec)
    df_json.to_sql(name=table_name,
                   con=chatdb.sqlite_con,
                   schema='main',
                   index=False,
                   if_exists='replace')

    logger.debug(f'Built table {code(table_name)}', arrow='black')
