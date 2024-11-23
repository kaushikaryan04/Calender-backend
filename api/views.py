from django.shortcuts import render
from .models import Event , User
from rest_framework import generics, status 
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegistrationSerializer , EventSerializer
from rest_framework.permissions import AllowAny , IsAuthenticated
from django.shortcuts import get_object_or_404

class RegisterUserView(generics.CreateAPIView) :
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self , request ) : 
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response({"Success" : "Now you can login"})



# class EventView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Event
#     serializer_class = EventSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         # return self.queryset.objects.filter(user = self.request.user)
#         return Event.objects.filter(user=self.request.user)

class EventListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        events = Event.objects.filter(user=request.user)
        print(events.count())
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def post(self, request):
        request.data['user'] = request.user.id
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class EventDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, event_id, user):
        try:
            return Event.objects.get(id=event_id, user=user)
        except Event.DoesNotExist:
            return None

    def get(self, request, event_id):
        event = self.get_object(event_id, request.user)
        if not event:
            return Response({"error": "Event not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def put(self, request, event_id):
        event = self.get_object(event_id, request.user)
        if not event:
            return Response({"error": "Event not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = EventSerializer(event, data=request.data, partial=True)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, event_id):
        event = self.get_object(event_id, request.user)
        if not event:
            return Response({"error": "Event not found."}, status=status.HTTP_404_NOT_FOUND)
        event.delete()
        return Response({"message": "Event deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
