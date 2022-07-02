from django.db import connection
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core import management


def delete_tables(recreate = False):
    dbinfo = settings.DATABASES['default']
    dbname = dbinfo['NAME']
    cursor = connection.cursor()
    find_tables_query = "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema' AND tableowner = '{}';".format(dbinfo['NAME'])
    print("find_tables_query", find_tables_query)
    cursor.execute(find_tables_query)
    parts = ('DROP TABLE IF EXISTS %s CASCADE;' % table for (table,) in cursor.fetchall())
    sql = "SET session_replication_role = 'replica';\n" + '\n'.join(parts) + "SET session_replication_role = 'origin';\n"
    print("ready to run ", sql)
    connection.cursor().execute(sql)
    if recreate:
        print("ready to run migrate to restore")
        management.call_command("migrate")
    exit()



class Command(BaseCommand):
    help = 'deletes all table and optionally recreates them'

    def add_arguments(self, parser):
        parser.add_argument('--recreate', action="store_true", help="to recreate all tables",)

    def handle(self, *args, **options):
        delete_tables(options['recreate'])