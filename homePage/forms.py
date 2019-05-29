from django import forms
from django.contrib.auth import get_user_model
from homePage.models import Comments, UserDetails

User = get_user_model()


class ContactForm(forms.Form):
    fullname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your Full Name',
                'id': 'form_fullname'
            }))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Email',
                'id': 'form_email'
            }))
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your Content Here',
                'id': 'form_content'
            }))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not 'gmail.com' in email:
            raise forms.ValidationError('Email has to be gmail.com')
        return email


class LoginForm(forms.Form):
    username = forms.CharField(label='', widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Username',
               'id': 'inputEmail',
               'autofocus': 'True'
               }))
    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'class': 'form-control',
               'placeholder': 'Password',
               'id': 'inputPassword',
               }))


class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'id': 'username'
        }))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'form_password'
        }))
    password2 = forms.CharField(label='Confirm Password',
                                widget=forms.PasswordInput(
                                    attrs={
                                        'class': 'form-control',
                                        'placeholder': 'Password',
                                        'id': 'password2'
                                    }))
    fullname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your Full Name',
                'id': 'form_fullname'
            }))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Email',
                'id': 'form_email'
            }))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError('Username is taken!')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError('Email already exist!')
        return email

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError('Passwords must match.')
        return data


YEARS = [x for x in range(1940, 2020)]
GENDER = [('male', 'Male'),
          ('female', 'Female'),
          ('others', 'Others'), ]


class AddDetailForm(forms.ModelForm):
    # dob = forms.DateField(widget=forms.SelectDateWidget(years=YEARS,
    #                                                     attrs={
    #                                                         'placeholder': 'DOB',
    #                                                   'id': 'dob'
    #                                                     }))
    # gender = forms.CharField(widget=forms.RadioSelect(choices=GENDER,
    #                                                   attrs={
    #                                                       'placeholder': 'Gender',
    #                                                       'id': 'gender'
    #                                                   }))
    # profile_pic = forms.ImageField()
    # cover_pic = forms.ImageField()

    class Meta:
        model = UserDetails
        fields = ['user_DOB', 'user_gender', 'user_profile_pic', 'user_cover_pic']


class PostForm(forms.Form):
    post = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'Post Something Here',
            'id': 'form_content',
            'rows': 2.5,
            'cols': 75
        }))


class CommentForm(forms.Form):
    Comment = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'Comment Here',
            'id': 'form_comment',
            'rows': 1,
            'cols': 75
        }))
