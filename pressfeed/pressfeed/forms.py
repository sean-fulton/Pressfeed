from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from django.forms.widgets import CheckboxSelectMultiple
from news.models import Source
from django import forms

User = get_user_model()

class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

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

class UsernameEditForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username']

    def __init__(self, *args, **kwargs):
        super(UsernameEditForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = "form-control"


class ChangePasswordForm(PasswordChangeForm):

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

        self.fields['old_password'].widget.attrs['class'] = "form-control"
        self.fields['new_password1'].widget.attrs['class'] = "form-control"
        self.fields['new_password2'].widget.attrs['class'] = "form-control"





