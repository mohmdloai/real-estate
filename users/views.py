from django.contrib.auth import get_user_model
User = get_user_model()# which is my custom user model
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response

from .serializers import UserSerializer

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):

        try:

            data = request.data

            name = data['name']
            email = data['email']
            password = data['password']
            re_password = data['re_password']
            is_realtor = data['is_realtor'] # => it returns a str


            if is_realtor == 'True':
                is_realtor =True
            else:
                is_realtor =False

            if password == re_password:
                if len(password) >=8:
                    if not User.objects.filter(email=email).exists():

                        if not is_realtor:
                            User.objects.create_user(name=name,email=email,password=password)
                            return Response(
                                {'success': 'User created successfully'},
                                status=status.HTTP_201_CREATED
                            )
                        else:
                            User.objects.create_realtor(name=name,email=email,password=password)
                            return Response(
                                {'success': 'Realtor created successfully'},
                                status=status.HTTP_201_CREATED
                            )

                    else:
                        return Response(
                        {'error': 'User already exists ! '},
                        status=status.HTTP_400_BAD_REQUEST
                )



                else:
                    return Response(
                    {'error': 'Password must be at least 8 characters! '},
                    status=status.HTTP_400_BAD_REQUEST
                )


            else:
                return Response(
                    {'error': 'Password don\'t match, Please retry again'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except:
            return Response(
                {'error':"Oh!, something went wrong while registering"},
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class RetrieveUserView(APIView):

    def get(self, request, format=None):
        try:
            #User always available = request.user (thanks to middleware)
            user = request.user # -> need to be serialized ...

            user = UserSerializer(user)

            return Response(
                {'user': user.data},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error':"Oh!, something went wrong while retrieving data"},
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )