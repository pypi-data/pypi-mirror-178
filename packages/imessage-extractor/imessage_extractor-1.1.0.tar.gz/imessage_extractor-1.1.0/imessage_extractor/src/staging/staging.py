import json
import logging
import typing
from collections import OrderedDict
from imessage_extractor.src.chatdb.chatdb import ChatDb
from imessage_extractor.src.helpers.config import WorkflowConfig
from imessage_extractor.src.helpers.verbosity import path, code
from imessage_extractor.src.helpers.utils import strip_ws, ensurelist
from imessage_extractor.src.staging.python_definitions.emoji_text_map import refresh_emoji_text_map
from imessage_extractor.src.staging.python_definitions.stopwords import refresh_stopwords
from imessage_extractor.src.staging.python_definitions.message_text_parsed_from_attributedbody import refresh_message_text_parsed_from_attributedbody
from imessage_extractor.src.staging.python_definitions.message_text_edit_history import refresh_message_text_edit_history
from imessage_extractor.src.staging.python_definitions.message_text_edit_history_json import refresh_message_text_edit_history_json
from os.path import basename, join, isfile


# Add to this dictionary to include a new refresh function into the workflow,
# and therefore create the associated staging table
python_staging_table_refresh_functions = dict(
    emoji_text_map=refresh_emoji_text_map,
    stopwords=refresh_stopwords,
    message_text_parsed_from_attributedbody=refresh_message_text_parsed_from_attributedbody,
    message_text_edit_history=refresh_message_text_edit_history,
    message_text_edit_history_json=refresh_message_text_edit_history_json,
)


