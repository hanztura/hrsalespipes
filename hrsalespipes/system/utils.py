import calendar

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from .models import Setting


def get_system_setting():
    return Setting.objects.first()


class DisplayDateFormatMixin:
    """Insert to the context the date format from settings
    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        system_setting = get_system_setting()
        context['display_date_format'] = system_setting.display_date_format

        return context


class PermissionRequiredWithCustomMessageMixin(PermissionRequiredMixin):
    permission_denied_message = 'Sorry you might not have the permission to \
        access this page. Please contact your administrator if you feel you \
        should be able to access this  page.'

    def handle_no_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:
            msg = self.get_permission_denied_message()
            context = {'permission_denied_message': msg}
            return render(self.request, 'system/403.html', context)
        return redirect_to_login(
            self.request.get_full_path(),
            self.get_login_url(),
            self.get_redirect_field_name()
        )


class ContextFromToMixin:
    is_default_date_from_year_beginning = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        today = timezone.localdate()
        last_day_of_the_month = calendar.monthrange(today.year, today.month)[1]
        self.month_first_day = str(today.replace(day=1))
        self.year_first_day = str(today.replace(day=1, month=1))
        self.month_last_day = str(today.replace(day=last_day_of_the_month))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        date_from = self.request.GET.get('from', self.month_first_day)
        if self.is_default_date_from_year_beginning:
            date_from = self.year_first_day

        date_to = self.request.GET.get(
            'to',
            self.month_last_day)
        context['from'] = date_from
        context['to'] = date_to
        return context


class FromToViewFilterMixin(ContextFromToMixin):
    paginate_by = 25

    def get_from_to_filter_expression(self, date_from, date_to):
        expression = Q(date__gte=date_from, date__lte=date_to)
        return expression

    def get_queryset(self):
        q = super().get_queryset()

        date_from = self.request.GET.get('from', '')
        if self.is_default_date_from_year_beginning:
            date_from = date_from if date_from else self.year_first_day
        else:
            date_from = date_from if date_from else self.month_first_day

        date_to = self.request.GET.get('to', '')
        date_to = date_to if date_to else self.month_last_day

        if date_from and date_to:
            try:
                q = q.filter(
                    self.get_from_to_filter_expression(date_from, date_to))
            except Exception as e:
                pass

        return q


class DateAndStatusFilterMixin(FromToViewFilterMixin):

    def get_queryset(self):
        q = super().get_queryset()

        # filter status
        # accepts one or more status
        status = self.request.GET.get('status', '')
        status = status.split(',') if status else []
        if status:
            q = q.filter(status_id__in=status)

        return q

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status'] = self.request.GET.get('status', '')
        return context


class ContextUrlBuildersMixin:
    context_urls_filter_fields = ('from', 'to')

    def get_context_urls(self):
        # pdf/excel buttons url builder
        context_urls = (
            ('pdf_url', reverse('reports:pdf_jobs_summary'), ),
            ('excel_url', reverse('reports:excel_jobs_summary'), ),
        )
        return context_urls

    def get_context_urls_filter_fields(self):
        return self.context_urls_filter_fields

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # pdf/excel buttons url builder
        urls = self.get_context_urls()
        filter_fields = self.get_context_urls_filter_fields()
        for name, url in urls:
            filter_string = [
                '{}={}'.format(
                    f, context.get(f, self.request.GET.get(
                        f, ''))) for f in filter_fields
            ]  # get from request if f is not in context
            filter_string = '&'.join(filter_string)
            filter_string = '?{}'.format(filter_string)
            context[name] = '{}{}'.format(url, filter_string)
        return context


class MonthFilterViewMixin:
    paginate_by = 25

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        today = timezone.localdate()
        self.month = today.strftime('%Y-%m')

    def get_queryset(self):
        q = super().get_queryset()

        month = self.request.GET.get('month', self.month)
        year, month = month.split('-')

        if month and year:
            try:
                q = q.filter(date__month=month, date__year=year)
            except Exception as e:
                pass

        return q

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        month = self.request.GET.get('month', self.month)
        context['month'] = month
        return context


CURRENCIES_CHOICES = (
    ('AFN', 'AFN'),
    ('EUR', 'EUR'),
    ('ALL', 'ALL'),
    ('DZD', 'DZD'),
    ('USD', 'USD'),
    ('AOA', 'AOA'),
    ('XCD', 'XCD'),
    ('ARS', 'ARS'),
    ('AMD', 'AMD'),
    ('AWG', 'AWG'),
    ('AUD', 'AUD'),
    ('AZN', 'AZN'),
    ('BSD', 'BSD'),
    ('BHD', 'BHD'),
    ('BDT', 'BDT'),
    ('BBD', 'BBD'),
    ('BYN', 'BYN'),
    ('BZD', 'BZD'),
    ('XOF', 'XOF'),
    ('BMD', 'BMD'),
    ('INR', 'INR'),
    ('BTN', 'BTN'),
    ('BOB', 'BOB'),
    ('BOV', 'BOV'),
    ('BAM', 'BAM'),
    ('BWP', 'BWP'),
    ('NOK', 'NOK'),
    ('BRL', 'BRL'),
    ('BND', 'BND'),
    ('BGN', 'BGN'),
    ('BIF', 'BIF'),
    ('CVE', 'CVE'),
    ('KHR', 'KHR'),
    ('XAF', 'XAF'),
    ('CAD', 'CAD'),
    ('KYD', 'KYD'),
    ('CLP', 'CLP'),
    ('CLF', 'CLF'),
    ('CNY', 'CNY'),
    ('COP', 'COP'),
    ('COU', 'COU'),
    ('KMF', 'KMF'),
    ('CDF', 'CDF'),
    ('NZD', 'NZD'),
    ('CRC', 'CRC'),
    ('HRK', 'HRK'),
    ('CUP', 'CUP'),
    ('CUC', 'CUC'),
    ('ANG', 'ANG'),
    ('CZK', 'CZK'),
    ('DKK', 'DKK'),
    ('DJF', 'DJF'),
    ('DOP', 'DOP'),
    ('EGP', 'EGP'),
    ('SVC', 'SVC'),
    ('ERN', 'ERN'),
    ('ETB', 'ETB'),
    ('FKP', 'FKP'),
    ('FJD', 'FJD'),
    ('XPF', 'XPF'),
    ('GMD', 'GMD'),
    ('GEL', 'GEL'),
    ('GHS', 'GHS'),
    ('GIP', 'GIP'),
    ('GTQ', 'GTQ'),
    ('GBP', 'GBP'),
    ('GNF', 'GNF'),
    ('GYD', 'GYD'),
    ('HTG', 'HTG'),
    ('HNL', 'HNL'),
    ('HKD', 'HKD'),
    ('HUF', 'HUF'),
    ('ISK', 'ISK'),
    ('IDR', 'IDR'),
    ('XDR', 'XDR'),
    ('IRR', 'IRR'),
    ('IQD', 'IQD'),
    ('ILS', 'ILS'),
    ('JMD', 'JMD'),
    ('JPY', 'JPY'),
    ('JOD', 'JOD'),
    ('KZT', 'KZT'),
    ('KES', 'KES'),
    ('KPW', 'KPW'),
    ('KRW', 'KRW'),
    ('KWD', 'KWD'),
    ('KGS', 'KGS'),
    ('LAK', 'LAK'),
    ('LBP', 'LBP'),
    ('LSL', 'LSL'),
    ('ZAR', 'ZAR'),
    ('LRD', 'LRD'),
    ('LYD', 'LYD'),
    ('CHF', 'CHF'),
    ('MOP', 'MOP'),
    ('MKD', 'MKD'),
    ('MGA', 'MGA'),
    ('MWK', 'MWK'),
    ('MYR', 'MYR'),
    ('MVR', 'MVR'),
    ('MRU', 'MRU'),
    ('MUR', 'MUR'),
    ('XUA', 'XUA'),
    ('MXN', 'MXN'),
    ('MXV', 'MXV'),
    ('MDL', 'MDL'),
    ('MNT', 'MNT'),
    ('MAD', 'MAD'),
    ('MZN', 'MZN'),
    ('MMK', 'MMK'),
    ('NAD', 'NAD'),
    ('NPR', 'NPR'),
    ('NIO', 'NIO'),
    ('NGN', 'NGN'),
    ('OMR', 'OMR'),
    ('PKR', 'PKR'),
    ('PAB', 'PAB'),
    ('PGK', 'PGK'),
    ('PYG', 'PYG'),
    ('PEN', 'PEN'),
    ('PHP', 'PHP'),
    ('PLN', 'PLN'),
    ('QAR', 'QAR'),
    ('RON', 'RON'),
    ('RUB', 'RUB'),
    ('RWF', 'RWF'),
    ('SHP', 'SHP'),
    ('WST', 'WST'),
    ('STN', 'STN'),
    ('SAR', 'SAR'),
    ('RSD', 'RSD'),
    ('SCR', 'SCR'),
    ('SLL', 'SLL'),
    ('SGD', 'SGD'),
    ('XSU', 'XSU'),
    ('SBD', 'SBD'),
    ('SOS', 'SOS'),
    ('SSP', 'SSP'),
    ('LKR', 'LKR'),
    ('SDG', 'SDG'),
    ('SRD', 'SRD'),
    ('SZL', 'SZL'),
    ('SEK', 'SEK'),
    ('CHE', 'CHE'),
    ('CHW', 'CHW'),
    ('SYP', 'SYP'),
    ('TWD', 'TWD'),
    ('TJS', 'TJS'),
    ('TZS', 'TZS'),
    ('THB', 'THB'),
    ('TOP', 'TOP'),
    ('TTD', 'TTD'),
    ('TND', 'TND'),
    ('TRY', 'TRY'),
    ('TMT', 'TMT'),
    ('UGX', 'UGX'),
    ('UAH', 'UAH'),
    ('AED', 'AED'),
    ('USN', 'USN'),
    ('UYU', 'UYU'),
    ('UYI', 'UYI'),
    ('UYW', 'UYW'),
    ('UZS', 'UZS'),
    ('VUV', 'VUV'),
    ('VES', 'VES'),
    ('VND', 'VND'),
    ('YER', 'YER'),
    ('ZMW', 'ZMW'),
    ('ZWL', 'ZWL'),
    ('XBA', 'XBA'),
    ('XBB', 'XBB'),
    ('XBC', 'XBC'),
    ('XBD', 'XBD'),
    ('XTS', 'XTS'),
    ('XXX', 'XXX'),
    ('XAU', 'XAU'),
    ('XPD', 'XPD'),
    ('XPT', 'XPT'),
    ('XAG', 'XAG'),
)
