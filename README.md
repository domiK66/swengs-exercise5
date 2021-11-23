
### 1. Download updated yamod app from Moodle

### 2.1 Install Django REST framework and JWT framework
- We use an 3rd party library to implement REST interfaces in Django – it is called Django REST framework [1] (Version 3.12.4)

```python 
pip install djangorestframework 
```

- In settings.py add 'rest_framework' in INSTALLED_APPS

### 2.2 Adding security
- In order to secure our APIs, we use the djangorestframework-jwt (Version 1.11.0)

```python 
pip install djangorestframework-jwt 
```

- Add the following snippet to your Django project's settings.py

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}
```

### 3. Update your Django project's urls.py

### 4. Open Django Admin at http://localhost:8000/admin and log in

### 5. In a separate browser tab open http://localhost:8000/ - you should see the interactive API

### 6. Open yamod/views.py and work through the TODOs – again until all tests work – in parallel you can use the browser-based interactive API to test your results