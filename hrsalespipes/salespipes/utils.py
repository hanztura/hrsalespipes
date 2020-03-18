from commissions.helpers import create_commission


class CreateCommissionFormMixin:

    def save(self, commit=True):
        instance = super().save(commit)

        probability = instance.status.probability
        if commit and probability >= 1:  # if status 100%, create commission(s)
            create_commission(instance)

        return instance
