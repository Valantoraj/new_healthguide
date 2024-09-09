from django.db import models
'''from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Login(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
      if self.pk is None:
          self.password = make_password(self.password)
      super().save(*args, **kwargs)

    def __str__(self):
        return self.username'''



from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], blank=True, null=True)
    agreed_to_terms = models.BooleanField(default=False)  # New field for terms and conditions agreement

class Medicine(models.Model):
    sub_category = models.CharField(max_length=500)
    product_name = models.CharField(max_length=500)
    salt_composition = models.TextField()
    product_price = models.CharField(max_length=50,null=True)
    product_manufactured = models.CharField(max_length=500)
    medicine_desc = models.TextField()
    side_effects = models.TextField()
    drug_interactions = models.JSONField()

    def __str__(self):
        return (
            f"Sub-Category: {self.sub_category}\n"
            f"Product Name: {self.product_name}\n"
            f"Salt Composition: {self.salt_composition}\n"
            f"Product Price: {self.product_price}\n"
            f"Product Manufactured: {self.product_manufactured}\n"
            f"Medicine Description: {self.medicine_desc}\n"
            f"Side Effects: {self.side_effects}\n"
            f"Drug Interactions: {self.drug_interactions}"
        )
    
class Contact(models.Model):
    email=models.EmailField(max_length=254)
    name=models.CharField(max_length=250)
    phone_no=models.CharField(max_length=50)
    type=models.CharField(max_length=50,choices=[('query', 'Query'), ('feedback', 'Feedback'), ('other', 'Other')], blank=True, null=True)
    message=models.TextField()

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    # New field to handle available time slots
    time_slots = models.JSONField(default=list)  # Example format: ['09:00', '10:00']

    def __str__(self):
        return self.name

class Book(models.Model):
    name = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=15)
    date = models.DateField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    time = models.TimeField()
    symptoms = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.date} - {self.time}"