from django import forms
from django.contrib.auth import get_user_model
from .models import Item, Image, File


class UserCreationForm(forms.ModelForm):
    password = forms.CharField()

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password', )

    def clean_password(self):
        password = self.cleaned_data.get("password")
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'category', 'tags', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),  # 説明用のテキストエリア
        }

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file']