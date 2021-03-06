import django_filters

from django.db.models import Q
from django.utils import timezone
from django.contrib.humanize.templatetags.humanize import intcomma

from .models import Candidate


class CandidateFilter(django_filters.FilterSet):
    languages = django_filters.CharFilter(method='languages_filter')
    nationalities = django_filters.CharFilter(method='nationalities_filter')
    is_male = django_filters.CharFilter(method='is_male_filter')
    age_range = django_filters.CharFilter(method='age_range_filter')
    positions = django_filters.CharFilter(method='positions_filter')
    notice_period = django_filters.CharFilter(method='notice_period_filter')
    current_salary = django_filters.CharFilter(method='current_salary_filter')
    expected_salary = django_filters.CharFilter(method='expected_salary_filter')

    class Meta:
        model = Candidate
        fields = {
            'name': ['icontains', ],
            'candidate_owner_id': ['in', ],
            'current_previous_company': ['icontains', ],
            'visa_status_id': ['in', ],
        }

    @classmethod
    def filter_expression_multi_value_string(
            cls, field, value, expression='icontains', split=True):
        if split:
            values = value.split(',') if value else []
        else:
            values = value if value else []

        if values:
            # multiple or expressions
            filter_expression = Q()
            for val in values:
                lookup = '{}__{}'.format(field, expression)
                filter_expression |= Q(**{
                    lookup: val.strip()
                })

        return filter_expression

    def notice_period_filter(self, queryset, name, value):
        return queryset if not value else queryset.filter(
            self.filter_expression_multi_value_string('notice_period', value))

    def languages_filter(self, queryset, name, value):
        return queryset if not value else queryset.filter(
            self.filter_expression_multi_value_string('languages', value))

    def positions_filter(self, queryset, name, value):
        return queryset if not value else queryset.filter(
            self.filter_expression_multi_value_string(
                'current_previous_position', value))

    def nationalities_filter(self, queryset, name, value):
        return queryset if not value else queryset.filter(
            self.filter_expression_multi_value_string('nationality', value))

    def is_male_filter(self, queryset, name, value):
        is_male = value
        is_male = is_male.split(',') if is_male else []
        if is_male:
            # multiple or expressions
            filter_expression = Q()
            possible_values = {
                'None': None,
                'true': True,
                'false': False
            }
            for value in is_male:
                filter_expression |= Q(
                    is_male=possible_values[value])

            queryset = queryset.filter(filter_expression)

        return queryset

    def age_range_filter(self, queryset, name, value):
        age_range = value
        age_range = age_range.split(',') if age_range else []
        if age_range and age_range != ['0', '100']:
            today = timezone.localdate()
            oldest_year = today.year - int(age_range[1])  # oldest
            youngest_year = today.year - int(age_range[0])  # youngest
            oldest_dob = today.replace(day=1, month=1, year=oldest_year)
            youngest_dob = today.replace(day=31, month=12, year=youngest_year)
            queryset = queryset.filter(
                date_of_birth__range=(oldest_dob, youngest_dob))

        return queryset

    def current_salary_filter(self, queryset, name, value):
        if value.find(','):
            value = [value.replace(',', ''), value]
        else:
            try:
                value = [value, intcomma(value, use_l10n=False)]
            except Exception as e:
                value = None

        return queryset if not value else queryset.filter(
            self.filter_expression_multi_value_string(
                'current_previous_salary',
                value,
                'contains',  # expression
                False,  # split
            ))

    def expected_salary_filter(self, queryset, name, value):
        if value.find(','):
            value = [value.replace(',', ''), value]
        else:
            try:
                value = [value, intcomma(value, use_l10n=False)]
            except Exception as e:
                value = None

        return queryset if not value else queryset.filter(
            self.filter_expression_multi_value_string(
                'expected_salary',
                value,
                'contains',  # expression
                False,  # split
            ))
