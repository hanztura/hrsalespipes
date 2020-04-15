from system.db import IsDeletedModelManager


class UnpaidCommissionManager(IsDeletedModelManager):
    def get_queryset(self):
        return super().get_queryset().filter(
            is_paid=False)
