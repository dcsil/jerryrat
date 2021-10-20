from django.shortcuts import redirect, render, get_object_or_404
from django.utils.safestring import mark_safe

from .models import Document, CampaignComboCentent
from .forms import DocumentForm


def data_entry_page(request):
    message = 'Please upload your files'
    notice = "Allowing file types: xlsx, xlsm, xlsb, xls, xlt, xla, csv\n\n" + \
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

            return redirect('data_entry_page')
        else:
            message = 'The form is not valid. Fix the following error:'
    else:
        form = DocumentForm()

    documents = Document.objects.all()
    context = {'documents': documents, 'form': form, 'message': message, 'notice': notice}
    return render(request, 'data_entry_page.html', context)

def campaign_customization_page(request):
    combo1 = CampaignComboCentent(title="P1", description="P1 desc")
    combo2 = CampaignComboCentent(title="P2", description="P2 desc")
    combo3 = CampaignComboCentent(title="P3", description="P3 desc")
    combo4 = CampaignComboCentent(title="P4", description="P4 desc")
    combos = [combo1, combo2, combo3, combo4]
    context = {"combos": combos}
    return render(request, 'campaign_customization_page.html', context)

def analytics_dashboard_page(request):
    context = {}
    return render(request, 'analytics_dashboard_page.html', context)

def calling_operations_page(request):
    context = {}
    return render(request, 'calling_operations_page.html', context)

def model_controlls_page(request):
    context = {}
    return render(request, 'model_controlls_page.html', context)
