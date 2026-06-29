from django.shortcuts import render

from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated , AllowAny

from .models import Candidate
from rest_framework import viewsets

from .models import Certification
from .serializers import CertificationSerializer



class DashboardAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        total_candidates = Candidate.objects.count()

        male_candidates = Candidate.objects.filter(gender="Male").count()

        female_candidates = Candidate.objects.filter(gender="Female").count()

        experienced_candidates = Candidate.objects.filter(
            experience__gt=0
        ).count()

        freshers = Candidate.objects.filter(
            experience=0
        ).count()

        experience_distribution = (
            Candidate.objects
            .values("experience")
            .annotate(count=Count("id"))
            .order_by("experience")
        )

        return Response({
            "total_candidates": total_candidates,
            "male_candidates": male_candidates,
            "female_candidates": female_candidates,
            "experienced_candidates": experienced_candidates,
            "freshers": freshers,
            "experience_distribution": experience_distribution,
        })
    


from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Certification
from .serializers import CertificationSerializer


class CertificationListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CertificationSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        canditate= Candidate.objects.first()
        return Certification.objects.filter(
            candidate__user=canditate.user
        ).order_by("-created_at")

    def perform_create(self, serializer):
        canditate= Candidate.objects.first()
        serializer.save(
            candidate=canditate
        )


class CertificationRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    serializer_class = CertificationSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        canditate= Candidate.objects.first()
        return Certification.objects.filter(
            candidate__user=canditate.user
        )