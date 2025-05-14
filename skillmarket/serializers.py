from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import InstructorProfile, StudentProfile, SkillClass, Booking

class InstructorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstructorProfile
        fields = '__all__'

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = '__all__'

class SkillClassSerializer(serializers.ModelSerializer):
    instructor = InstructorProfileSerializer(read_only=True)

    class Meta:
        model = SkillClass
        fields = '__all__'
        read_only_fields = ['instructor']
    
    def create(self, validated_data):
        request = self.context['request']
        instructor_profile = get_object_or_404(InstructorProfile, user=request.user)
        validated_data['instructor'] = instructor_profile
        return super().create(validated_data)

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'