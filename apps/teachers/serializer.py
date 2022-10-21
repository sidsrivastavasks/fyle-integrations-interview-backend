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

        #Updating the state from SUBMITTED to GRADED.
        if 'grade' in attrs:
            attrs['state'] = 'GRADED'
        
        if self.partial:
            return attrs

        return super().validate(attrs)
