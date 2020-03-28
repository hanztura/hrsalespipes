from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

from commissions.helpers import create_commission
from .rules import is_allowed_to_view_or_edit_pipeline


class CreateCommissionFormMixin:

    def save(self, commit=True):
        instance = super().save(commit)

        probability = instance.status.probability
        if commit and probability >= 1:  # if status 100%, create commission(s)
            create_commission(instance)

        return instance


class IsAllowedToViewOrEditMixin:
    model_pk_kwarg = 'pk'
    redirect_to_single_object_url_pattern = 'salespipes:list'
    not_allowed_message = 'Sorry you are not an associate or consultant \
        of this record. You are not allowed to do this action.'

    def get_model_pk_kwarg(self):
        return self.model_pk_kwarg

    def get_model_object(self):
        """Get the Model's object.
        """
        object_pk = self._kwargs[self.get_model_pk_kwarg()]
        model_object = get_object_or_404(self.model, pk=object_pk)

        return model_object

    def get_rule_to_pass(self, user, instance):
        return is_allowed_to_view_or_edit_pipeline(user, instance)

    def redirect_to_if_not_allowed(self, model_object):
        """Redirect here. Override if needed"""
        return redirect(self.redirect_to_single_object_url_pattern)

    def dispatch(self, request, *args, **kwargs):
        """check if status is closed and redirect if not
           allowed to edit
        """
        self._kwargs = kwargs
        model_object = self.get_model_object()
        user = request.user
        if not self.get_rule_to_pass(user, model_object):
            messages.info(request, self.not_allowed_message)

            return self.redirect_to_if_not_allowed(model_object)

        return super().dispatch(request, *args, **kwargs)
