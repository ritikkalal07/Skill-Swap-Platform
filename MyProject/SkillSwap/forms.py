# Create this file as: SkillSwap/forms.py

from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Skill, SkillExchange, Message, Review

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=False)
    
    class Meta:
        model = UserProfile
        fields = ['bio', 'location', 'phone', 'profile_picture', 'skills_offered', 'skills_wanted']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'skills_offered': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'e.g. Python, Web Development, Guitar'}),
            'skills_wanted': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'e.g. Spanish, Photography, Cooking'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
    
    def save(self, commit=True):
        profile = super().save(commit=commit)
        if commit:
            user = profile.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.save()
        return profile

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'category', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

class SkillExchangeForm(forms.ModelForm):
    provider = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Select the user you want to exchange skills with"
    )
    skill_offered = forms.ModelChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="What skill are you offering?"
    )
    skill_wanted = forms.ModelChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="What skill do you want to learn?"
    )
    
    class Meta:
        model = SkillExchange
        fields = ['provider', 'skill_offered', 'skill_wanted', 'description', 'scheduled_date', 'location']
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 4, 
                'class': 'form-control',
                'placeholder': 'Describe what you want to learn and what you can teach...'
            }),
            'scheduled_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Meeting location (optional)'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # Exclude the current user from provider choices
            self.fields['provider'].queryset = User.objects.exclude(id=user.id)

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Type your message here...'
            }),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(
                choices=[(i, f'{i} Star{"s" if i != 1 else ""}') for i in range(1, 6)],
                attrs={'class': 'form-control'}
            ),
            'comment': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Share your experience with this skill exchange...'
            }),
        }

class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search skills, users, or exchanges...'
        })
    )
    category = forms.ChoiceField(
        choices=[('', 'All Categories')] + Skill.CATEGORY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )