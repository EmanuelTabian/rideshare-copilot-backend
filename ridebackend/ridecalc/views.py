from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CalculatorEntrySerializer

# Create your views here.
class AddCalculatorEntry(APIView):
    def post(self, request):
        serializer = CalculatorEntrySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)