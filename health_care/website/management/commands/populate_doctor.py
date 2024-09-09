# management/commands/add_doctors.py
from django.core.management.base import BaseCommand
from faker import Faker
from website.models import Doctor, Department
import random

class Command(BaseCommand):
    help = 'Add 100 doctors to the database'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create departments if they don't exist
        departments = ['Cardiology', 'Neurology', 'Orthopedics', 'Pediatrics', 'Oncology']
        for dept_name in departments:
            Department.objects.get_or_create(name=dept_name)

        # Fetch all departments
        all_departments = Department.objects.all()

        # Time slots for the day
        time_slots = ['09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30']

        # Add 100 doctors
        for _ in range(100):
            doctor_name = fake.name()
            department = fake.random_element(elements=all_departments)

            # Generate random time slots for each doctor
            available_slots = random.sample(time_slots, k=random.randint(5, 10))  # Randomly select 5 to 10 time slots
            Doctor.objects.create(name=doctor_name, department=department, time_slots=available_slots)

        self.stdout.write(self.style.SUCCESS('Successfully added 100 doctors with time slots'))
