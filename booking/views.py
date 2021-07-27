from uuid import UUID

from django.db.models import Q
from rest_framework import status, exceptions
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from TicketVendor.settings import MAX_OCCUPANCY
from booking.models import Orders, Seat
from booking.serializers import OrderSerializer, SeatSerializer


class VacateApi(APIView):
    """
    This class will update the status of seats
    """

    def post(self, request, *args, **kwargs):
        seat_objects = Seat.objects.filter(SEATNUM=request.data['SEATNUM'])
        if seat_objects.exists() and seat_objects[0].status is True:
            seat = Seat.objects.get(pk=seat_objects[0].pk)
            seat.status = False
            seat.save()
            return Response("updated status", status=status.HTTP_200_OK)
        return Response("Seat not Found or Already vacant", status=status.HTTP_404_NOT_FOUND)


class OccupyApi(ListCreateAPIView):
    serializer_class = OrderSerializer
    queryset = Orders.objects.all()

    def get(self, request, **kwargs):
        return self.list(request)

    def perform_create(self, serializer):
        # It will check the free seats
        all_seats = Seat.objects.filter(status=False)
        if all_seats.exists():
            seat = Seat.objects.get(pk=all_seats[0].pk)
            seat.status = True
            seat.save()
        else:
            # if free slot not present raise exception
            raise NotFound(detail="All seats Resereved", code=404)
        serializer.save(seat=seat)

    def post(self, request, **kwargs):
        return self.create(request)


class GetInfoApi(GenericAPIView):

    def validate_uuid4(self, uuid_string):
        # This function checks the valid UUID
        try:
            val = UUID(uuid_string, version=4)
        except ValueError:
            return False

        return True

    def get_object(self, **kwargs):
        # Here key refers to the request data , it can be ticket id , person name or seat number
        key = kwargs['key']

        # First it tries to find the ticket using seat no and person name
        ticket = Orders.objects.filter(Q(seat__SEATNUM=key) | Q(person_name=key))
        if ticket.exists():
            return ticket[0]

        # It check if uuid is valid or not
        valid_uuid = self.validate_uuid4(key)
        if valid_uuid:
            ticket = Orders.objects.filter(ticket_id=key)
            if ticket.exists:
                return ticket[0]
        raise exceptions.NotFound(detail="No Result Found", code=404)

    def get(self, request, *args, **kwargs):
        ticket = self.get_object(**kwargs)
        serializer = OrderSerializer(instance=ticket)
        if serializer.is_valid:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddSeatApi(CreateModelMixin):
    serializer_class = SeatSerializer

    # this function will overwrite the default create Model mixin, We can even use the APIview class too.
    def create(self, request, *args, **kwargs):
        total_seat = Seat.objects.count()
        if total_seat > MAX_OCCUPANCY-1:
            return Response("Seat exceeds the MAX_OCCUPANCY", status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
