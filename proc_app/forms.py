from django import forms

class UserInput(forms.Form):
    name=forms.CharField(label='First Name',max_length=30,required=True)
    last_name=forms.CharField(label='Last Name',max_length=30,required=True)
    Email=forms.EmailField(label='Email',required=True)
    picture=forms.ImageField(label='Please uploade image in white backgroud')