import pandas as pd
import tempfile
import subprocess
from imessage_extractor.src.helpers.verbosity import bold
from imessage_extractor.src.helpers.utils import strip_ws


def columns_match_expectation(df: pd.DataFrame, table_name: str, columnspec: dict) -> bool:
    """
    Make sure that there is alignment between the columns specified in staging_table_info.json
    and the actual columns in the dataframe about to be inserted.
    """
    expected_columns = sorted([k for k, v in columnspec.items()])
    actual_columns = df.columns

    for col in expected_columns:
        if col not in actual_columns:
            raise KeyError(strip_ws(
                f"""Column {bold(col)} defined in staging_table_info.json
                for table {bold(table_name)} but not in actual dataframe columns
                ({bold(str(df.columns))})"""))

    for col in actual_columns:
        if col not in actual_columns:
            raise KeyError(strip_ws(
                f"""Column {bold(col)} in actual dataframe {bold(table_name)}
                columns ({bold(str(df.columns))}) but not in staging_table_info.json"""))


def pytypedstream(bytes_str: bytes) -> str:
    """
    Execute `pytypedstream decode ...` on a string of bytes.
    """
    file = tempfile.NamedTemporaryFile(mode='w+b')
    file.write(bytes_str)
    file.seek(0)
    p = subprocess.run(f'pytypedstream decode "{file.name}"', shell=True, stdout=subprocess.PIPE)
    result = p.stdout.decode()
    file.close()
    return result


def parse_type_from_typedstream(typedstream_str: str, ns_type: str) -> list:
    """
    Get the text wrapped in: type b'@': {ns_type}('get this text').

    Example with ns_type='NSString': type b'@': NSString('test text') -> return 'test text'
    """
    typedstream_lst = [x.strip() for x in typedstream_str.split('\n')]
    prefix = "type b'@': "
    suffix = '('
    search_for = prefix + ns_type + suffix
    match_lst = [x for x in typedstream_lst if x.startswith(search_for)]
    return [x.replace(search_for, '')[1:-2] for x in match_lst]  # 1: is to remove leading " or ', :-2 is to remove trailing ") or ')


def chatdb_format_date_to_epoch_seconds(x: int) -> float:
    """
    Format a date value formatted the way chat.db stores dates as an epoch seconds float.

    Example: x=691125786311000064 -> return=1669432986.311
    """
    assert len(str(int(x))) == 18, f"Input date '{str(x)}' is not in the proper, 18-digit format found in date columns in chat.db"
    return int(x) / 1000000000 + 978307200
