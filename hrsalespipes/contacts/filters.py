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

    class Meta:
        model = Candidate
        fields = {
            'name': ['icontains', ],
            'candidate_owner_id': ['in', ],
            'current_previous_company': ['icontains', ]
        }

    def languages_filter(self, queryset, name, value):
        languages = value
        languages = languages.split(',') if languages else []
        if languages:
            # multiple or expressions
            filter_expression = Q()
            for language in languages:
                filter_expression |= Q(languages__icontains=language.strip())

            queryset = queryset.filter(filter_expression)

        return queryset

    def positions_filter(self, queryset, name, value):
        positions = value
        positions = positions.split(',') if positions else []
        if positions:
            # multiple or expressions
            filter_expression = Q()
            for position in positions:
                filter_expression |= Q(current_previous_position__icontains=position.strip())

            queryset = queryset.filter(filter_expression)

        return queryset

    def nationalities_filter(self, queryset, name, value):
        nationalities = value
        nationalities = nationalities.split(',') if nationalities else []
        if nationalities:
            # multiple or expressions
            filter_expression = Q()
            for nationality in nationalities:
                filter_expression |= Q(
                    nationality__icontains=nationality.strip())

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
