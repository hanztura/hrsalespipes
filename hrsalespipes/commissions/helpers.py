import datetime

from .models import Rate, Commission


def create_commission(pipeline):
    """"Create commission records based on a given Pipeline object."""

    rates = Rate.objects.all()
    commissions_created = []

    for rate in rates:
        rate_details = rate.details.all()

        # get commission computation base value and employee
        if rate.role_type == 'one':
            # lowest level / associate
            commission_base_amount = pipeline.invoice_amount
            employee = pipeline.job_candidate.associate

        elif rate.role_type == 'two':
            commission_base_amount = pipeline.potential_income
            employee = pipeline.job_candidate.candidate.candidate_owner

        elif rate.role_type == 'three':
            commission_base_amount = pipeline.invoice_amount
            employee = None

        else:
            commission_base_amount = pipeline.invoice_amount
            employee = None

        # get commission rate data
        if rate_details:
            commission_rate_type = 'percentage'
            commission_rate = 0
            for rate_detail in rate_details:
                _min = rate_detail.base_minimum
                _max = rate_detail.base_maximum
                is_within = _min <= commission_base_amount <= _max
                is_max_unli = _min <= commission_base_amount and _max == 0
                if is_within or is_max_unli:
                    commission_rate = rate_detail.rate_value
                    commission_rate_type = rate_detail.rate_value_type
                    break
        else:
            commission_rate_type = 'percentage'
            commission_rate = rate.straight_rate

        # compute commisison amount
        if commission_rate_type == 'percentage':
            commission_amount = commission_base_amount * commission_rate
        else:
            if commission_base_amount == 0:
                commission_amount = 0
            else:
                # amount
                commission_amount = commission_rate

        data = {
            'date': datetime.date.today(),
            'pipeline': pipeline,
            'employee': employee,
            'rate_used': commission_rate,
            'amount': commission_amount,
            'rate_role_type': rate.role_type,
        }

        commission, created = Commission.objects.update_or_create(
            pipeline=pipeline,
            rate_role_type=rate.role_type,
            defaults=data)
        commissions_created.append(commission)

    return commissions_created
