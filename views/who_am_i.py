from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from kernel.managers.get_role import get_all_roles
from kernel.serializers.person import ProfileSerializer
from kernel.serializers.roles.student import StudentSerializer
from kernel.serializers.roles.faculty_member import FacultyMemberSerializer
from kernel.serializers.generics.contact_information import ContactInformationSerializer



class WhoAmI(GenericAPIView):
    """
    This view shows some personal information of the currently logged in user
    """

    permission_classes = [IsAuthenticated, ]
    serializer_class = ProfileSerializer

    def get(self, request, *args, **kwargs):
        """
        View to serve GET requests
        :param request: the request that is to be responded to
        :param args: arguments
        :param kwargs: keyword arguments
        :return: the response for request
        """

        person = request.person
        roles = get_all_roles(person)
        try:
            contact_information = person.contact_information.get()
        except:
            contact_information = None

        user = None
        if "Student" in roles:
            user = StudentSerializer(
                person.student
            ).data
        elif "FacultyMember" in roles:
            user = FacultyMemberSerializer(
                person.facultymember
            ).data

        contact_information = ContactInformationSerializer(
            contact_information
        ).data
        user['person']['contact_information'] = contact_information
        return Response(user, status=status.HTTP_200_OK)
