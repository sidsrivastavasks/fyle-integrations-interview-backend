from os import stat
from attr import attr
from rest_framework import serializers

from apps.students.models import Assignment, GRADE_CHOICES


class TeacherAssignmentSerializer(serializers.ModelSerializer):
    """
    Teacher Assignment serializer
    """
    class Meta:
        model = Assignment
        fields = '__all__'

    def validate(self, attrs):

        if (not any(attrs['grade'] in i for i in GRADE_CHOICES)):
            raise serializers.ValidationError(attr['grade'])
        
        if 'grade' in attrs and 'teacher' in attrs:
            attrs['state'] = 'GRADED'
        
        if self.partial:
            return attrs

        return super().validate(attrs)
