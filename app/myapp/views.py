from django.shortcuts import redirect, render, get_object_or_404, reverse
from django.utils.safestring import mark_safe
# import plotly.plotly as py
# import plotly.graph_objs as go

from .models import *
from .forms import DocumentForm
from .utils.tableUploader import *

def data_entry_page(request):
    message = 'Please upload your files'
    notice = "Allowing file types: xlsx, xlsm, xlsb, xls, csv\n\n" + \
             "File must be in specific formats, please see the following for the column specifications:\n" + \
             "<strong>Contact<i> [String]</i></strong>: The mobile/other phone number of the client\n" + \
             "<span class='thick'>First Name <i>[String](Optional)</i></span>: The first name of the client\n" + \
             "<strong>Last Name <i>[String](Optional)</i></strong>: The last name of the client\n" + \
             "<strong>Age <i>[int]</i></strong>: The numeric integer to represent the client's age\n" + \
             "<strong>Job <i>[String]</i></strong>: The categorical label to mark the position/employment status of the client, available values:\n" + \
             "......"
    notice = mark_safe(notice)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()
            uploadFileToDB(newdoc.get_file_path())
            return redirect('data_entry_page')
        else:
            message = 'The form is not valid. Fix the following error:'
    else:
        form = DocumentForm()

    documents = Document.objects.all()
    context = {'documents': documents, 'form': form, 'message': message, 'notice': notice, 'current': 'data_entry_page'}
    return render(request, 'data_entry_page.html', context)

def campaign_customization_page(request):
    combo1 = CampaignComboContent(title="P1", description="P1 desc")
    combo2 = CampaignComboContent(title="P2", description="P2 desc")
    combo3 = CampaignComboContent(title="P3", description="P3 desc")
    combo4 = CampaignComboContent(title="P4", description="P4 desc")
    combo5 = CampaignComboContent(title="P5", description="P5 desc")
    combos = [combo1, combo2, combo3, combo4, combo5]
    context = {"combos": combos, 'current': 'campaign_customization_page'}
    return render(request, 'campaign_customization_page.html', context)


def analytics_dashboard_page(request):
    add_graph_form = AddGraphForm()
    if request.method == "POST":
        add_graph_form = AddGraphForm(request.POST or None)
        if add_graph_form.is_valid():
            add_graph_form.save()
    all_graphs = Linechart.objects.all()
    return render(request, 'analytics_dashboard_page.html', {'add_graph_form': add_graph_form, 'all_graphs': all_graphs})

def delete_graph(request, id):
    Linechart.objects.filter(id=id).delete()
    return redirect(reverse('analytics_dashboard_page'))


def calling_operations_page(request):
    context = {'current': 'calling_operations_page'}
    return render(request, 'calling_operations_page.html', context)

def model_controlls_page(request):
    m1 = PredictionModel(name="Worthy Client Prediction")
    m2 = PredictionModel(name="Campaign Result Prediction")
    m3 = PredictionModel(name="Cost Efficiency Prediction")
    context = {'current': 'model_controlls_page', 'models': [m1, m2, m3]}
    return render(request, 'model_controlls_page.html', context)
