from django.forms import ModelForm

from .models import Rate


class RateModelForm(ModelForm):

    class Meta:
        model = Rate
        fields = [
            'name',
            'straight_rate',
            'role_type',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['role_type'].required = True
