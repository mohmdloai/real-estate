from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Listing


class ManagingListingView(APIView):

    def get(self, request, format=None):
        pass


    def post(self, request):
        try:
            user = request.user
            if not user.is_realtor:
                return Response({'error':'User has no permission to access'},status=status.HTTP_403_FORBIDDEN)# forbidden means logged in (auth), but with no permission to create listing.
            data = request.data

            title = data['title']
            address = data['address']

            slug = data['slug']
            if Listing.objects.filter(slug=slug).exists():
                Response({'error': 'Listing with this slug already exists !'},
                        status=status.HTTP_400_BAD_REQUEST
                        )

            city = data['city']
            state = data['state']
            zipcode = data['zipcode']
            description = data['description']
            price = data['price']
            try:
                price = int(price)
            except:
                return Response({'error':'price must be integer!'})

            bedrooms = data['bedrooms']
            try:
                bedrooms = int(bedrooms)
            except:
                return Response({'error':'bedrooms must be integer!'})

            bathrooms = data['bathrooms']
            try:
                bathrooms = float(bathrooms)
            except:
                return Response({'error':'bathrooms must be floating point number!'})

            if bathrooms <= 0 or bathrooms >= 10 :
                bathrooms = 1.0
            bathrooms = round(bathrooms, 1)

            sale_type = data['sale_type']
            if sale_type == 'FOR_RENT':
                sale_type = 'For Rent'
            else:
                sale_type = 'For Sale'

            home_type = data['home_type']
            if home_type == 'TOWNHOUSE':
                home_type = 'Townhouse'
            elif home_type == 'CONDO':
                home_type = 'Condo'
            else:
                home_type = 'House'

            main_photo = data['main_photo']

            photo_1 = data['photo_1']
            photo_2 = data['photo_2']
            photo_3 = data['photo_3']

            is_published = data['is_published']
            if is_published == 'True':
                is_published = True
            else:
                is_published = False


            Listing.objects.create(
                realtor = user.email,
                title = title,
                slug = slug,
                address = address,
                city = city,
                state = state,
                zipcode = zipcode,
                description = description,
                price = price,
                bathrooms = bathrooms,
                bedrooms = bedrooms,
                sale_type = sale_type,
                home_type = home_type,
                main_photo = main_photo,
                photo_1 = photo_1,
                photo_2 = photo_2,
                photo_3 = photo_3,
                is_published = is_published
            )

            return Response({"success":"Listing has created successfully"},
                        status=status.HTTP_201_CREATED)

        except:
            return Response({
                'error': 'Something went wrong while creating a listing, please try again! '
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #will be for a realtor -> must be authorized and authenticated.