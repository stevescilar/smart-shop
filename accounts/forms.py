from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter Password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Re-Enter Password'
    }))
    class Meta:
        model =Account
        fields = ['first_name','last_name','phone','email','password']
    
    def __init__(self,*args, **kwargs):
        super(RegistrationForm,self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder']='First Name'
        self.fields['last_name'].widget.attrs['placeholder']='Last Name'
        self.fields['phone'].widget.attrs['placeholder']='Phone Number'
        self.fields['email'].widget.attrs['placeholder']='Email Address'
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'

 
