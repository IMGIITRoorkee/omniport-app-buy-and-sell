from itertools import chain

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from kernel.managers.get_role import get_all_roles
from kernel.serializers.person import ProfileSerializer
from kernel.serializers.roles.student import StudentSerializer
from kernel.serializers.roles.faculty_member import FacultyMemberSerializer
from kernel.serializers.generics.contact_information import ContactInformationSerializer

from buy_and_sell.models import SaleProduct, RequestProduct



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
        is_phone_visible = False
        sale_product = SaleProduct.objects.filter(person= person)
        request_product = RequestProduct.objects.filter(person= person)
        all_results = list(chain(sale_product, request_product))
        for product in all_results:
            if(product.is_phone_visible == True):
                is_phone_visible=True
                break
        user['is_phone_visible'] = is_phone_visible
        user['person']['contact_information'] = contact_information
        return Response(user, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        """
        View to serve POST requests
        :param request: the request that is to be responded to
        :param args: arguments
        :param kwargs: keyword arguments
        :return: the response for request
        """

        person = request.person
        try:
            phone_status = request.data['phone_status']
            sale_product = SaleProduct.objects.filter(person= person)
            request_product = RequestProduct.objects.filter(person= person)
            all_results = list(chain(sale_product, request_product))
            for product in all_results :
                if(phone_status == "true"):
                    product.is_phone_visible = True
                    product.save()
                elif(phone_status == "false"):
                    product.is_phone_visible = False
                    product.save()
            return Response(data={
                        'phone_status': 'phone status successfully changed.'
                        }, status=status.HTTP_200_OK)
        except:
            return Response(data={
                        'error': 'phone status was not changed due to some error.'
                        }, status=status.HTTP_400_BAD_REQUEST)
