from django import forms

from .models import Status

# this form model can also be directly used on views
class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = [
            'user',
            'context',
            'image',
        ]

    # validates data to ensure cdontent and image are required
    def clean(self,*args,**kwargs):
        data = self.cleaned_data

        context = data.get('context',None)
        if context == "":
            context = None

        image = data.get('image', None)

        if context is None and image is None:
            raise forms.ValidationError("Content or image is required")

        return super().clean(*args,**kwargs)

    # if we want to validate a single field eg context
    def clean_context(self,*args,**kwargs):
        context = self.cleaned_data.get('context')

        if len(context) > 100:
            raise forms.ValidationError("Status Content is too long")
        return context
