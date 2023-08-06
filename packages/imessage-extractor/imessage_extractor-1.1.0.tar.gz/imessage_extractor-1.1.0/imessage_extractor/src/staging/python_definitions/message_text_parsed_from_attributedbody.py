import logging
import pandas as pd
import subprocess
from imessage_extractor.src.chatdb.chatdb import ChatDb
from imessage_extractor.src.helpers.verbosity import code
from imessage_extractor.src.staging.common import columns_match_expectation
from os import mkdir, listdir, chdir
from os.path import expanduser, isdir, join, splitext, basename
from shutil import rmtree


def extract_message_text_from_decoded_attributedbody(bytes_str: bytes) -> str:

    def write_tempfile(bytes_str: bytes) -> str:
        tmp_attributedbody_filepath = expanduser('~/tmp_attributedbody')
        with open(tmp_attributedbody_filepath, 'w+b') as f:
            f.write(bytes_str)

        return tmp_attributedbody_filepath


    def decode_tempfile(filepath: str) -> str:
        p = subprocess.run(f'pytypedstream decode "{filepath}"', shell=True, stdout=subprocess.PIPE)
        result = p.stdout.decode()
        return result


    def extract_message_text(result: str):
        if 'NSMutableString' in result:
            search_attribute = 'NSMutableString'
        else:
            search_attribute = 'NSString'

        search_prefix = "\ttype b\'@\': "
        search_suffix = '('
        search_phrase = search_prefix + search_attribute + search_suffix

        ns_mutable_string_lst = [x for x in result.split('\n') if x.startswith(search_phrase)]
        if len(ns_mutable_string_lst) != 1:
            raise Exception('No valid "NSMutableString" or "NSString" found')

        ns_mutable_string = ns_mutable_string_lst[0]
        message_text = ns_mutable_string.replace(search_phrase, '')[1:-2]  # 1: is to remove leading " or ', :-2 is to remove trailing ") or ')
        return message_text

    if bytes_str is not None:
        tempfile = write_tempfile(bytes_str)
        decoded_result = decode_tempfile(tempfile)
        message_text = extract_message_text(decoded_result)
        return message_text
    else:
        return None


def refresh_message_text_parsed_from_attributedbody(
    chatdb: 'ChatDb',
    table_name: str,
    columnspec: dict,
    logger: logging.Logger) -> None:
    """
    With the introduction of macOS Ventura, it became possible that the `text`
    field in the `message` table is NULL, and instead the message text is embedded
    within the `attributedBody`.

    This function is responsible for the following:
        1. Connect to the copied chat.db
        2. Read all rows of the `message` table where there is no next, and the
            `attributedBody` field is populated
        3. Parse the message text from the `attributedBody` using pytypedstream
        4. Write the parsed message text to a new table
            `message_text_parsed_from_attributedbody` with columns (message_id,
            text, is_text_parsed_from_attributedbody=True)
    """
    logger.info(f'Refreshing table {code(table_name)}', arrow='black')

    df_attributedbody = pd.read_sql("""
    select ROWID, attributedBody
    from message
    where text is null
      and attributedBody is not null
    order by ROWID desc""", chatdb.sqlite_con)

    # TODO: add pytypedstream() function from common



    tmp_attributedbody_dirpath = expanduser('~/tmp_imessage_extractor_attributedbody')
    if not isdir(tmp_attributedbody_dirpath):
        mkdir(tmp_attributedbody_dirpath)

    chdir(tmp_attributedbody_dirpath)

    for i, row in df_attributedbody.iterrows():
        rowid = row['ROWID']
        attributedbody_bytes = row['attributedBody']
        filepath = join(tmp_attributedbody_dirpath, f'attributedBody_{rowid}.bin')
        with open(filepath, 'wb+') as f:
            f.write(attributedbody_bytes)

    df_parsed = pd.DataFrame({k: pd.Series(dtype=v) for k, v in columnspec.items()})

    written_attributedbody_filepaths = [x for x in listdir() if 'attributedBody' in x and splitext(x)[1] == '.bin']
    for filepath in written_attributedbody_filepaths:
        with open(filepath, 'rb') as f:
            bytes_str = f.read()

        rowid = splitext(basename(filepath))[0].replace('attributedBody_', '')
        rowid = int(rowid)
        text = extract_message_text_from_decoded_attributedbody(bytes_str)
        text = None if text == '' else text
        df_parsed.loc[len(df_parsed)] = [rowid, text, 1]

    columns_match_expectation(df_parsed, table_name, columnspec)
    df_parsed.to_sql(name=table_name,
                     con=chatdb.sqlite_con,
                     schema='main',
                     index=False,
                     if_exists='replace')

    if isdir(tmp_attributedbody_dirpath):
        rmtree(tmp_attributedbody_dirpath)

    logger.debug(f'Built table {code(table_name)}', arrow='black')
