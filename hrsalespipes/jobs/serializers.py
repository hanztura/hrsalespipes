from rest_framework import serializers

from .models import JobCandidate
from contacts.serializers import CandidateModelSerializer


class JobCandidateModelSerializer(serializers.ModelSerializer):
    candidate = CandidateModelSerializer(read_only=True)

    class Meta:
        model = JobCandidate
        fields = [
            'id',
            'job',
            'candidate',
        ]
