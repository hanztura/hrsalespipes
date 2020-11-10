import django_filters

from django.db.models import Q
from django.utils import timezone

from .models import Candidate


class CandidateFilter(django_filters.FilterSet):
    languages = django_filters.CharFilter(method='languages_filter')
    nationalities = django_filters.CharFilter(method='nationalities_filter')
    is_male = django_filters.CharFilter(method='is_male_filter')
    age_range = django_filters.CharFilter(method='age_range_filter')
    positions = django_filters.CharFilter(method='positions_filter')
    notice_period = django_filters.CharFilter(method='notice_period_filter')

    class Meta:
        model = Candidate
        fields = {
            'name': ['icontains', ],
            'candidate_owner_id': ['in', ],
            'current_previous_company': ['icontains', ],
            'visa_status_id': ['in', ],
        }

    @classmethod
    def filter_expression_multi_value_string(cls, field, value):
        values = value.split(',') if value else []
        if values:
            # multiple or expressions
            filter_expression = Q()
            for val in values:
                lookup = '{}__icontains'.format(field)
                filter_expression |= Q(**{
                    lookup: val.strip()
                })

        return filter_expression

    def notice_period_filter(self, queryset, name, value):
        return queryset if not value else queryset.filter(
            self.filter_expression_multi_value_string('notice_period', value))

    def languages_filter(self, queryset, name, value):
        if value:
            # multiple or expressions
            filter_expression = self.filter_expression_multi_value_string(
                'languages', value)

            queryset = queryset.filter(filter_expression)

        return queryset

    def positions_filter(self, queryset, name, value):
        if value:
            # multiple or expressions
            filter_expression = self.filter_expression_multi_value_string(
                'current_previous_position', value)

            queryset = queryset.filter(filter_expression)

        return queryset

    def nationalities_filter(self, queryset, name, value):
        if value:
            # multiple or expressions
            filter_expression = self.filter_expression_multi_value_string(
                'nationality', value)

            queryset = queryset.filter(filter_expression)

        return queryset

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
