from django.contrib import messages
from django.forms import ModelForm, ValidationError
from django.utils import timezone

from .models import Rate, Commission


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


class CommissionCreateModelForm(ModelForm):

    class Meta:
        model = Commission
        fields = [
            'employee',
            'rate_role_type',
            'rate_used',
            'amount',
        ]

    def __init__(self, *args, **kwargs):
        self.pipeline = kwargs.pop('pipeline')
        self.request = kwargs.pop('request')

        super().__init__(*args, **kwargs)

    def clean_rate_role_type(self):
        """Don't let create new record if role type exists
        for the pipeline
        """
        rate_role_type = self.cleaned_data['rate_role_type']
        commission = Commission.objects.filter(
            pipeline=self.pipeline, rate_role_type=rate_role_type)

        if commission.exists():  # don't allow
            msg = 'Commission already exists for the same Pipeline \
                   and role type.'
            messages.warning(self.request, msg)
            raise ValidationError(msg)

        return rate_role_type

    def is_valid(self):
        is_valid = super().is_valid()
        if is_valid:
            self.instance.pipeline = self.pipeline
            self.instance.date = timezone.localdate()

        return is_valid
