from django.db import models
from django.contrib.auth.models import User

# Student model is linked to Django's built-in User model
# This way each student has their own login (roll number + password)
class Student(models.Model):

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    # This links the student to a login account
    # When a student registers, a User is created automatically
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    course = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    contact = models.CharField(max_length=15)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"Rollno :{self.roll_number} --- Name:{self.name}"


# This model stores room information
class Room(models.Model):

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    room_number = models.CharField(max_length=10)
    block = models.CharField(max_length=10)
    gender_type = models.CharField(max_length=10, choices=GENDER_CHOICES)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return f"Room {self.room_number} - Block {self.block}"


# This model stores which student is allocated to which room
class Allocation(models.Model):

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Vacated', 'Vacated'),
    ]

    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    allocated_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')

    def __str__(self):
        return f"{self.student.name} - Room {self.room.room_number}"


# This model stores students who are waiting for a room
class WaitlistEntry(models.Model):

    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    requested_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Waitlist - {self.student.name}"

# This model stores fee details for each student
class Fee(models.Model):

    STATUS_CHOICES = [
        ('Paid', 'Paid'),
        ('Unpaid', 'Unpaid'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)  # e.g. "Hostel Fee - June 2025"
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Unpaid')

    def __str__(self):
        return f"{self.student.name} - {self.description}"