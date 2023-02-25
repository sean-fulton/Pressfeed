from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import CheckboxSelectMultiple
from news.models import Source
from django import forms

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = "form-control"
        self.fields['password1'].widget.attrs['class'] = "form-control"
        self.fields['password2'].widget.attrs['class'] = "form-control"

class SubscriptionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['sources'] = forms.ModelMultipleChoiceField(
            queryset=Source.objects.all(),
            widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            label='',
            required=False,
        )

    def save(self):
        selected_sources = self.cleaned_data.get('sources', [])
        user_sources= UserSource.objects.filter(user=self.user)
        for source in user_sources:
            if source.source not in selected_sources:
                source.delete()
            else:
                selected_sources = selected_sources.exclude(pk=source.source.pk)
            for source in selected_sources:
                UserSource.objects.create(user=self.user, source=source)
