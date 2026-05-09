# Hostel Room Allocation System

A modern Django-based Hostel Room Allocation System designed to simplify hostel room management for administrators and students. The system provides room allocation, waiting list management, student registration, fee management, and gender-based room filtering.

---

# Features

## Student Management

* Student registration and login system
* Secure authentication using Django authentication
* Student profile management
* Roll number based identification

## Room Management

* Add and manage hostel rooms
* Block-wise room organization
* Gender-based room allocation
* Room capacity management

## Allocation Management

* Allocate rooms to students
* Prevent duplicate allocations
* Allocation status management

## Smart Room Filtering

* Male students can only view male rooms
* Female students can only view female rooms
* Dynamic room filtering using AJAX without page reload

## Waiting List System

* Students can be added to waiting list
* Automatically removes students from waiting list after room allocation

## Fee Management

* Track hostel fee payments
* Paid and unpaid fee status
* Due date management

## Dashboard Features

* Separate admin and student functionalities
* Students can view their room allocation details
* Admin can manage all hostel operations

---

# Technologies Used

* Python
* Django
* HTML
* CSS
* Bootstrap
* JavaScript
* AJAX
* SQLite

---

# Project Structure

```text
hostel_project/
│
├── allocation/
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── hostel_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── manage.py
└── db.sqlite3
```

---

# Database Models

## Student Model

Stores student details such as:

* Name
* Roll number
* Gender
* Course
* Year
* Contact
* Email

## Room Model

Stores room details:

* Room number
* Block
* Gender type
* Capacity

## Allocation Model

Stores room allocation information:

* Student
* Room
* Allocation date
* Allocation status

## Waitlist Model

Stores students waiting for room allocation.

## Fee Model

Stores fee payment details.

---

# Installation Guide

## Step 1: Clone Repository

```bash
git clone https://github.com/kombact/project-hostel-room-allocation-system.git
```

## Step 2: Navigate to Project Folder

```bash
cd project-hostel-room-allocation-system
```

## Step 3: Create Virtual Environment

```bash
python -m venv venv
```

## Step 4: Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

## Step 5: Install Dependencies

```bash
pip install django
```

## Step 6: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Step 7: Create Superuser

```bash
python manage.py createsuperuser
```

## Step 8: Start Development Server

```bash
python manage.py runserver
```

Open browser:

```text
http://127.0.0.1:8000/
```

---

# AJAX Based Dynamic Room Filtering

The project includes dynamic room filtering functionality.

When an admin selects a student during room allocation:

* Only rooms matching the student's gender are displayed
* Rooms update instantly without page reload

This functionality is implemented using:

* JavaScript Fetch API
* Django JsonResponse
* AJAX requests

---

# Future Improvements

* Online hostel fee payment integration
* Email notifications
* QR code based hostel entry
* Room vacancy analytics dashboard
* Complaint management system
* Mobile responsive enhancements
* PDF report generation

#

---

# Author

Navaneeth P.

MCA Student CCSIT Calicut university

---

# License

This project is developed for educational and academic purposes.
