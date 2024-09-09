from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,Book  # Make sure to import your custom user model


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=False)
    name = forms.CharField(max_length=100, required=False)
    date_of_birth = forms.DateField(required=False)
    gender = forms.ChoiceField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], required=False)
    terms = forms.BooleanField(required=True, label="I agree to the Terms and Conditions")

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'name', 'date_of_birth', 'gender', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone_number = self.cleaned_data.get('phone_number')
        user.name = self.cleaned_data.get('name')
        user.date_of_birth = self.cleaned_data.get('date_of_birth')
        user.gender = self.cleaned_data.get('gender')
        
        if commit:
            user.save()
        return user
    
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['email', 'name', 'phone_no', 'type', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
        }

class BookForm(forms.ModelForm):
    
    class Meta:
        model = Book
        fields = ['name', 'phone_no', 'date','department','doctor','time','symptoms']
        widgets = {
            'department':forms.Select(),
            'doctor':forms.Select(),
        
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.Select(),
        }

class HeartForm(forms.Form):
    AGE_CHOICES = [(i, str(i)) for i in range(0, 121)]
    SEX_CHOICES = [
        (1, 'Male'),
        (0, 'Female'),
    ]
    CHEST_PAIN_CHOICES = [
        (1, 'Typical Angina'),
        (2, 'Atypical Angina'),
        (3, 'Non-anginal Pain'),
        (4, 'Asymptomatic'),
    ]
    FBS_CHOICES = [
        (1, 'Yes'),
        (0, 'No'),
    ]
    EKG_CHOICES = [
        (0, 'Normal'),
        (1, 'Abnormal'),
        (2, 'Hypertrophy'),
    ]
    EXERCISE_ANGINA_CHOICES = [
        (1, 'Yes'),
        (0, 'No'),
    ]
    SLOPE_CHOICES = [
        (1, 'Upsloping'),
        (2, 'Flat'),
        (3, 'Downsloping'),
    ]
    THALLIUM_CHOICES = [
        (3, 'Normal'),
        (6, 'Fixed Defect'),
        (7, 'Reversible Defect'),
    ]
    
    age = forms.IntegerField(label="Age", min_value=0, max_value=120, required=True)
    sex = forms.ChoiceField(label="Sex", choices=SEX_CHOICES, required=True)
    chest_pain = forms.ChoiceField(label="Chest Pain Type", choices=CHEST_PAIN_CHOICES, required=True)
    bp = forms.IntegerField(label="Blood Pressure (BP)", required=True)
    cholesterol = forms.IntegerField(label="Cholesterol", required=True)
    fbs = forms.ChoiceField(label="Fasting Blood Sugar (FBS over 120)", choices=FBS_CHOICES, required=True)
    ekg = forms.ChoiceField(label="EKG Results", choices=EKG_CHOICES, required=True)
    max_hr = forms.IntegerField(label="Maximum Heart Rate (Max HR)", required=True)
    exercise_angina = forms.ChoiceField(label="Exercise Induced Angina", choices=EXERCISE_ANGINA_CHOICES, required=True)
    st_depression = forms.DecimalField(label="ST Depression", max_digits=4, decimal_places=1, required=True)
    slope = forms.ChoiceField(label="Slope of ST Segment", choices=SLOPE_CHOICES, required=True)
    num_vessels = forms.IntegerField(label="Number of Vessels Fluoroscopy", min_value=0, max_value=3, required=True)
    thallium = forms.ChoiceField(label="Thallium Stress Test", choices=THALLIUM_CHOICES, required=True)

class LungForm(forms.Form):
    GENDER_CHOICES = [
        ('F', 'Female'),
        ('M', 'Male'),
    ]
    YES_NO_CHOICES = [
        (2, 'Yes'),
        (1, 'No'),
    ]
    SCALE_CHOICES = [
        (1, 'Low'),
        (2, 'High')
    ]

    gender = forms.ChoiceField(label="Gender", choices=GENDER_CHOICES, required=True)
    age = forms.IntegerField(label="Age", min_value=0, required=True)
    smoking = forms.ChoiceField(label="Smoking", choices=SCALE_CHOICES, required=True)
    yellow_fingers = forms.ChoiceField(label="Yellow Fingers", choices=YES_NO_CHOICES, required=True)
    anxiety = forms.ChoiceField(label="Anxiety", choices=YES_NO_CHOICES, required=True)
    peer_pressure = forms.ChoiceField(label="Peer Pressure", choices=SCALE_CHOICES, required=True)
    chronic_disease = forms.ChoiceField(label="Chronic Disease", choices=YES_NO_CHOICES, required=True)
    fatigue = forms.ChoiceField(label="Fatigue", choices=SCALE_CHOICES, required=True)
    allergy = forms.ChoiceField(label="Allergy", choices=YES_NO_CHOICES, required=True)
    wheezing = forms.ChoiceField(label="Wheezing", choices=SCALE_CHOICES, required=True)
    alcohol_consuming = forms.ChoiceField(label="Alcohol Consuming", choices=SCALE_CHOICES, required=True)
    coughing = forms.ChoiceField(label="Coughing", choices=SCALE_CHOICES, required=True)
    shortness_of_breath = forms.ChoiceField(label="Shortness of Breath", choices=SCALE_CHOICES, required=True)
    swallowing_difficulty = forms.ChoiceField(label="Swallowing Difficulty", choices=YES_NO_CHOICES, required=True)
    chest_pain = forms.ChoiceField(label="Chest Pain", choices=SCALE_CHOICES, required=True)

