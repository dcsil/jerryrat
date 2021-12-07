from django.contrib.auth import get_user_model

# create temporary account if not exist
try:
    User = get_user_model()
    user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
except:
    pass