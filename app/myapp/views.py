from django.contrib import messages
from django.contrib.auth import login, authenticate, REDIRECT_FIELD_NAME
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LogoutView as BaseLogoutView, PasswordChangeView as BasePasswordChangeView,
    PasswordResetDoneView as BasePasswordResetDoneView, PasswordResetConfirmView as BasePasswordResetConfirmView,
)
from .utils.task import CreateTrainModelPeriodicallyThread
from myapp.datapipe.predUploadedFile import predictUploadedFile
import os
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect, render, get_object_or_404, reverse, HttpResponseRedirect
from django.utils.safestring import mark_safe
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import View, FormView
from django.conf import settings
import pandas
from .datapipe import customize_config
from .models import *
from .forms import *
from .utils.tableUploader import *
import os
from myapp.datapipe.predUploadedFile import predictUploadedFile
from .utils.task import CreateTrainModelPeriodicallyThread


train_t = CreateTrainModelPeriodicallyThread()


def data_entry_page(request):
    # get into the user's folder
    path = './users/' + request.user.get_username() + '/data'
    if not os.path.exists(path):
        os.makedirs(path)
    documents = os.listdir(path)
    error = 0
    if request.method == 'POST':
        try:
            form = DocumentForm(request.POST, request.FILES)
            if form.is_valid():
                # save to personal folder
                newdoc = request.FILES['docfile']
                if '.csv' not in newdoc.name:
                    raise TypeError
                if newdoc.name in documents:
                    form = DocumentForm()
                    context = {'documents': documents, 'form': form, 'error': 2, 'current': 'data_entry_page'}
                    return render(request, 'data_entry_page.html', context)
                fs = FileSystemStorage(location=path)
                filename = fs.save(newdoc.name, newdoc)
                uploaded_file_url = fs.url(filename)

                # upload to db for future training
                newdoc = Document(docfile=request.FILES['docfile'])
                newdoc.save()
                print('==========')
                print("Saving to DB...")
                print('==========')
                uploadFileToDB(newdoc.get_file_path())

                # feed data to model and predict the result

                predictUploadedFile(request.user.get_username(), newdoc.name)
                print('==========')
                print("Predicted...")
                print('==========')
                return redirect('data_entry_page')
            else:
                message = 'The form is not valid. Fix the following error:'
        except:
            form = DocumentForm()
            context = {'documents': documents, 'form': form, 'error': 1, 'current': 'data_entry_page'}
            return render(request, 'data_entry_page.html', context)
        else:
            message = 'The form is not valid. Fix the following error:'
    else:
        form = DocumentForm()
    # get this user's documents
    context = {'documents': documents, 'form': form, 'error': 0, 'current': 'data_entry_page'}
    return render(request, 'data_entry_page.html', context)


def analytics_dashboard_page(request):
    add_graph_form = AddGraphForm()
    if request.method == "POST":
        add_graph_form = AddGraphForm(request.POST or None)
        if add_graph_form.is_valid():
            add_graph_form.save()
    all_graphs = Barchart.objects.all()
    client_x = ["age", "job", "marital", "education", "default", "housing", "loan"]
    dbc_list = []
    for x in client_x:
        dbc_list.append(DoubleBarChart(xaxis=x, title=x.capitalize()))
    return render(request, 'analytics_dashboard_page.html',
                  {'add_graph_form': add_graph_form, 'all_graphs': all_graphs, 'dbc_list': dbc_list})


def delete_graph(request, id):
    Barchart.objects.filter(id=id).delete()
    return redirect(reverse('analytics_dashboard_page'))


