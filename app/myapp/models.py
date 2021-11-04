from django.db import models
from plotly.offline import plot
from django.contrib.postgres.fields import ArrayField
# import plotly.plotly as py
import plotly.graph_objs as go
from random import uniform

class Graph(models.Model):
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("created_at",)
    
    def count(self):
        return self.graphs.count()


class Linechart(models.Model):
    xaxis = models.CharField(max_length=32)
    yaxis = models.CharField(max_length=32)
    title = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now=True)
    graphs = models.ForeignKey(Graph, null=True, related_name="graphs", on_delete=models.CASCADE)

    class Meta:
        ordering = ("created_at",)

    @property
    def line_chart(self):
        x1, y1 = [i for i in range(50)], [uniform(0, 50) for _ in range(50)]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x1, y=y1))
        fig.layout.update(title=self.title)
        fig.layout.update(
            xaxis_title=self.xaxis,
            yaxis_title=self.yaxis,
            title={
                'text': '<span style="font-size: 20px;"><b>' + self.title + '</b></span>' + '<br>' + \
                        'Line Chart for ' + self.yaxis + ' vs ' + self.xaxis,
                'x': 0.1
            },
            xaxis=dict(
                rangeslider=dict(
                    visible=True,
                    autorange=True,
                    range=[min(x1), max(x1)]
                ),
                type="linear"
            ),
            font=dict(size=12, color="gray")
        )
        plot_div = plot(fig, output_type='div', auto_open=False, 
                        config=dict(
                            displayModeBar=True,
                            displaylogo=False,
                        )
                    )
        return plot_div


class Document(models.Model):
    id = models.AutoField(primary_key=True)
    # docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    docfile = models.FileField(default='', null=True, blank=True)

    def get_file_path(self):
        return self.docfile.path


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
    emp_var_rate = models.DecimalField(db_column='emp.var.rate', max_digits=4, decimal_places=1)  # Field renamed to remove unsuitable characters.
    cons_price_idx = models.DecimalField(db_column='cons.price.idx', max_digits=5, decimal_places=3)  # Field renamed to remove unsuitable characters.
    cons_conf_idx = models.DecimalField(db_column='cons.conf.idx', max_digits=3, decimal_places=1)  # Field renamed to remove unsuitable characters.
    euribor3m = models.DecimalField(max_digits=4, decimal_places=3)
    nr_employed = models.DecimalField(db_column='nr.employed', max_digits=5, decimal_places=1)  # Field renamed to remove unsuitable characters.
    y = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'userdata'