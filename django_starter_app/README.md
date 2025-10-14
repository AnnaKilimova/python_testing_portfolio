# 🎓 Django Starter App
A small Django project with two applications:

- **courses_app** — for managing courses  
- **members_app** — for managing participants

The project demonstrates a **many-to-many relationship** between models, as well as basic CRUD operations (creating and displaying objects via forms and templates).

## ⚙️ Installation and Environment Setup
### 1. Clone the repository
```bash
git clone https://github.com/AnnaKilimova/python_testing_portfolio.git
```
### 2. Navigate to the project folder:
```bash
cd django_starter_app
```
### 3. Create and activate a virtual environment
#### For MacOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate    
```  
#### For Windows:
```bash
venv\Scripts\activate    
```
### 4. Install dependencies
Make sure you are in the root folder of the project, where the requirements.txt file is located.
If you are currently inside a subproject (for example, django_starter_app), go one level up first:
```bash
cd ..
pip install -r requirements.txt    
```
or, if you prefer to stay in the subproject folder:
```bash
pip install -r ../requirements.txt 
```
This command will install all necessary Python packages listed in the requirements.txt file,
so your environment matches the dependencies used in the project.
## 🧩 Task Description
Create a new Django project and implement two applications:
- courses_app - for managing courses
- members_app - for managing participants
### 📝 Requirements:
1. The models should have a many-to-many relationship between courses and members.
2. Each app must include:
   - Model (models.py)
   - Form (forms.py)
   - Views (views.py) for listing and creating objects
   - Templates (templates/) for displaying lists and forms
3. Set up routes (urls.py) and include them in the main project urls.py.
### 🧪 Running Tests
```bash
# ---------------- unittest ----------------
python manage.py test
```
The tests check:
- creation of Course and Member objects;
- many-to-many relationship between courses and members;
- form validation (CourseForm, MemberForm);
- basic view functionality (listing and creation).
### 🚀 Running the Application
After successful tests, start the development server:
```bash
python manage.py runserver
```
The app will be available at:
```bash
👉 http://127.0.0.1:8000/
```
Available routes:
- [/admin/](http://127.0.0.1:8000/admin/) - admin panel
- [/courses/](http://127.0.0.1:8000/courses/) - list of courses
- [/courses/create/](http://127.0.0.1:8000/courses/create/) - form for adding a new course
- [/members/](http://127.0.0.1:8000/members/) - list of members
- [/members/create/](http://127.0.0.1:8000/members/create/) - form for adding a new member
  
## 🧱 Project Structure
```
django_starter_app/
│
├── courses_app/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   ├── apps.py
│   ├── tests.py
│   ├── templates/courses_app/
│   │   ├── course_list.html
│   │   └── course_form.html
│   └── migrations/
│       ├── __init__.py
│       └── 0001_initial.py
│
├── django_starter_app/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── members_app/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── apps.py
│   ├── tests.py
│   ├── templates/members_app/
│   │   ├── member_list.html
│   │   └── member_form.html
│   └── migrations/
│       ├── __init__.py
│       └── 0001_initial.py
│
└── manage.py
```
### 🧠 Notes

The email field in the Member model uses EmailField(unique=True) - ensures email uniqueness.
Validation occurs automatically through MemberForm.

All tests use django.test.TestCase to provide database isolation.
