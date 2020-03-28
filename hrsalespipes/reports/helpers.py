from django.utils import timezone


def get_successful_jobs_queryset(
        pipelines,
        date_from=None,
        date_to=None,
        consultant_pk='',
        industry=''):
    """Returns a queryset filtered by date from, date to, industry,
       and consultant.

       Requires a queryset of successful pipeline.

       Accepts all time records. from or to should be ALL
       then get all.
    """
    q = pipelines.filter(status__probability__gte=1)

    if date_to == 'ALL':
        # until today
        today = timezone.localdate()
        q = q.filter(invoice_date__lte=today)

    elif date_to:
        # until a certain date that is may not be today
        try:
            q = q.filter(invoice_date__lte=date_to)
        except Exception as e:
            pass

    if date_from == 'ALL':
        # from the beginning
        pass

    elif date_from:
        # from a certain point of time
        try:
            q = q.filter(invoice__gte=date_from)
        except Exception as e:
            pass

    # filter consultant (optional)
    if consultant_pk:
        q = q.filter(
            job_candidate__consultant_id=consultant_pk)

    # industry is charfield
    if industry:
        q = q.filter(job_candidate__job__client__industry=industry)

    return q
