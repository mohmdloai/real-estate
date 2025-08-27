from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .models import Listing
from .serializers import ListingSerializer

class ManagingListingView(APIView):

    def get(self, request, format=None):
        try:
            user = request.user
            if not user.is_realtor:
                return Response({'error':'User has no permission to access'},status=status.HTTP_403_FORBIDDEN)
            slug = request.query_params.get('slug')
            if not slug:
                listing = Listing.objects.order_by('-created_at').filter(realtor = user.email)
                listing = ListingSerializer(listing, many=True)

                return Response({'listings': listing.data},
                                status=status.HTTP_200_OK) #wrapped ( .data ) within serialized
            if not Listing.objects.filter(
                realtor = user.email,
                slug = slug
            ).exists():
                return  Response({'error': 'Listing not found'},status=status.HTTP_404_NOT_FOUND)

            listing = Listing.objects.get(realtor=user.email, slug=slug)
            listing = ListingSerializer(listing)# no many as dict (like obj)... not a list like above
            return Response({'listing': listing.data},status=status.HTTP_200_OK)

        except:
            return Response({'error': 'O something went wrong while retrieving data!'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
                return Response({'error': 'Listing with this slug already exists !'},
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
                return Response({'error':'price must be integer!'},
                                status=status.HTTP_400_BAD_REQUEST)

            bedrooms = data['bedrooms']
            try:
                bedrooms = int(bedrooms)
            except:
                return Response({'error':'bedrooms must be integer!'},
                                status=status.HTTP_400_BAD_REQUEST)

            bathrooms = data['bathrooms']
            try:
                bathrooms = float(bathrooms)
            except:
                return Response({'error':'bathrooms must be floating point number!'},status=status.HTTP_400_BAD_REQUEST)

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


class ListingDetailView(APIView):
    def get(self, request, format=None):


        try:
            #==> /api/listing/detail?slug=the_slug_of_listing

            #- get the slug from req params

            slug = request.query_params.get('slug')

            if not slug:
                return Response({'error':'slug must be provided'},status=status.HTTP_400_BAD_REQUEST)

            if not Listing.objects.filter(slug=slug, is_published=True).exists():
                return Response({'error':'Listing not found!'},status=status.HTTP_404_NOT_FOUND)

            listing = Listing.objects.get(slug=slug, is_published=True)
            listing = ListingSerializer(listing)

            return Response({'listing':listing.data},status=status.HTTP_200_OK)
        except:
            return Response({'error':'Error while retrieving listing data!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ListingView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):


        try:
            # ==> check if there are published listings or not

            if not Listing.objects.filter(is_published=True).exists():
                return Response({'error':'No published listings found'},status=status.HTTP_404_NOT_FOUND)

            # ==> retrieve those published
            listings = Listing.objects.order_by('-created_at').filter(is_published=True)
            # many=True --> as a list
            listings = ListingSerializer(listings, many=True)

            return Response({'listings':listings.data},status=status.HTTP_200_OK)
        except:
            return Response({'error':'Something went wrong while retrieving listings !'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
