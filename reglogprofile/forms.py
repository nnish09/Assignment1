from django import forms
from reglogprofile.models import User
from django.forms import ModelForm
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.core.files.images import get_image_dimensions


class SignUpForm(forms.ModelForm):
    username = forms.CharField(max_length=254)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254,required=True)
    
   
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name','phone_no', 'email')
        

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).count() > 0:
            raise forms.ValidationError('This email address is already registered.')
        return email

    def clean_phone_no(self):
        phone_no = self.cleaned_data.get('phone_no')
        # username = self.cleaned_data.get('username')
        if phone_no and User.objects.filter(phone_no=phone_no).count() > 0:
            raise forms.ValidationError('This phone number is already registered.')
        return phone_no



class SetPasswordForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput,max_length=30, required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput,max_length=30, required=False)
  
   
    class Meta:
        model = User
        fields = ('password', 'confirm_password')
        
    # def clean(self):
    #     cleaned_data = super(SetPasswordForm, self).clean()
    #     if 'password' in self.cleaned_data and 'password2' in self.cleaned_data:
    #         if self.cleaned_data['password1'] != self.cleaned_data['password2']:
    #             raise forms.ValidationError("Passwords don't match. Please enter both fields again.")
    #     return self.cleaned_data


    #  def clean(self):
    #     cleaned_data = super(UserForm, self).clean()
    #     password = cleaned_data.get("password")
    #     confirm_password = cleaned_data.get("confirm_password")

    #     if password != confirm_password:
    #         raise forms.ValidationError(
    #             "password and confirm_password does not match"
    #         )

    def clean(self):
        cleaned_data = super(SetPasswordForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        # check for min length
        min_length = 8
        if len(password) < min_length:
            msg = 'Password must be at least %s characters long.' %(str(min_length))
            self.add_error('password', msg)

        # check for digit
        if sum(c.isdigit() for c in password) < 1:
            msg = 'Password must contain at least 1 number.'
            self.add_error('password', msg)

       

        confirm_password = cleaned_data.get('confirm_password')


        if password and confirm_password:
            if password != confirm_password:
                msg = "The two password fields must match."
                self.add_error('confirm_password', msg)
        return cleaned_data


class LoginForm(forms.ModelForm):
    username=forms.CharField(max_length=30, required=True)
    password = forms.CharField(widget=forms.PasswordInput,max_length=30, required=False)
  
   
    class Meta:
        model = User
        fields = ('username', 'password')




class RestrictedImageField(forms.ImageField):
    def __init__(self, *args, **kwargs):
        self.max_upload_size = kwargs.pop('max_upload_size', None)
        if not self.max_upload_size:
            self.max_upload_size = settings.MAX_UPLOAD_SIZE
        super(RestrictedImageField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(RestrictedImageField, self).clean(*args, **kwargs)
        try:
            if data.size > self.max_upload_size:
                raise forms.ValidationError(_('File size must be under %s. Current file size is %s.') % (filesizeformat(self.max_upload_size), filesizeformat(data.size)))
        except AttributeError:
            pass

        return data


class UpdateProfile(forms.ModelForm):
    username = forms.CharField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=True)
    profimg = RestrictedImageField(max_upload_size=2097152)
    organization = forms.CharField(required=False)
    address = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('username','first_name', 'last_name','phone_no','email','profimg','organization','address')

    def clean_picture(self):
       profimg = self.cleaned_data.get("profimg")
       if not profimg:
           raise forms.ValidationError("No image!")
       else:
           w, h = get_image_dimensions(profimg)
           if w <= 500:
               raise forms.ValidationError("The image is %i pixel wide. It's supposed to be 500px" % w)
           if h <= 500:
               raise forms.ValidationError("The image is %i pixel high. It's supposed to be 500px" % h)
       return profimg