class StagingTableOrViewSQLDefined(object):
    """
    Store information and operations on a target SQLite iMessage user table.
    """
    def __init__(self, table_name: str, logger: logging.Logger, cfg: 'WorkflowConfig') -> None:
        self.table_name = table_name
        self.logger = logger
        self.cfg = cfg

        self.def_fpath = join(self.cfg.dir.staging_sql, self.table_name + '.sql')
        with open(self.cfg.file.staging_sql_info, 'r') as f:
            table_info = json.load(f)

        self.def_sql = self.read_def_sql(self.def_fpath)

        if self.table_name not in table_info:
            raise KeyError(f'Table "{self.table_name}" not found in "{self.cfg.file.chatdb_vw_info}"')

        self.table_info = table_info[self.table_name]

        self.dependencies = self.table_info['dependencies']
        if self.dependencies is not None and not isinstance(self.dependencies, list):
            raise ValueError(strip_ws(f"dependencies for {code(self.table_name)} must be None or a list"))

        if isinstance(self.dependencies, list) and len(self.dependencies) > 0:
            self.has_dependencies = True
        else:
            self.has_dependencies = False

        self._validate_table_definition()



    def _validate_table_definition(self) -> None:
        """
        Validate that this table has a key: value pair in *_table_info.json and a corresponding
        .sql file.
        """
        if not isfile(self.def_fpath):
            raise FileNotFoundError(strip_ws(
                f"Table definition {code(self.table_name)} expected at {path(self.def_fpath)}"))

        with open(self.cfg.file.staging_sql_info, 'r') as f:
            table_info = json.load(f)

        if self.table_name not in table_info:
            raise ValueError(strip_ws(
                f"""View definition {code(self.table_name)} expected as key: value
                pair in {path(self.cfg.file.staging_sql_info)}"""))


    def read_def_sql(self, def_fpath: str) -> str:
        """
        Read a .sql file containing a definition of a SQLite user table.
        """
        if not isfile(def_fpath):
            raise FileNotFoundError(strip_ws(
                f"View definition {code(self.table_name)} expected at {path(def_fpath)}"))

        with open(def_fpath, 'r') as sql_file:
            return sql_file.read()


    def check_dependencies(self, chatdb: 'ChatDb') -> None:
        """
        Check whether ALL dependency objects (views or tables) for a given view exist, and
        list nonexistent dependencies.
        """
        if self.has_dependencies:
            self.dependencies_exist = all([chatdb.table_or_view_exists(ref) for ref in self.dependencies])
            self.nonexistent_dependencies = [ref for ref in self.dependencies if not chatdb.table_or_view_exists(ref)]
        else:
            self.dependencies_exist = True
            self.nonexistent_dependencies = []


    def drop(self, chatdb: 'ChatDb', if_exists: bool=False, cascade: bool=False) -> None:
        """
        Drop the target view.
        """
        if not hasattr(self, 'dependencies_exist'):
            self.check_dependencies(chatdb)

        if if_exists:
            if chatdb.view_exists(self.table_name):
                chatdb.drop_view(self.table_name, cascade=cascade)
                self.logger.info(f'Dropped view "{code(self.table_name)}" (cascade {code(cascade)}) ', arrow='red')
        else:
            chatdb.drop_view(self.table_name, cascade=cascade)
            self.logger.info(f'Dropped view "{code(self.table_name)}" (cascade {code(cascade)}) ', arrow='red')


    def create(self, chatdb: 'ChatDb', cascade: bool=False) -> None:
        """
        Define a view/table with or without cascade. Views may be dependent on other views or tables,
        and as such, as we cannot simply execute a view definition since a dependency of that
        view might not exist yet. Instead, we will define views in a manner that ensures
        that all dependencies for a particular view are created before executing that view's
        definition.

        We will iterate through each view in the *view_info.json file, and for each view,
        check each of its dependencies (if any) to ensure that they exist. If one or more
        do not, we must navigate to that view in the *view_info.json file and ensure that
        all of that view's dependencies exist. If one or more do not yet exist, we must then
        continue navigating down the tree of dependencies until we can create all of them.

        For example, suppose view A depends on view B and view C, and view B depends on view D.
        We will attempt to create view A, but it depends on two non-existent views, B and C. We
        then navigate to view B and find that it depends on view D. We create view D for which
        all dependencies exist. Then we can create view B. We then check view C, and find that
        we are able to create it without issue. At this point, all dependencies for view A
        exist and we can create view A.
        """
        def get_dependency_type(ref_name: str) -> str:
            """
            Read config files to determine whether the given dependency is a
            SQL staging table/view, or a Python staging table.
            """
            if ref_name in staging_sql_info:
                return 'staging_sql'
            elif ref_name in staging_python_info:
                return 'staging_python'
            else:
                raise ValueError(f'Dependency {code(ref_name)} not found in either {path(self.cfg.file.staging_sql_info)} or {path(self.cfg.file.staging_python_info)}')


        with open(self.cfg.file.staging_sql_info, 'r') as f:
            staging_sql_info = json.load(f)

        with open(self.cfg.file.staging_python_info, 'r') as f:
            staging_python_info = json.load(f)

        if not cascade:
            self.logger.debug(f'Cascaded create not required, creating the staging object {code(self.table_name)}', arrow='black')
            chatdb.execute(self.def_sql)
            self.logger.info(f'Created staging object {code(self.table_name)}', arrow='black')
        else:
            self.logger.debug(f'Requested cascaded definition for {code(self.table_name)}', arrow='black')
            if chatdb.table_or_view_exists(self.table_name):
                self.logger.debug('User table already exists', arrow='black')
            else:
                if not hasattr(self, 'dependencies_exist'):
                    self.check_dependencies(chatdb)

                if self.dependencies_exist:
                    self.logger.debug(f'All dependencies exist, creating the staging object {code(self.table_name)}', arrow='black')
                    chatdb.execute(self.def_sql)
                    self.logger.info(f'Created staging object {code(self.table_name)}', arrow='black')
                else:
                    self.logger.debug(strip_ws(
                        f"""Cannot create the user table because of nonexistent
                        dependencies: {', '.join([code(x) for x in self.nonexistent_dependencies])}"""), arrow='black')

                    for ref in self.nonexistent_dependencies:
                        ref_type = get_dependency_type(ref)

                        if ref_type == 'staging_sql':
                            ref_table_obj = StagingTableOrViewSQLDefined(table_name=ref,
                                                                         logger=self.logger,
                                                                         cfg=self.cfg)
                            ref_table_obj.create(chatdb=chatdb, cascade=True)

                        elif ref_type == 'staging_python':
                            staging_python_obj = StagingTablePythonDefined(
                                table_name=ref,
                                chatdb=chatdb,
                                logger=chatdb.logger,
                                cfg=self.cfg
                            )
                            staging_python_obj.refresh()

                    # At this point, we have created all of the refrences for this view,
                    # so we should be able to simply create it as normal
                    chatdb.execute(self.def_sql)
                    self.logger.info(f'Created staging object {code(self.table_name)}', arrow='black')


