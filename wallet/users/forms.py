from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()


class CreationForm(UserCreationForm):    
    class Meta(UserCreationForm.Meta):
        model = User        
        fields = ('first_name', 'last_name', 'username', 'email')   
    
    def clean(self):
        cleaned_data = super().clean()
        if User.objects.filter(email=cleaned_data.get('email')).exists():
            self.add_error('email', "Эта почта уже зарегестрированна")
        return cleaned_data