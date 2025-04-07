# BE-Capstone-project
This repo contains my BE capstone project(task management app)
## Task management app 
STARTING PROJECT
## WEEK 1//
project= Task_manager
app=tasks
## WEEK 2  DEFINING USER MODELS AND AUTHENTICATION BACKENDS
##  User Authentication Features
- **Custom User Model** (Email-based authentication)
- **User Registration**
- **User Login & Logout**
- **Session & Token Authentication**
- **Role-based Access Control (Admins & Users)**
----------------------------------------------------------
- created user model using custom user manager in models.py
- cretaed custom usercreation form and custom user login form 
- created authentications.py to handle backend auths such as log in with email
- created views for user creation (registration.html) and added url configurations
- created login & logout views that use auths to login user
- created homeview  where user is led after login in or registration

# urls
`http://127.0.0.1:8000/register/`      (register)
`http://127.0.0.1:8000/login/`         (login)
`http://127.0.0.1:8000/logout/`        (logout)
`http://127.0.0.1:8000/`               (lists tasks)
`http://127.0.0.1:8000/home/`          (showes home/ require loged in user)
`http://127.0.0.1:8000/create/`        (creating new tasks)
`http://127.0.0.1:8000/<int:pk>/`      (viewing tasks details)
`http://127.0.0.1:8000/<int:pk>/edit/` (editing task)
`http://127.0.0.1:8000/<int:pk>/delete/`(deleting task)
## API urls
`http://127.0.0.1:8000/api/tasks/	 `                       (listtasks)
`http://127.0.0.1:8000/api/tasks/create/`  	             (create Task)
`http://127.0.0.1:8000/api/tasks/{id}/`                    (tasks detail)
`http://127.0.0.1:8000/api/tasks/{id}/update/`	         (updating task)
`http://127.0.0.1:8000/api/tasks/{id}/delete/`	         (deleting task)


# SETTINGS
# redirects 
- This defines the URL where users will be redirected 
- if they try to access a restricted page without being logged in.
`LOGIN_URL = '/tasks/login/'`
- After a user successfully logs in, Django will redirect them to this URL by default.
`LOGIN_REDIRECT_URL = '/tasks/home/' `
- When a user logs out, they will be redirected to this URL.
`LOGOUT_REDIRECT_URL = '/tasks/login/'`
# to use the custom user created
AUTH_USER_MODEL = 'tasks.CustomUser' 
# Custom email login backend
AUTHENTICATION_BACKENDS = [
    'tasks.authentications.EmailBackend',  
]
# directory for templates
'DIRS': [BASE_DIR / "templates"], #show template directory

# WEEK 3 defining a task model and categories /status /creating its views &urls
# also define admin to manage users
` !!  I HAVE DECIDED TO MAKE CATEGORIES AS A FIELD RATHER THAN A MODEL  !!`
- created tasks model with its fields in models.py
- created serialzers.py (used in API )
- created CRUD views for tasks model
- creating tasks api views
- implemented urls

# completed project
- modified c codes for the web
- deployed on python anywhere === `https://timothyandre.pythonanywhere.com/`
- provided a 5 minute demo video on loom


