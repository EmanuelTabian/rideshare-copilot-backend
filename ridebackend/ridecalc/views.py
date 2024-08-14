from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CalculatorEntrySerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from ridecalc.models import CalculatorEntry
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

    def get(self,request):
      calcentries = CalculatorEntry.objects.all().filter(user=request.user)
      serializer = CalculatorEntrySerializer(calcentries,many=True)
      return Response(serializer.data)
    
class UpdateCalculatorEntries(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, calcentry_id):
        calcentry = get_object_or_404(CalculatorEntry, pk=calcentry_id)

        if calcentry.user != request.user:
            return Response({"detail": "You do not have permission to edit this entry."})

        serializer = CalculatorEntrySerializer(calcentry, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
   

