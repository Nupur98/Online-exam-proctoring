from django.db import models

class Candidate(models.Model):
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    gmail=models.EmailField(max_length=30,primary_key=True)
    picture=models.ImageField(upload_to = "images/")
class Candidate_Proc(models.Model):
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    gmail=models.EmailField(max_length=30,primary_key=True)
    Gaze_Score=models.IntegerField()
    

