from rest_framework.generics import ListAPIView

from .models import JobCandidate
from .permissions import CustomDjangoModelPermissions
from .serializers import JobCandidateModelSerializer


class JobCandidateListAPIView(ListAPIView):
    queryset = JobCandidate.objects.all()
    serializer_class = JobCandidateModelSerializer
    permission_classes = [
        CustomDjangoModelPermissions
    ]
    filterset_fields = ['job', 'id']
