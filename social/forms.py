from django import forms
from allauth.account.forms import SignupForm

class MySignupForm(SignupForm):
    first_name= forms.CharField(max_length=50,widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name= forms.CharField(max_length=50,required=False,widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    


    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        first_name=first_name[0].upper()+first_name[1:].lower()
        return first_name

    def clean_last_name(self):
        try:
            last_name = self.cleaned_data.get('last_name')
            last_name=last_name[0].upper()+last_name[1:].lower()
        except IndexError:
            pass
        else:
            return last_name


    def save(self, request):
   
        user = super(MySignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        return user



        # next_url = request.GET.get('redirect_field_name')
        # print(next_url)
        # print('here')
        # user.first_name = self.cleaned_data['first_name']
        # user.last_name = self.cleaned_data['last_name']
        # next_url = request.GET.get('redirect_field_name')
        # print(next_url)
        # print('here')
        # user.save()
        # return user
    