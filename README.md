# doctor_patient_appointment

## Overview:
This project is made for doctor and patient appointment booking as per the following rules and guidelines:
Build a Django REST Application that allows patients to connect to doctors and book
appointments. Each day is divided into time slots of 30 mins each, starting from 9 am to 9
pm. Doctors can login to the portal and declare their availability for the given day in terms of
slots. Patients can login and book appointments/ cancel existing appointments.
Functionalities required (Must Have):

1. A new doctor should be able to register
2. A doctor should be able to declare his/her availability in each 30 min slot for the day
from 9 am
3. Patients should be able to login, and look at all available slots across all doctors. The
slots should be sorted by slot time. However, the sorting criteria can be extended in
future
4. Patients should be able to book appointments with a doctor for an available slot. A
patient can book multiple slots in the same day. A patient cannot book two
appointments with two different doctors in the same time slot
5. Patients can also cancel an appointment, in which case that slot becomes available
for someone else to book
6. Search functionality for all booked appointments given the doctor's name or patient's
name

## Steps to run the project:
### Step 1: Project setup

1. Install the project
    ```bash
    git clone git_repo_ssh
    cd doctor_patient_appointment/ && python -m venv venv
    source venv/bin/activate
    pip install -r doctor_appointment/requirement.txt
    ```

1. Create database in postgres:
    ```bash
    sudo su postgres
    psql
    create database appointment;
    create user omkar with encrypted password '123';
    grant all privileges on database appointment to omkar;
    ```

1. Make migrations:
    The credentials of the superuser are to be used for jwt authentication to create bearer token and then wwe use the token for all apis.
    ```bash
    python manage.py makemigrations && python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver
    ```

### Step 2: Authentication Endpoints

### 1. Obtain Token
**URL:** `http://127.0.0.1:8000/api/api/token_obtain/`  
**Method:** `POST`  
**Description:** Obtain JWT token using username and password.

**Request Body:**
Use the credentials of the superuser you created only to created doctor and patient. Later use the token of doctor and patient for their respective apis. 
Get this response access token to only create `doctor` and `patient`.
```json
{
    "username": "user1",
    "password": "password123"
}
```

### 2. Verify Token
**URL:** `http://127.0.0.1:8000/api/api/token_verify/`  
**Method:** `POST`  
**Description:** Verify JWT token.


**Request Body:**
```json
{
    "token": "access_token"
}
```

### 3. Refresh Token

**URL:** `http://127.0.0.1:8000/api/api/token_refresh/`  
**Method:** `POST`  
**Description:** Refresh JWT token.

**Request Body:**

```json
{
    "refresh": "refresh_token"
}
```

### 4. User Registration Endpoints Register Doctor

**URL:** `http://127.0.0.1:8000/api/register_doctor/`  
**Method:** `POST`  
**Description:** Register a new doctor.

**Request Body:**
```json
{
    "user": {
        "username": "doctor1",
        "email": "doctor1@gmail.com",
        "password": "123"
    }
}
```

### 5. User Registration Endpoints Register Patient

**URL:** `http://127.0.0.1:8000/api/register_patient/`  
**Method:** `POST`  
**Description:** Register a new patient.

**Request Body:**
```json
{
    "user": {
        "username": "patient1",
        "email": "patient1@gmail.com",
        "password": "123"
    }
}
```

### 6. TimeSlot Api
To create a timeslot of 30min each from 9a.m. to 9p.m. use the `populate_time_slot.py` file.

```bash
    python manage.py populate_time_slot
```

1. List TimeSlots
    **URL:** `http://127.0.0.1:8000/api/timeslots/`  
    **Method:** `GET`  
    **Description:**  Retrieve a list of all timeslots.

    **Request Body:**

    ```json
    [
        {
            "id": 1,
            "start_time": "09:00:00",
            "end_time": "10:00:00"
        }
    ]
    ```

2. Create TimeSlot

    **URL:** `http://127.0.0.1:8000/api/timeslots/`  
    **Method:** `POST`  
    **Description:** Create a new timeslot.

    **Request Body:**

    ```json
    {
        "start_time": "09:00:00",
        "end_time": "10:00:00"
    }
    ```

3. Update TimeSlot

    **URL:** `http://127.0.0.1:8000/api/timeslots/{id}/`  
    **Method:** `PUT`  
    **Description:** Update a timeslot by ID.
    
    **Request Body:**

    ```json
    {
        "start_time": "10:00:00",
        "end_time": "11:00:00"
    }
    ```
    
4. Delete TimeSlot

    **URL:** `http://127.0.0.1:8000/api/timeslots/{id}/`  
    **Method:** `DELETE`  
    **Description:** Delete a timeslot by ID.

### 7. Availability Endpoints
**The Patients can only view/list this Api and the Doctors can have get, post, put and delete access**
1. List Availabilities
    
    **URL:** `http://127.0.0.1:8000/api/availabilities/`  
    **Method:** `GET`  
    **Description:** Retrieve a list of all available time slots for doctors, sorted by date and start time.
    
    **Request Body:**

2. Create Availability

    **URL:** `http://127.0.0.1:8000/api/availabilities/`  
    **Method:** `POST`  
    **Description:** Create a new availability (only accessible by doctors).
    
    **Request Body:**

    ```json
    {
        "doctor": 1,
        "date": "2024-05-22",
        "time_slot": 1,
        "is_available": true
    }
    ```

3. Update Availability

    **URL:** `http://127.0.0.1:8000/api/availabilities/{id}/`  
    **Method:** `PUT`  
    **Description:** Update an availability by ID (only accessible by doctors).
    
    **Request Body:**

    ```json
    {
        "doctor": 1,
        "date": "2024-05-22",
        "time_slot": 1,
        "is_available": false
    }
    ```

4. Delete Availability

    **URL:** `http://127.0.0.1:8000/api/availabilities/{id}/`  
    **Method:** `DELETE`  
    **Description:** Delete an availability by ID (only accessible by doctors).
    
### 8. Appointment Endpoints
**Only Patient can create an Appoinment and both Patient and Doctor can delete an Appoinment**
1. List Appointments

    **URL:** `http://127.0.0.1:8000/api/appointments/`  
    **Method:** `GET`  
    **Description:** Retrieve a list of all appointments.
    
2. Create Appointment

    **URL:** `http://127.0.0.1:8000/api/appointments/`  
    **Method:** `POST`  
    **Description:** Create a new appointment (only accessible by patients).
    
    **Request Body:**

    ```json
    {
        "patient": 1,
        "doctor": 1,
        "date": "2024-05-22",
        "time_slot": 1
    }
    ```

3. Update Appointment

    **URL:** `http://127.0.0.1:8000/api/appointments/{id}/`  
    **Method:** `PUT`  
    **Description:** Update an appointment by ID (only accessible by patients).
    
    **Request Body:**

    ```json
    {
        "patient": 1,
        "doctor": 1,
        "date": "2024-05-23",
        "time_slot": 2
    }
    ```

4. Delete Appointment

    **URL:** `http://127.0.0.1:8000/api/appointments/{id}/`  
    **Method:** `DELETE`  
    **Description:** Delete an appointment by ID (only accessible by patients or doctors).
    
5. Search Appointments

    **URL:** `http://127.0.0.1:8000/api/appointments/search/`  
    **Method:** `GET`  
    **Description:** Search for appointments by doctor or patient name.
    
    **Request Body:**

    ```json
    Query Parameters:

    doctor: The username of the doctor to search for.
    patient: The username of the patient to search for.
    ```
    `http://127.0.0.1:8000/api/appointments/search/?doctor=doctor_name&patient=patient_name`  
    ```