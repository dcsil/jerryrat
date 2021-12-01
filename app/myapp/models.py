from django.db import models
from django import forms
from plotly.offline import plot
# from django.contrib.postgres.fields import ArrayField
from django.forms import ModelForm
# import plotly.plotly as py
import plotly.graph_objs as go
from random import uniform

AXES = (('age', 'age'), ('month', 'month'), ('day_of_week', 'day_of_week'), 
        ('duration', 'duration'), ('campaign', 'campaign'), ('pdays', 'pdays'), 
        ('previous', 'previous'))
CHART_TYPES = (('Line Chart', 'Line Chart'), ('Bar Chart', 'Bar Chart'), ('Pie Chart', 'Pie Chart'))

class Linechart(models.Model):
    id = models.AutoField(primary_key=True)
    xaxis = models.CharField(max_length=32, choices=AXES, default=AXES[0][0])
    yaxis = models.CharField(max_length=32, choices=AXES, default=AXES[0][0])
    title = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now=True)
    # graphs = models.ForeignKey(Graph, null=True, related_name="graphs", on_delete=models.CASCADE)

    class Meta:
        ordering = ("created_at",)

    def set_axis(self, x, y):
        self.x, self.y = x, y

    @property
    def line_chart(self):
        x, y = [i for i in range(50)], [uniform(0, 50) for _ in range(50)]
        self.set_axis(x, y)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=self.x, y=self.y))
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
                    range=[min(self.x), max(self.x)]
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


class AddGraphForm(ModelForm):
    class Meta:
        model = Linechart
        fields = '__all__'
        exclude = ['created_at']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': "Please enter the title of the new graph", 'style': 'width: 400px', 'class': 'form-control'})
            # 'graph_type': forms.TextInput(attrs={'placeholder': "Please enter the type of the new graph"})
        }


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

class Userinfo(models.Model):
    dataid = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    numbers = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'userinfo'
