from rest_framework import serializers

from .models import Candidate


class CandidateModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = [
            'id',
            'name',
        ]