class StagingTablePythonDefined(object):
    """
    Store information and operations for tables that get staged after chat.db
    data has been loaded into SQLite.
    """
    def __init__(self,
                 table_name: str,
                 chatdb: 'ChatDb',
                 logger: logging.Logger,
                 cfg: 'WorkflowConfig'
                 ) -> None:
        self.chatdb = chatdb
        self.table_name = table_name
        self.refresh_function = python_staging_table_refresh_functions[self.table_name]
        self.logger = logger
        self.cfg = cfg

        self.logger.debug(f'Initializing table metadata {code(self.table_name)}', arrow='black')

        with open(self.cfg.file.staging_python_info) as f:
            json_data = json.load(f)
            if self.table_name in json_data.keys():
                json_data = json_data[self.table_name]
            else:
                raise KeyError(strip_ws(
                    f"""Table {table_name} expected as a key in
                    {basename(self.cfg.file.staging_python_info)} but not found"""))

        self.columnspec = json_data['columnspec']
        self.primary_key = json_data['primary_key']
        self.dependency = json_data['dependencies']
        self.check_dependencies(self.dependency)

        assert isinstance(self.columnspec, dict), \
            f'Columnspec for {self.table_name} must be a dictionary'
        assert self.primary_key is None or isinstance(self.primary_key, str) or isinstance(self.primary_key, list), \
            f'Primary key for {self.table_name} must be None or a string or a list'
        assert self.dependency is None or isinstance(self.dependency, list), \
            f'dependencies for {self.table_name} must be None or a list'


    def check_dependencies(self, dependency) -> None:
        """
        Return True if all dependency objects exist in SQLite schema, and return
        an error otherwise.
        """
        if isinstance(dependency, list):
            missing_refs = []
            for ref in dependency:
                if not self.chatdb.table_or_view_exists(ref):
                    missing_refs.append(ref)

            if len(missing_refs) > 0:
                raise Exception(strip_ws(
                    f"""Staging table {code(self.table_name)} requires the
                    following non-existent dependencies: {', '.join([code(x) for x in missing_refs])}"""))


    def refresh(self, check_if_exists=False) -> None:
        """
        Execute custom refresh function for a particular table. Refresh functions are
        stored as python modules and live in relative directory refresh_functions/
        """
        if check_if_exists:
            if not self.chatdb.table_or_view_exists(self.table_name):
                self.refresh_function(chatdb=self.chatdb,
                                      table_name=self.table_name,
                                      columnspec=self.columnspec,
                                      logger=self.logger)
        else:
            self.refresh_function(chatdb=self.chatdb,
                                  table_name=self.table_name,
                                  columnspec=self.columnspec,
                                  logger=self.logger)


