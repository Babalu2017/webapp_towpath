from dataclasses import field
from django import forms
from .models import User, UserProfile
from .validators import allow_only_images_validator


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
    
    def clean(self):
        cleaned_date =  super(UserForm, self).clean()
        password =  cleaned_date.get('password')
        confirm_password =  cleaned_date.get('confirm_password')
        
        # not field errors
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")


class UserProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Start typing...', 'required': 'required'}))
    profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator])
    cover_photo = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator])

    # 1^ method to make readonly field for long and lat
    # latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    # longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    class Meta:
        model = UserProfile
        # fields = ['profile_picture', 'cover_photo', 'address_line_1', 'address_line_2', 'country', 'state', 'city', 'pin_code', 'latitude', 'longitude']
        fields = ['profile_picture', 'cover_photo', 'address', 'country', 'state', 'city', 'pin_code', 'latitude', 'longitude']


    # 2^ method to make readonly field for long and lat
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'latitude' or field == 'longitude':
                self.fields[field].widget.attrs['readonly'] = 'readonly'

