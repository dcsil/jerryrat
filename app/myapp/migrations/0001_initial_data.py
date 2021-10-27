# http://flecox.github.io/django/2015/05/28/django-execute-sql-file-inside-a-migration-step.html
import os

from django.db import connection, migrations

def load_data_from_sql(filename):
    file_path = os.path.join(os.path.dirname(__file__), '../sql/', filename)
    sql_statement = open(file_path).read()
    with connection.cursor() as c:
        c.execute(sql_statement)

initial_data = lambda apps, schema_editor: load_data_from_sql('initDataBase.sql')


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL("USE jerryratdb;"),
        migrations.RunPython(initial_data),
    ]