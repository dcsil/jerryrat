# Generated by Django 3.2.8 on 2021-12-01 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CampaignComboContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('docfile', models.FileField(blank=True, default='', null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Linechart',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('xaxis', models.CharField(choices=[('age', 'age'), ('month', 'month'), ('day_of_week', 'day_of_week'), ('duration', 'duration'), ('campaign', 'campaign'), ('pdays', 'pdays'), ('previous', 'previous')], default='age', max_length=32)),
                ('yaxis', models.CharField(choices=[('age', 'age'), ('month', 'month'), ('day_of_week', 'day_of_week'), ('duration', 'duration'), ('campaign', 'campaign'), ('pdays', 'pdays'), ('previous', 'previous')], default='age', max_length=32)),
                ('title', models.CharField(max_length=64)),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='PredictionModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=32)),
                ('email', models.EmailField(max_length=32)),
                ('pwd', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Userdata',
            fields=[
                ('dataid', models.AutoField(primary_key=True, serialize=False)),
                ('age', models.IntegerField()),
                ('job', models.CharField(max_length=255)),
                ('marital', models.CharField(max_length=255)),
                ('education', models.CharField(max_length=255)),
                ('default', models.CharField(max_length=10)),
                ('housing', models.CharField(max_length=10)),
                ('loan', models.CharField(max_length=10)),
                ('contact', models.CharField(max_length=255)),
                ('month', models.CharField(max_length=5)),
                ('day_of_week', models.CharField(max_length=5)),
                ('duration', models.IntegerField()),
                ('campaign', models.IntegerField()),
                ('pdays', models.IntegerField()),
                ('previous', models.IntegerField()),
                ('poutcome', models.CharField(max_length=255)),
                ('emp_var_rate', models.DecimalField(db_column='emp.var.rate', decimal_places=1, max_digits=4)),
                ('cons_price_idx', models.DecimalField(db_column='cons.price.idx', decimal_places=3, max_digits=5)),
                ('cons_conf_idx', models.DecimalField(db_column='cons.conf.idx', decimal_places=1, max_digits=3)),
                ('euribor3m', models.DecimalField(decimal_places=3, max_digits=4)),
                ('nr_employed', models.DecimalField(db_column='nr.employed', decimal_places=1, max_digits=5)),
                ('y', models.CharField(blank=True, max_length=5, null=True)),
            ],
            options={
                'db_table': 'userdata',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Userinfo',
            fields=[
                ('dataid', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('numbers', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'userinfo',
                'managed': True,
            },
        ),
    ]
