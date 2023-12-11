from django.db import models

# Create your models here.
class doctors(models.Model):
    doc_name = models.CharField(max_length=50)
    contact_no = models.CharField(max_length=50)
    address = models.CharField(max_length=50)

    def __str__(self):
        return self.doc_name
    
class analysis(models.Model):
    user_name = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    analysis_count = models.CharField(max_length=500)
    highest_expression = models.CharField(max_length=50)
    q1 = models.CharField(max_length= 50)
    q2 = models.CharField(max_length= 50)
    q3 = models.CharField(max_length= 50)
    q4 = models.CharField(max_length= 50)
    q5 = models.CharField(max_length= 50)
    q6 = models.CharField(max_length= 50)
    q7 = models.CharField(max_length= 50)
    q8 = models.CharField(max_length= 50)
    q9 = models.CharField(max_length= 50)
    q10 = models.CharField(max_length= 50)
    q11 = models.CharField(max_length= 50)
    q12 = models.CharField(max_length= 50)
    q13 = models.CharField(max_length= 50)
    q14 = models.CharField(max_length= 50)
    q15 = models.CharField(max_length= 50)
    feedback = models.CharField(max_length= 500)
    doc = models.CharField(max_length= 500)

    def __str__(self):
        return self.user_name