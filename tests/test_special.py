import uuid
import pytest
from mssqltestutils import create_mssql_cli_client, create_mssql_cli_options, \
                           create_test_db, shutdown, clean_up_test_db
from mssqlcli.packages.special.main import special_command, execute, NO_QUERY


# All tests require a live connection to a SQL Server database
class TestSpecialCommands:
    session_guid = str(uuid.uuid4().hex)
    table1 = 'mssql_cli_table1_{0}'.format(session_guid)
    table2 = 'mssql_cli_table2_{0}'.format(session_guid)
    view = 'mssql_cli_view_{0}'.format(session_guid)
    database = 'mssql_cli_db_{0}'.format(session_guid)
    schema = 'mssql_cli_schema_{0}'.format(session_guid)
    index = 'mssql_cli_index_{0}'.format(session_guid)
    function = 'mssql_cli_func_{0}'.format(session_guid)
    login = 'mssql_cli_login_{0}'.format(session_guid)

    @classmethod
    @pytest.fixture(scope='class')
    def client(cls):
        """
        Pytest fixture which creates client and runs commands, and tears down on completion
        """
        # create the database objects to test upon
        test_db = create_test_db()

        # create options with db name
        options = create_mssql_cli_options()
        options.database = test_db

        client = create_mssql_cli_client(options)
        list(client.execute_query('CREATE DATABASE {0};'.format(cls.database)))
        list(client.execute_query('CREATE TABLE {0} (a int, b varchar(25));'
                                  .format(cls.table1)))
        list(client.execute_query('CREATE TABLE {0} (x int, y varchar(25), z bit);'
                                  .format(cls.table2)))
        list(client.execute_query('CREATE VIEW {0} as SELECT a from {1};'
                                  .format(cls.view, cls.table1)))
        list(client.execute_query('CREATE SCHEMA {0};'.format(cls.schema)))
        list(client.execute_query('CREATE INDEX {0} ON {1} (x);'.format(cls.index, cls.table2)))
        list(client.execute_query('CREATE FUNCTION {0}() '\
                                  'RETURNS TABLE AS RETURN (select 1 as number);'
                                  .format(cls.function)))
        list(client.execute_query('CREATE LOGIN {0} WITH PASSWORD=\'yoloC123445!\''
                                  .format(cls.login)))
        yield client

        # delete the database objects created
        client = create_mssql_cli_client()
        try:
            list(client.execute_query('DROP DATABASE {0};'.format(cls.database)))
            list(client.execute_query('DROP INDEX {0} ON {1};'.format(cls.index, cls.table2)))
            list(client.execute_query('DROP TABLE {0};'.format(cls.table1)))
            list(client.execute_query('DROP TABLE {0};'.format(cls.table2)))
            list(client.execute_query('DROP VIEW {0};'.format(cls.view)))
            list(client.execute_query('DROP SCHEMA {0};'.format(cls.schema)))
            list(client.execute_query('DROP FUNCTION {0}'.format(cls.function)))
            list(client.execute_query('DROP LOGIN {0}'.format(cls.login)))
        finally:
            shutdown(client)
            clean_up_test_db(test_db)

    def test_list_tables_command(self, client):
        self.command(client, '\\lt', self.table1, min_rows_expected=2,
                     rows_expected_pattern_query=1, cols_expected=2, cols_expected_verbose=4)

    def test_list_views_command(self, client):
        self.command(client, '\\lv', self.view, min_rows_expected=1,
                     rows_expected_pattern_query=1, cols_expected=2, cols_expected_verbose=3)

    def test_list_schemas_command(self, client):
        self.command(client, '\\ls', self.schema, min_rows_expected=1,
                     rows_expected_pattern_query=1, cols_expected=1, cols_expected_verbose=3)

    def test_list_indices_command(self, client):
        self.command(client, '\\li', self.index, min_rows_expected=1,
                     rows_expected_pattern_query=1, cols_expected=3, cols_expected_verbose=5)

    @pytest.mark.skip(reason="Disabling since this test assumes a single database exists, "
                             "which doesn't work for any shared database.")
    def test_list_databases_command(self, client):
        self.command(client, '\\ld', self.database, min_rows_expected=1,
                     rows_expected_pattern_query=1, cols_expected=1, cols_expected_verbose=4)

    @pytest.mark.skip(reason="Disabling since this test is broken on Azure which returns "
                             "more logins than expected.")
    def test_list_logins_command(self, client):
        self.command(client, '\\ll', self.login, min_rows_expected=1,
                     rows_expected_pattern_query=1, cols_expected=2, cols_expected_verbose=5)

    def test_list_functions_command(self, client):
        self.command(client, '\\lf', self.function, min_rows_expected=1,
                     rows_expected_pattern_query=1, cols_expected=1, cols_expected_verbose=2)

    def test_show_function_definition_command(self, client):
        for rows, col, _, _, _ in client.execute_query('\\sf {0}'.format(self.function)):
            assert len(rows) == 1
            assert len(col) == 1

    def test_describe_object_command(self, client):
        result_set_count = 0
        for _ in client.execute_query('\\d {0}'.format(self.function)):
            result_set_count += 1

        assert result_set_count == 2

    @staticmethod
    def test_named_queries_commands(client):
        # Save named queries
        list(client.execute_query('\\sn test123 select 1'))
        list(client.execute_query('\\sn test234 select 2'))

        # List named queries
        for rows, col, _, _, _ in client.execute_query('\\n'):
            assert len(rows) >= 2
            num_queries = len(rows)

        # Execute named query created above
        for rows, col, _, _, _ in client.execute_query('\\n test123'):
            assert len(rows) == 1
            assert len(col) == 1

        # Delete a named query that was created
        list(client.execute_query('\\dn test123'))

        # Number of named queries should have reduced by 1
        for rows, col, _, _, _ in client.execute_query('\\n'):
            assert num_queries-1 == len(rows)

        # Clean up the second named query created
        list(client.execute_query('\\dn test234'))

    @staticmethod
    def test_add_new_special_command():
        @special_command('\\empty', '\\empty[+]', 'returns an empty list', arg_type=NO_QUERY)
        def empty_list_special_command():
            # pylint: disable=unused-variable
            return []

        ret = execute(None, '\\empty')
        assert len(ret) == 0

    @staticmethod
    def command(client, command, pattern, min_rows_expected, rows_expected_pattern_query,
                cols_expected, cols_expected_verbose):
        # pylint: disable=too-many-arguments

        for rows, col, _, _, _ in client.execute_query(command):
            assert len(rows) >= min_rows_expected
            assert len(col) == cols_expected

        # execute with pattern and verbose
        command = command + "+ " + pattern
        for rows, col, _, _, _ in client.execute_query(command):
            assert len(rows) == rows_expected_pattern_query
            assert len(col) == cols_expected_verbose
