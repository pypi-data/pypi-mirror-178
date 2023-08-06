import logging
from imessage_extractor.src.chatdb.chatdb import ChatDb
from imessage_extractor.src.helpers.config import WorkflowConfig
from imessage_extractor.src.helpers.utils import listfiles
from imessage_extractor.src.helpers.verbosity import code
from os.path import splitext, basename


def create_qc_views(chatdb: 'ChatDb', cfg: WorkflowConfig, logger: logging.Logger) -> None:
    """
    Execute quality control view definitions.
    """
    view_fpaths = listfiles(cfg.dir.qc_views, ext='.sql', full_names=True)

    for view_fpath in view_fpaths:
        view_name = splitext(basename(view_fpath))[0]
        logger.debug(f'Defining view {code(view_name)}')
        sql = open(view_fpath, 'r').read()
        try:
            chatdb.execute(sql)
        except Exception as e:
            logger.debug(sql)
            raise e
        logger.debug(f'Defined view {code(view_name)}', arrow='black')


def run_quality_control(chatdb: 'ChatDb', cfg: WorkflowConfig, logger: logging.Logger) -> None:
    """
    Query each QC view and check for any data integrity issues.
    """
    vw_names = [splitext(basename(f))[0] for f in listfiles(cfg.dir.qc_views, ext='.sql')]
    total_warnings = 0

    for view_name in vw_names:
        # Validate the view was successfully defined
        if not chatdb.view_exists(view_name):
            raise Exception(f'View {code(view_name)} expected, but does not exist in SQLite')

        qc_df = chatdb.read_table(view_name)

        if len(qc_df):
            # At least one data integrity issue to report
            total_warnings += 1

            if view_name == 'qc_duplicate_chat_identifier_defs':
                logger.warning(f"""{code(view_name)}: {qc_df['chat_identifier'].nunique()} {code('chat_identifier')}
                value(s) recorded in multiple places""", arrow='yellow')

            elif view_name == 'qc_missing_contact_names':
                logger.warning(f'{code(view_name)}: unmapped {code("chat_identifier")} value(s) found', arrow='yellow')

            elif view_name == 'qc_null_flags':
                logger.warning(f"""{code(view_name)}: {len(qc_df)} records found with one
                or more flag columns set to NULL (should be either True or False)""", arrow='yellow')

            elif view_name == 'qc_duplicate_message_id':
                logger.warning(f"""{code(view_name)}: {len(qc_df)} duplicate
                {code('message_id')} values found in {code('message_user')}""", arrow='yellow')

            elif view_name == 'qc_message_special_types':
                logger.warning(f"""{code(view_name)}: {len(qc_df)} missing
                {code('message_special_type')} values found in
                {code('message_user')}""", arrow='yellow')

        else:
            logger.info(f'{code(view_name)}: OK ✓', arrow='green')

    return total_warnings