def stage_objects(chatdb: 'ChatDb', cfg: 'WorkflowConfig', logger: logging.Logger) -> OrderedDict:
    """
    Return a dictionary of staging tables and/or views in the order that they should be created.
    """
    def get_staging_object_status() -> dict:
        """
        Return a dictionary of all staging tables and views with a list of their dependencies,
        and an indicator as to whether each dependency exists.

        {
            'staging_table_name': {
                'staging_type': 'staging_sql' or 'staging_python',
                'dependencies': {
                    'dependency_name1': True,
                    'dependency_name2': False,
                    ...
                }
            }
        }
        """
        staging_object_dependencies = dict()

        with open(cfg.file.staging_sql_info) as f:
            x = json.load(f)
            for obj_name, obj_info in x.items():
                dependencies_exist_map = {r: chatdb.table_or_view_exists(r) for r in ensurelist(obj_info['dependencies']) if r is not None}
                staging_object_dependencies[obj_name] = dict(staging_type='staging_sql', dependencies=dependencies_exist_map)

        with open(cfg.file.staging_python_info) as f:
            x = json.load(f)
            for obj_name, obj_info in x.items():
                dependencies_exist_map = {r: chatdb.table_or_view_exists(r) for r in ensurelist(obj_info['dependencies']) if r is not None}
                staging_object_dependencies[obj_name] = dict(staging_type='staging_python', dependencies=dependencies_exist_map)

        return staging_object_dependencies


    def read_staging_info(cfg: 'WorkflowConfig') -> dict:
        """
        Read Python and SQL staging table JSON config info and return as dictionary.
        """
        staging_info = {}

        with open(cfg.file.staging_sql_info, 'r') as f:
            x = json.load(f)
            for name, info in x.items():
                info['staging_type'] = 'sql'
                staging_info[name] = info

        with open(cfg.file.staging_python_info, 'r') as f:
            x = json.load(f)
            for name, info in x.items():
                info['staging_type'] = 'python'
                staging_info[name] = info

        return staging_info


    def format_dependencies_for_topological_sort(staging_info: dict) -> list:
        """
        Read staging SQL and Python info configuration JSON files and return a list in
        the following format to be fed into `topological_sort()`:

        {
            'name': [list of dependencies],
            ...
        }
        """
        dependencies_dct = {}
        for name, info in staging_info.items():
            deps = info['dependencies']
            if deps is None:
                dependencies_dct[name] = []
            else:
                dependencies_dct[name] = deps

        return dependencies_dct


    import networkx as nx
    logger.debug('Building staging order', arrow='black')
    staging_info = read_staging_info(cfg)
    dependencies_dct = format_dependencies_for_topological_sort(staging_info)
    staging_order = list(reversed(list(nx.topological_sort(nx.DiGraph(dependencies_dct)))))
    logger.debug(f"Staging order: {' → '.join([code(x) for x in staging_order])}", arrow='black')


    for name in staging_order:
        staging_type = staging_info[name]['staging_type']
        if staging_type == 'sql':
            logger.debug(f'Creating SQL staging object {code(name)}', arrow='black')
            staging_sql_obj = StagingTableOrViewSQLDefined(
                table_name=name,
                logger=chatdb.logger,
                cfg=cfg
            )
            staging_sql_obj.create(chatdb=chatdb, cascade=False)
        elif staging_type == 'python':
            logger.debug(f'Creating Python staging object {code(name)}', arrow='black')
            staging_python_obj = StagingTablePythonDefined(
                table_name=name,
                chatdb=chatdb,
                logger=chatdb.logger,
                cfg=cfg
            )
            staging_python_obj.refresh(check_if_exists=False)
        else:
            raise ValueError(f"Invalid `staging_type` for name '{name}', must be one of 'sql' or 'python")


    # for obj_name, obj_info in staging_object_dependencies.items():
    #     if obj_info['staging_type'] == 'staging_sql':
    #         staging_sql_obj = StagingTableOrViewSQLDefined(
    #             table_name=obj_name,
    #             logger=chatdb.logger,
    #             cfg=cfg
    #         )
    #         staging_sql_obj.create(chatdb=chatdb, cascade=True)

    #     elif obj_info['staging_type'] == 'staging_python':
    #         staging_python_obj = StagingTablePythonDefined(
    #             table_name=obj_name,
    #             chatdb=chatdb,
    #             logger=chatdb.logger,
    #             cfg=cfg
    #         )
    #         staging_python_obj.refresh(check_if_exists=True)
