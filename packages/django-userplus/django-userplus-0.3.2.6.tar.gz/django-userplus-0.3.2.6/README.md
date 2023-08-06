# django-userplus
Django-Userplus is an extenstion of Django auth_user module that comes with some extra functionalities.

### Compatibility
django >= 1.9


### Features
* Login with username or email
* uuid primary key
* case-insensitve authentication
* generates user activation key on signup
* improved password validatior


### Installation:
```
$ pip install django-userplus
```
* add ```"userplus"``` to ```INSTALLED_APPS``` in your settings file
* add the following to `urls.py`
```
url(r'^user/', include('userplus.urls')),
```


### Usage:

to make use of django-userplus, you need to extend the model in your user model like so.
```python
...
from userplus.models import UserPlus

class User(UserPlus):
    pass  # you can add other fields here.
```
django-userplus comes with signup and login forms out of the box, so in your views you can make use of the forms like so.
```python
from userplus.forms import SignUpForm, SignInForm
from django.contrib.auth import authenticate

class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        ...

    def post(self, request):
        form = SignUpForm(request.POST)

        if form.is_valid:
            user = form.save()
            ...

class SignInView(View):
    def get(self, request):
        form = SignInForm()
        ...

    def post(self, request):
        form = SignInForm(request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user:
                login(request, user)
                ...
```

##### Sign in with Username or Email :
To use django-userplus agnostic signin feature, add the following to your `settings.py`
```python
...
AUTHENTICATION_BACKENDS = ['userplus.backends.UserPlusBackend']
...
```

This makes `django.contrib.auth.authenticate` **username** or **email** agnostic, i.e it would authenticate the user if she inputs her `email` or her `username`. So you can do this.

```python
from django.contrib.auth import authenticate

user = authenticate(username='JohnDoe', password='MySecret')
```
or

```python
from django.contrib.auth import authenticate

user = authenticate(email='johndoe@email.com', password='MySecret')
```

If you use userplus SigninForm this already comes with a `username_or_email` field that auto-detects what the user has passed in.

### User Activation key:
To set activation key on signup, add the following to `settings.py`.

```python
...
USERPLUS_SET_ACTIVATION_KEY = True
...
```
you can also set an *optional* parameter for how long the key is valid for. This defaults to 2 days if not set;

```python
...
USERPLUS_ACTIVATION_DAYS = 3  # valid for 3 days.
...
```

On Signup an activation key will then be set for the user. The user needs to activate this before she can login. After saving the user form on signup, an activation email can be sent like so.

```python
...
user = form.save()
url = reverse('userplus_confirm_registration', kwargs={
                               'activation_key': user.activation_key})
user.email_user('Confirmation Email', url)
```

### Password Validation:
Although django 1.9 comes with quite some useful password validators. You can also add Userplus pattern validator to enforce a stronger password. Simply add to the already existing `AUTH_PASSWORD_VALIDATORS` variable in `settings.py`.

```python
...
AUTH_PASSWORD_VALIDATORS = [
    ...
    {
        'NAME': 'userplus.validators.PatternValidator',
    },
]
```
this would enusre the password contains uppercase and lowercase alphabet, Number and Special Character.
