# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from .models import Booking, InstructorProfile, SkillClass, StudentProfile
from .serializers import BookingSerializer, SkillClassSerializer

User = get_user_model()
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Health check endpoint to verify the API is running.
    """
    return Response({"status": "deployed_ok"})

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get logged-in user profile details",
        responses={200: "User profile returned"}
    )
    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'email': user.email,
            'name': user.get_full_name() if user.get_full_name() else "Not set"
        })
    
class SkillClassListCreate(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=SkillClassSerializer)
    def post(self, request):
        user = request.user
        instructor_profile = get_object_or_404(InstructorProfile, user=user)
        data = request.data.copy()
        data['instructor'] = instructor_profile.id
        serializer = SkillClassSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        skills = SkillClass.objects.all()
        serializer = SkillClassSerializer(skills, many=True)
        return Response(serializer.data)


# --------------------- Booking ---------------------
class BookSkillClass(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['skill_class_id'],
        properties={
            'skill_class_id': openapi.Schema(type=openapi.TYPE_INTEGER),
        }
    ))
    def post(self, request):
        student_profile = get_object_or_404(StudentProfile, user=request.user)
        skill_class_id = request.data.get('skill_class_id')
        skill_class = get_object_or_404(SkillClass, id=skill_class_id)

        booking = Booking.objects.create(student=student_profile, skill_class=skill_class)
        return Response({"message": "Class booked successfully", "booking_id": booking.id})


class MyBookingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        student_profile = get_object_or_404(StudentProfile, user=request.user)
        bookings = Booking.objects.filter(student=student_profile)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)


# --------------------- Messaging (Dummy) ---------------------
class ChatMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Dummy response for chat feature, replace with real Message model if added later
        dummy_data = [
            {"from": "Instructor A", "to": request.user.email, "message": "Welcome to the class!"},
            {"from": request.user.email, "to": "Instructor A", "message": "Thanks!"},
        ]
        return Response(dummy_data)
