from django.shortcuts import redirect, render
from .models import Document
from .forms import DocumentForm


def my_view(request):
    bold_start, bold_end = "\033[1m", "\033[0;0m"
    message = 'Please upload your files'
    notice = "Allowing file types: xlsx, xlsm, xlsb, xls, xlt, xla, csv\n\n" + \
             "File must be in specific formats, please see the following for the column specifications:\n" + \
             "Contact[String]: The mobile/other phone number of the client\n" + \
             "First Name[String](Optional): The first name of the client\n" + \
             "Last Name[String](Optional): The last name of the client\n" + \
             "Age[int]: The numeric integer to represent the client's age\n" + \
             "Job[String]: The categorical label to mark the position/employment status of the client, available values:\n" + \
             "......"
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            return redirect('my-view')
        else:
            message = 'The form is not valid. Fix the following error:'
    else:
        form = DocumentForm()

    documents = Document.objects.all()

    context = {'documents': documents, 'form': form, 'message': message, 'notice': notice}
    return render(request, 'list.html', context)
