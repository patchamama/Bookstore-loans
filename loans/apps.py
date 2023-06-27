from django.apps import AppConfig


class LoansConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'loans'

    def ready(self):
        from .models import Loan
        from django.utils import timezone
        from django.db.models import Q

        qsearch = Q(Q(expire__lt=timezone.now()) & Q(status__lt=2))
        loans = Loan.objects.filter(qsearch)
        if loans.count() > 0:
            for loan in loans:
                print(loan)
                if loan.status == 1:
                    loan.status = 4
                    loan.save()

