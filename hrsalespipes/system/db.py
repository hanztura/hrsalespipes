# modules for model mixins
from django.db import models


class IsDeletedModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class IsDeletedAbstractModel(models.Model):
    """
    An abstract model base class with is_deleted field and the default
    queryset returns fields that are not deleted.

    delete() is overriden to not actually delete the record from the
    database but updates the is_deleleted field into True instead.
    """
    class Meta:
        abstract = True

    is_deleted = models.BooleanField(default=False, blank=True)

    objects = IsDeletedModelManager()
    base_objects = models.Manager()

    def delete(self, *args, **kwargs):
        """update is_delete into True"""
        assert self.pk is not None, (
            "%s object can't be deleted because its %s attribute is set to None." %
            (self._meta.object_name, self._meta.pk.attname)
        )

        if not self.is_deleted:
            self.is_deleted = True
            self.save(update_fields=['is_deleted'])

        return self
