from urllib import response
from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.response import Response

from apps.teachers.models import Teacher

from apps.students.models import Assignment, ASSIGNMENT_STATE_CHOICES, GRADE_CHOICES
from .serializer import TeacherAssignmentSerializer


class TeacherAssignmentsView(generics.ListCreateAPIView):
    serializer_class = TeacherAssignmentSerializer

    """Returns the List of Assignments assiciated with a particular Teacher"""
    def get(self, request, *args, **kwargs):

        #fetching all the assignment passing the query
        assignments = Assignment.objects.filter(teacher__user=request.user)

        return Response(
            data=self.serializer_class(assignments, many=True).data,
            status=status.HTTP_200_OK
        )


    def patch(self, request, *args, **kwargs):

        #Verify if there is a content sent by Teacher (Teacher's are not allowed to update content)
        if 'content' in request.data:
            return Response(
                data={"non_field_errors": ["Teacher cannot change the content of the assignment"]},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        #Check if the request body has the student id.
        if 'student' in request.data:
            return Response(
                data={"non_field_errors": ["Teacher cannot change the student who submitted the assignment"]},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            #fetching the assignment haveing the id same as passed in Payload
            assignment = Assignment.objects.get(id = request.data['id'])

            #Fetch teacher_id from the database.
            request.data['teacher_id'] = Teacher.objects.get(user=request.user).id


            #Check if the assignment is associated with the same Teacher or not.
            if request.data['teacher_id'] != assignment.teacher.id:
                return Response(
                    data={'non_field_errors': ['Teacher cannot grade for other teacher''s assignment']},
                    status=status.HTTP_400_BAD_REQUEST
                )

            #Check if the Assignment is still in DRAFT state
            if assignment.state == ASSIGNMENT_STATE_CHOICES[0][1]:
                return Response(
                    data={"non_field_errors": ["SUBMITTED assignments can only be graded"]},
                    status=status.HTTP_400_BAD_REQUEST
                )

            #Check if the passed grade is valid or not.
            if (request.data.get('grade') and not any(request.data.get('grade') in i for i in GRADE_CHOICES)):
                return Response(
                    data={'grade': ['is not a valid choice.']},
                    status=status.HTTP_400_BAD_REQUEST
                )

            #Check if the assignment is already been GRADED
            if assignment.state == ASSIGNMENT_STATE_CHOICES[2][1]:
                return Response(
                    data={"non_field_errors": ["GRADED assignments cannot be graded again"]},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Assignment.DoesNotExist:
            return Response(
                data={'non_field_errors': ['Assignment does not exist/permission denied']},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.serializer_class(assignment, data=request.data, partial=True)

        #If no erros, update the data
        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

