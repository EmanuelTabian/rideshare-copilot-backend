from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ridecalc.models import CalculatorEntry

from .serializers import CalculatorEntrySerializer
from datetime import timedelta
from django.utils import timezone


# Create your views here.
class AddCalculatorEntry(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CalculatorEntrySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data)


class GetCalculatorEntries(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        calcentries = CalculatorEntry.objects.all().filter(user=request.user)
        serializer = CalculatorEntrySerializer(calcentries, many=True)
        return Response(serializer.data)

class GetRecentCalcultaorEntries(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        days =  request.data.get('days') # Default to 7 days if not provided
        if days not in [7, 30, 90]:
            return Response({"detail": "Invalid number of days. Must be 7, 30, or 90."}, status=400)

        time_threshold = timezone.now() - timedelta(days=days)
        calcentries = CalculatorEntry.objects.all().filter(user=request.user, pub_date__gte=time_threshold)
        serializer = CalculatorEntrySerializer(calcentries, many=True)
        return Response(serializer.data)

class UpdateCalculatorEntry(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, calcentry_id):
        calcentry = get_object_or_404(CalculatorEntry, pk=calcentry_id)

        if calcentry.user != request.user:
            return Response(
                {"detail": "You do not have permission to edit this entry."}
            )

        serializer = CalculatorEntrySerializer(
            calcentry, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class DeleteCalculatorEntry(APIView):
    def delete(self, request, calcentry_id):
        calcentry = get_object_or_404(CalculatorEntry, pk=calcentry_id)
        if calcentry.user != request.user:
            return Response(
                {"detail": "You do not have permission to delete this entry."}
            )

        calcentry.delete()

        return Response()
