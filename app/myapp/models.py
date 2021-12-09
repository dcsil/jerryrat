from django.db import models
from plotly.offline import plot
import plotly.graph_objs as go
from .datapipe.readData import *

X_AXES = (('age', 'age'), ('job', 'job'), ('marital', 'marital'), ('education', 'education'), ('default', 'default'),
          ('housing', 'housing'), ('loan', 'loan'))
Y_AXES = (('month', 'month'), ('day_of_week', 'day_of_week'), ('campaign', 'campaign'), ('pdays', 'pdays'),
          ('previous', 'previous'), ('poutcome', 'poutcome'))

def getTitle(self, type, title, xaxis, yaxis):
    title = {
        'text': '<span style="font-size: 20px;"><b>' + title + '</b></span>' + '<br>' + \
                type + ' for ' + yaxis + ' vs ' + xaxis,
        'x': 0.1
    }
    return title


class Barchart(models.Model):
    id = models.AutoField(primary_key=True)
    xaxis = models.CharField(max_length=32, choices=X_AXES, default=X_AXES[0][0])
    yaxis = models.CharField(max_length=32, choices=Y_AXES, default=Y_AXES[0][0])
    title = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("created_at",)

    @property
    def get_barchart(self):
        x_data, info = get_graph_data(self.xaxis, self.yaxis)
        fig = go.Figure(data=[
            go.Bar(name=str(k), x=x_data, y=info[k]) for _, k in enumerate(info)
        ])
        fig.layout.update(title=self.title)
        fig.layout.update(barmode='stack')
        fig.layout.update(
            xaxis_title=self.xaxis,
            yaxis_title=self.yaxis,
            title=getTitle(self, 'Stacked Barchart', self.title, self.xaxis, self.yaxis),
            font=dict(size=12, color="gray"),
            showlegend=True
        )
        plot_div = plot(fig, output_type='div', auto_open=False,
                        config=dict(
                            displayModeBar=True,
                            displaylogo=False,
                        )
                    )
        return plot_div


class DoubleBarChart(models.Model):
    id = models.AutoField(primary_key=True)
    xaxis = models.CharField(max_length=32, choices=X_AXES, default=X_AXES[0][0])
    title = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("created_at",)

    @property
    def get_double_barchart(self):
        x_data, info = get_graph_data(self.xaxis, "y")
        fig = go.Figure()
        if "yes" in info:
            fig.add_trace(go.Bar(
                x=x_data,
                y=info["yes"],
                name='Yes',
                marker_color='indianred'
            ))
        if "no" in info:
            fig.add_trace(go.Bar(
                x=x_data,
                y=info["no"],
                name='No',
                marker_color='lightsalmon'
            ))
        fig.layout.update(title=self.title)
        fig.layout.update(barmode='group', xaxis_tickangle=-45)
        fig.layout.update(
            xaxis_title=self.xaxis,
            yaxis_title="results",
            title=getTitle(self, 'Double Barchart', self.title, self.xaxis, 'Outcome'),
            font=dict(size=12, color="gray"),
            showlegend=True
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
    emp_var_rate = models.DecimalField(db_column='emp.var.rate', max_digits=4,
                                       decimal_places=1)  # Field renamed to remove unsuitable characters.
    cons_price_idx = models.DecimalField(db_column='cons.price.idx', max_digits=5,
                                         decimal_places=3)  # Field renamed to remove unsuitable characters.
    cons_conf_idx = models.DecimalField(db_column='cons.conf.idx', max_digits=3,
                                        decimal_places=1)  # Field renamed to remove unsuitable characters.
    euribor3m = models.DecimalField(max_digits=4, decimal_places=3)
    nr_employed = models.DecimalField(db_column='nr.employed', max_digits=5,
                                      decimal_places=1)  # Field renamed to remove unsuitable characters.
    y = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'userdata'


class Userinfo(models.Model):
    dataid = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    numbers = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'userinfo'
