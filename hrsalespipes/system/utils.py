import calendar
import datetime

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import render


class PermissionRequiredWithCustomMessageMixin(PermissionRequiredMixin):
    permission_denied_message = 'Sorry you might not have the permission to \
        access this page. Please contact your administrator if you feel you \
        should be able to access this  page.'

    def handle_no_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:
            context = {
                'permission_denied_message': self.get_permission_denied_message()
            }
            return render(self.request, 'system/403.html', context)
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())


class FromToViewFilterMixin:
    paginate_by = 25

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        today = datetime.date.today()
        last_day_of_the_month = calendar.monthrange(today.year, today.month)[1]
        self.month_first_day = str(today.replace(day=1))
        self.month_last_day = str(today.replace(day=last_day_of_the_month))

    def get_queryset(self):
        q = super().get_queryset()

        date_from = self.request.GET.get('from', self.month_first_day)
        date_to = self.request.GET.get('to', self.month_last_day)
        if date_from and date_to:
            try:
                q = q.filter(date__gte=date_from, date__lte=date_to)
            except Exception as e:
                pass

        return q

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        date_from = self.request.GET.get('from', self.month_first_day)
        date_to = self.request.GET.get(
            'to',
            self.month_last_day)
        context['from'] = date_from
        context['to'] = date_to
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
