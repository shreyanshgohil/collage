from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
    class Meta: 
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']

    
    def __init__(self,*args,**kwargs):
        super(CreateUserForm,self).__init__(*args,**kwargs)
    
        for name,field in self.fields.items():
                field.widget.attrs.update({'class':'form-control'})
            