class DiabetesForm(forms.Form):
    pregnancies = forms.IntegerField(label="Pregnancies", min_value=0, required=True)
    glucose = forms.FloatField(label="Glucose", min_value=0, required=True)
    blood_pressure = forms.FloatField(label="Blood Pressure", min_value=0, required=True)
    skin_thickness = forms.FloatField(label="Skin Thickness", min_value=0, required=True)
    insulin = forms.FloatField(label="Insulin", min_value=0, required=True)
    bmi = forms.FloatField(label="BMI", min_value=0, required=True)
    diabetes_pedigree_function = forms.FloatField(label="Diabetes Pedigree Function", min_value=0, required=True)
    age = forms.FloatField(label="Age", min_value=0, required=True)


class StrokeForm(forms.Form):
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female')]
    WORK_TYPE_CHOICES = [('Private', 'Private'), ('Self-employed', 'Self-employed'), ('Govt_job', 'Government job'), ('children', 'Children')]
    RESIDENCE_TYPE_CHOICES = [('Urban', 'Urban'), ('Rural', 'Rural')]
    SMOKING_STATUS_CHOICES = [('never smoked', 'Never smoked'), ('formerly smoked', 'Formerly smoked'), ('smokes', 'Smokes')]

    gender = forms.ChoiceField(label="Gender", choices=GENDER_CHOICES, required=True)
    age = forms.IntegerField(label="Age", min_value=0, required=True)
    hypertension = forms.BooleanField(label="Hypertension", required=False)
    heart_disease = forms.BooleanField(label="Heart Disease", required=False)
    ever_married = forms.ChoiceField(label="Ever Married", choices=[('Yes', 'Yes'), ('No', 'No')], required=True)
    work_type = forms.ChoiceField(label="Work Type", choices=WORK_TYPE_CHOICES, required=True)
    Residence_type = forms.ChoiceField(label="Residence Type", choices=RESIDENCE_TYPE_CHOICES, required=True)
    avg_glucose_level = forms.FloatField(label="Average Glucose Level", min_value=0, required=True)
    bmi = forms.FloatField(label="BMI", min_value=0, required=True)
    smoking_status = forms.ChoiceField(label="Smoking Status", choices=SMOKING_STATUS_CHOICES, required=True)
    
class KidneyStoneForm(forms.Form):
    gravity = forms.FloatField(label="Gravity", min_value=0, required=True)
    ph = forms.FloatField(label="pH", min_value=0, required=True)
    osmo = forms.FloatField(label="Osmolality", min_value=0, required=True)
    cond = forms.FloatField(label="Conductivity", min_value=0, required=True)
    urea = forms.FloatField(label="Urea", min_value=0, required=True)
    calc = forms.FloatField(label="Calcium", min_value=0, required=True)

class LiverDiseaseForm(forms.Form):
    age = forms.IntegerField(
        label="Age",
        min_value=20,
        max_value=80,
        required=True
    )
    
    gender = forms.ChoiceField(
        label="Gender",
        choices=[(0, 'Male'), (1, 'Female')],
        required=True
    )
    
    bmi = forms.FloatField(
        label="BMI",
        min_value=15,
        max_value=40,
        required=True
    )
    
    alcohol_consumption = forms.FloatField(
        label="Alcohol Consumption",
        min_value=0,
        max_value=20,
        required=True
    )
    
    smoking = forms.ChoiceField(
        label="Smoking",
        choices=[(0, 'No'), (1, 'Yes')],
        required=True
    )
    
    genetic_risk = forms.ChoiceField(
        label="Genetic Risk",
        choices=[(0, 'Low'), (1, 'Medium'), (2, 'High')],
        required=True
    )
    
    physical_activity = forms.FloatField(
        label="Physical Activity",
        min_value=0,
        max_value=10,
        required=True
    )
    
    diabetes = forms.ChoiceField(
        label="Diabetes",
        choices=[(0, 'No'), (1, 'Yes')],
        required=True
    )
    
    hypertension = forms.ChoiceField(
        label="Hypertension",
        choices=[(0, 'No'), (1, 'Yes')],
        required=True
    )
    
    liver_function_test = forms.FloatField(
        label="Liver Function Test",
        min_value=20,
        max_value=100,
        required=True
    )
