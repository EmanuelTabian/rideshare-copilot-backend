from datetime import timedelta

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ridecalc.models import CalculatorEntry

from .serializers import CalculatorEntrySerializer


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

    # This API View will feature nearly the same Paginator mechanism as the GetAllRidePosts API View from ridebackend/ridecars/views.py but we'll use a query parameter instead of a positional argument.
    def get(self, request):
        calcentries = CalculatorEntry.objects.all().filter(user=request.user).order_by("-pub_date")
        page = request.query_params.get("page", 1)
        calc_entries_length = len(calcentries)
        paginator = Paginator(calcentries, 10)

        try:
            calc_entries_page = paginator.page(page)

        except PageNotAnInteger:
            return Response(
                {"error": "Invalid page number. Page should be an integer!"}
            )
        except EmptyPage:
            return Response(
                {
                    "error": "Page not found! The page number you're requesting is out of range!"
                }
            )
        calc_entries_by_page = calc_entries_page.object_list

        serializer = CalculatorEntrySerializer(calc_entries_by_page, many=True)

        pagination_details = {
            "current_page": calc_entries_page.number,
            "total_pages": paginator.num_pages,
            "has_previous": calc_entries_page.has_previous(),
            "has_next": calc_entries_page.has_next(),
            "previous_page_number": (
                calc_entries_page.previous_page_number()
                if calc_entries_page.has_previous()
                else None
            ),
            "next_page_number": (
                calc_entries_page.next_page_number()
                if calc_entries_page.has_next()
                else None
            ),
        }

        return Response(
            {
                "data": serializer.data,
                "count": calc_entries_length,
                "pagination": pagination_details,
            }
        )


class GetRecentCalculatorEntries(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        days = request.query_params.get("days", "7")
        if days is None or not days.isdigit() or int(days) not in [7, 30, 90]:
            return Response(
                {"detail": "Invalid number of days. Must be 7, 30, or 90."}, status=400
            )

        days = int(days)
        
        time_threshold = timezone.now() - timedelta(days=days)
        calcentries = CalculatorEntry.objects.all().filter(
            user=request.user, pub_date__gte=time_threshold
        ).order_by("pub_date")
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
