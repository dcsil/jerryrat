from django.db import models


class Document(models.Model):
    id = models.AutoField(primary_key=True)
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')


class User(models.Model):
    user = models.CharField(max_length=32)
    email = models.EmailField(max_length=32)
    pwd = models.CharField(max_length=32)


class CampaignComboContent(models.Model):
    title = models.TextField()
    description = models.TextField()


class PredictionModel(models.Model):
    model_name = None
    description = None

    def __init__(self, name):
        self.model_name = name

    def add_description(self, description):
        self.description = description


# ORM for user data model
# feed ML model data to learn
# add to add a pyspark channel for feeding
class Userdata(models.Model):
    dataid = models.AutoField(primary_key=True)
    age = models.IntegerField()
    job = models.CharField(max_length=255)
    marital = models.CharField(max_length=255)
    education = models.CharField(max_length=255)
    default = models.CharField(max_length=10)
    housing = models.CharField(max_length=10)
    loan = models.CharField(max_length=10)
    contact = models.CharField(max_length=255)
    month = models.CharField(max_length=5)
    day_of_week = models.CharField(max_length=5)
    duration = models.IntegerField()
    campaign = models.IntegerField()
    pdays = models.IntegerField()
    previous = models.IntegerField()
    poutcome = models.CharField(max_length=255)
    emp_var_rate = models.DecimalField(db_column='emp.var.rate', max_digits=4,
                                       decimal_places=1)  # Field renamed to remove unsuitable characters.
    cons_price_idx = models.DecimalField(db_column='cons.price.idx', max_digits=5,
                                         decimal_places=3)  # Field renamed to remove unsuitable characters.
    cons_conf_idx = models.DecimalField(db_column='cons.conf.idx', max_digits=3,
                                        decimal_places=1)  # Field renamed to remove unsuitable characters.
    euribor3m = models.DecimalField(max_digits=4, decimal_places=3)
    nr_employed = models.DecimalField(db_column='nr.employed', max_digits=5,
                                      decimal_places=1)  # Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'userdata'
