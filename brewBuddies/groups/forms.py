from django import forms
from .models import Group, Membership

class GroupForm(forms.ModelForm):
   class Meta:
       model = Group
       tags = forms.MultipleChoiceField(
           widget=forms.SelectMultiple,
           choices=[('beer', 'beer'), ('wine', 'wine'), ('whisky', 'whisky')]
       )
       fields = ['name', 'members', 'description', 'tags']
       

class JoinGroupForm(forms.Form):
   group_id = forms.IntegerField()
   name = forms.CharField()
   
class LeaveGroupForm(forms.Form):
   group_id = forms.IntegerField()
   name = forms.CharField()