def configure_graph(request, id):
    add_graph_form = AddGraphForm()
    print("configure_graph")
    new_xaxis, new_yaxis, new_title = None, None, None
    if request.method == "POST":
        add_graph_form = AddGraphForm(request.POST or None)
        if add_graph_form.is_valid():
            new_xaxis = add_graph_form.cleaned_data.get('xaxis')
            new_yaxis = add_graph_form.cleaned_data.get('yaxis')
            new_title = add_graph_form.cleaned_data.get('title')
    Barchart.objects.filter(id=id).update(
        xaxis=new_xaxis,
        yaxis=new_yaxis,
        title=new_title
    )
    return redirect(reverse('analytics_dashboard_page'))


def calling_operations_page(request):
    path = './users/' + request.user.get_username() + '/result'
    if not os.path.exists(path):
        os.makedirs(path)
    types = os.listdir(path)
    data = {}
    for i in types:
        data[i.split('.')[0]] = pandas.read_csv(path + '/' + i).to_numpy().tolist()
    context = {'current': 'calling_operations_page', 'data': data, 'types': types}
    return render(request, 'calling_operations_page.html', context)


def model_controlls_page(request):
    user = request.user.get_username()
    context = {'current': 'model_controlls_page'}
    config = {}
    print(request.user.get_username())
    global train_t
    message = None
    if train_t.is_alive():
        message = "<span style='color:red'>The periodic training is working!</span>"
    else:
        message = "<span style='color:green'>The periodic training is idle.</span>"
    context = {'current': 'model_controlls_page', 'message': message}

    if request.method == 'POST':
        if 'start' in request.POST:
            if not train_t.is_alive():
                context['message'] = "<span style='color:red'>The periodic training is working!</span>"
                train_t.start()
        elif 'end' in request.POST:
            if train_t.is_alive():
                context['message'] = "<span style='color:green'>The periodic training is idle.</span>"
                train_t.join()
                train_t = CreateTrainModelPeriodicallyThread()
        elif 'configure' in request.POST:
            for i in request.POST:
                config[i] = request.POST[i]
            customize_config.customize_config(config, request.user.get_username())

    return render(request, 'model_controlls_page.html', context)


# ============================================= User Account Pages =============================================


class SignUp(FormView):
    template_name = 'signup.html'
    form_class = SignUpForm

    def form_valid(self, form):
        request = self.request
        user = form.save(commit=False)

        if settings.DISABLE_USERNAME:
            # Set a temporary username
            user.username = get_random_string()
        else:
            user.username = form.cleaned_data['username']

        if settings.ENABLE_USER_ACTIVATION:
            user.is_active = False

        # Create a user record
        user.save()

        # Change the username to the "user_ID" form
        if settings.DISABLE_USERNAME:
            user.username = f'user_{user.id}'
            user.save()

        raw_password = form.cleaned_data['password1']
        user = authenticate(username=user.username, password=raw_password)
        login(request, user)

        messages.success(request, _('You are successfully signed up!'))

        return redirect('/')


class LogIn(FormView):
    template_name = 'login.html'

    @staticmethod
    def get_form_class(**kwargs):
        if settings.DISABLE_USERNAME or settings.LOGIN_VIA_EMAIL:
            return SignInViaEmailForm

        return SignInViaUsernameForm

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        request = self.request

        # If the test cookie worked, go ahead and delete it since its no longer needed
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()

        # The default Django's "remember me" lifetime is 2 weeks and can be changed by modifying
        # the SESSION_COOKIE_AGE settings' option.
        if settings.USE_REMEMBER_ME:
            if not form.cleaned_data['remember_me']:
                request.session.set_expiry(0)

        login(request, form.user_cache)

        redirect_to = request.POST.get(REDIRECT_FIELD_NAME, request.GET.get(REDIRECT_FIELD_NAME))
        url_is_safe = is_safe_url(redirect_to, allowed_hosts=request.get_host(), require_https=request.is_secure())

        if url_is_safe:
            return redirect(redirect_to)

        return redirect(settings.LOGIN_REDIRECT_URL)


class LogOut(LoginRequiredMixin, BaseLogoutView):
    template_name = 'logout.html'

# ==============================================================================================================
