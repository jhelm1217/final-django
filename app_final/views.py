from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import *
from .serializers import *
import logging
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Q

# Create your views here.

@api_view(['POST'])
@permission_classes([])
def create_user(request):
  user = User.objects.create(
    username = request.data['username'],
  )
  user.set_password(request.data['password'])
  user.save()
  profile = Profile.objects.create(
    user = user,
    first_name = request.data['first_name'],
    last_name = request.data['last_name']
  )
  profile.save()
  profile_serialized = ProfileSerializer(profile)
  return Response(profile_serialized.data)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_friend(request, pk):
    username = request.data.get('username')
    trip = Trip.objects.get(pk=pk, user=request.user)  # only the authenticated user's trips can be modified
    if not trip:
        return Response({'error': 'Trip not found'}, status=status.HTTP_404_NOT_FOUND)

    friend = User.objects.filter(username=username).first()
    if not friend:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    trip.friends.add(friend)
    trip.save()
    serialized_trip = TripSerializer(trip)
    return Response(serialized_trip.data)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def send_join_request(request, trip_id):
#     trip = Trip.objects.get(pk=trip_id)
#     trip.pending_requests.add(request.user)
#     return Response({'message': 'Join request sent successfully'})

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def accept_join_request(request, trip_id, user_id):
#     trip = Trip.objects.get(pk=trip_id)
#     user = User.objects.get(pk=user_id)
#     trip.pending_requests.remove(user)
#     trip.accepted_participants.add(user)
#     return Response({'message': 'Join request accepted successfully'})

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def decline_join_request(request, trip_id, user_id):
#     trip = Trip.objects.get(pk=trip_id)
#     user = User.objects.get(pk=user_id)
#     trip.pending_requests.remove(user)
#     return Response({'message': 'Join request declined successfully'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_message(request):
    # user = User.objects.get(username=request.data['username']) 
    user = request.user
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!! ", request.data)
    message = Message.objects.create(
        user=user,
        content=request.data['content'],
        image=request.data['image'],
    )
    message.save()
    message_serialized = MessageSerializer(message)
    return Response(message_serialized.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def create_image(request):
  image_serialized = ImageSerializer(data=request.data)
  if image_serialized.is_valid():
    image_serialized.save()
    return Response(image_serialized.data, status=status.HTTP_201_CREATED )
  return Response(image_serialized.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_trip(request):
    user = request.user
    data = request.data.copy()  # Make a mutable copy of request.data
    data['created_by'] = user.pk  # Use 'created_by' to match serializer field
    data['user'] = user.pk

    trip_serialized = TripSerializer(data=data)
    if trip_serialized.is_valid():
        trip_serialized.save()
        return Response(trip_serialized.data, status=status.HTTP_201_CREATED)
    return Response(trip_serialized.errors, status=status.HTTP_400_BAD_REQUEST)




# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_trips(request):
#     user = request.user
#     user_trips = Trip.objects.filter(user=user)
#     # user_trips = Trip.objects.filter(friends=user)

#     serialized_trips = TripSerializer(user_trips, many=True)
#     return Response(serialized_trips.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_trips(request):
    user = request.user
    user_trips = Trip.objects.filter(Q(user=user) | Q(friends=user))
    
    serialized_trips = TripSerializer(user_trips, many=True)
    return Response(serialized_trips.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_completed_trips(request):
    user = request.user
    completed_trips = Trip.objects.filter(user=user, completed=True)
    serializer = TripSerializer(completed_trips, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_trips(request):
    user = request.user
    # Get trips where the user is the creator or a friend!
    user_trips = Trip.objects.filter(user=user) | Trip.objects.filter(friends__in=[user])
    serialized_trips = TripSerializer(user_trips, many=True)
    return Response

logger = logging.getLogger(__name__)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_trip(request, pk):
    logger.info(f"User {request.user} is attempting to update trip {pk}")

    trip = get_object_or_404(Trip, pk=pk, user=request.user)
    serializer = TripSerializer(trip, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        logger.info(f"Trip {pk} successfully updated by user {request.user}")
        return Response(serializer.data)
    
    logger.error(f"Validation errors: {serializer.errors} for user {request.user}")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_trip(request, pk):
    print(pk)
    trip = Trip.objects.filter(pk=pk, user=request.user).first()
    if trip:
        trip.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response({'error': 'Trip not found'}, status=status.HTTP_404_NOT_FOUND)




@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_message(request):
  message = Message.objects.get(id=request.data['id'])
  message.delete()
  return Response()

   

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_message(request, message_id):
    message = Message.objects.filter(id=message_id).first()
    
    message.content = request.data.get('content', message.content)
    message.save()
    message_serialized = MessageSerializer(message)
    return Response(message_serialized.data)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    user = request.user
    profile = user.profile
    serialized_profile = ProfileSerializer(profile, many=False)
    return Response(serialized_profile.data)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_trips(request):
#     user = request.user
#     user_trips = Trip.objects.filter(user=user)
#     serialized_trips = TripSerializer(user_trips, many=True)
#     return Response(serialized_trips.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_trips_detail(request, pk):
    user = request.user
    request.data['user'] = user.pk
    get_trips_detail = Trip.objects.all(Trip, pk=pk, user=request.user)
    serialized_trips = TripSerializer(get_trips_detail)
    return Response(serialized_trips.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_images(request):
  images = Image.objects.all()
  images_serialized = ImageSerializer(images, many=True)
  return Response(images_serialized.data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class MessageViewSet(viewsets.ModelViewSet):
   queryset = Message.objects.all()
   serializer_class = MessageSerializer


class ImageViewSet(viewsets.ModelViewSet):
   queryset = Image.objects.all()
   serializer_class = ImageSerializer


class TripViewSet(viewsets.ModelViewSet):
   queryset = Trip.objects.all()
   serializer_class = TripSerializer




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_messages(request):
    user = request.user
    messages = Message.objects.all()
    serialized_messages = MessageSerializer(messages, many=True)
    return Response(serialized_messages.data)