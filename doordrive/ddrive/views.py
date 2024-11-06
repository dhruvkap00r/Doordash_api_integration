from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .Serializer  import UserSerializer
from rest_framework.views import APIView
from .main import *
import asyncio
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny 
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.views import (
  TokenObtainPairView,
  TokenRefreshView,
  token_obtain_pair
)
from .Serializer import *
import logging
logger = logging.getLogger("ddrive")


from rest_framework_simplejwt.tokens import AccessToken

#TODO: first we need to select a user before doing this step

token = jwt_token()



class CustomTokenObtainView(TokenObtainPairView):
  def get(request):

    pass


def get_user_from_token(request):
  auth_header = request.headers.get('Authorization')
  if not auth_header or not auth_header.startswith('Bearer '):
   raise AuthenticationFailed('Invalid or missing token')
  
  raw_token = auth_header.split(' ')[1]
  access_token_obj = AccessToken(raw_token)
  user = access_token_obj['user_id']
  user = User.objects.get(id=user)
  return user 

  """logger.error(ret)
  if ret.exists():
    return info
  else:
    return -1"""

class UserCreateView(generics.CreateAPIView):
  queryset = User.objects.all()
  permission_classes = [AllowAny]
  serializer_class = UserSerializer

  def create(self, request, *args, **kwargs):
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    address = request.data.get('address')
    phone_number = request.data.get('phone_number')
    username = request.data.get('username')
    password = request.data.get('password')

    if User.objects.filter(username=username).exists():
      return Response(
        {"error": "User already exists"},
        status=status.HTTP_400_BAD_REQUEST
      )
    if User.objects.filter(phone_number=phone_number).exists():
      return Response(
        {"error": "User already exists"},
        status = status.HTTP_400_BAD_REQUEST
      )

    #user = super().create(request, *args, **kwargs)
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()

    return Response(
      {f"hello {user.id}"}
    )
class UserInfoView(APIView):
  #in request there will only token
  permission_classes = [IsAuthenticated]
  queryset = User.objects.all()
  def get(self, request):
    #token = request.data.get('access token')
    user = get_user_from_token(request)
    if user == -1:
      Response(
        {"error": "User doesn't exists."},
        status = status.HTTP_400_BAD_REQUEST
      )
    else:
      user = {
        'first_name': user.first_name,
        'last_name' : user.last_name,
        'phone_number': user.phone_number,
        'address': user.address,
        'username': user.username
      }

      return Response(
        user,
        status = status.HTTP_200_OK)

def doorApiHandler(r,u):
  return API_Requests(r.business_name, r.address, r.phone_number, "say hello", "h-1212", u.address, u.phone_number, "afsf", u.first_name, u.last_name)

class DoorDashProxy(APIView):

  permission_classes = [IsAuthenticated]
  def post(self, request):

    user = get_user_from_token(request=request)
    dd_handler = doorApiHandler(Restaurant_info.objects.get(id=5),user)
    response = asyncio.run(dd_handler.create_quote())
    if response.status_code == 200:
      return Response(response.json(), status=status.HTTP_200_OK)
    else:
      return Response(response.json(), status=response.status_code)
    

class AcceptQuote(APIView):
  permission_classes = [IsAuthenticated]
  def post(self, request):
    dd_handler = API_Requests()
    user = get_user_from_token(request=request)
    delivery_id = request.data.get('delivery_id')
    if delivery_id is None or delivery_id == "null":
      return Response(
        request.headers
      )

    DeliveryInfo.objects.create(
      user = user,
      delivery_id = delivery_id,
      is_active = True,
      is_completed=False,
      refrence_tag="h-1212"
    )
    ret = asyncio.run(dd_handler.accept_quote(delivery_id)) 
    
    return Response(
      ret.json(), 
      status=status.HTTP_200_OK
    ) 

class GetStatus(APIView):
  def post(self,request):
    dd_handler = API_Requests()
    user = get_user_from_token(request=request)
    deliveries = DeliveryInfo.objects.filter(user__username=user.username)
    deliveries = deliveries.filter(is_active=True)
    serializer = DeliveryInfoSerializer(deliveries, many=True)
    
    update = asyncio.run(dd_handler.get_update(serializer.data[0]['delivery_id']))
    if update['delivery_data'] == "delivered":
      serializer.data[-1]['is_active'] = False
      serializer.data[-1]['is_completed'] = True

    return Response(
      update.json(),
      status=status.HTTP_200_OK
    )

from rest_framework_simplejwt.authentication import JWTAuthentication
class testView(APIView):
  permission_classes = [AllowAny]
  queryset = User.objects.all()
  def get(self, request):
    return Response({
      "token": "hellp"
    })

"""
{
  '(item_id)': '(count)'
}

"""
#Cart Operaton
class AddCartView(APIView):
  permission_classes = [IsAuthenticated]
  queryset = CartModel.objects.all()
  def post(self,request):
    itemId = request.data.get('itemId')
    itemCount = request.data.get('count')
    user = get_user_from_token(request)
    cart = CartModel.objects.create(itemId=itemId, itemCount=itemCount, user=user)
    cart.save()

class getCartView(APIView):
  permission_classes = [IsAuthenticated]
  queryset = CartModel.objects.all()
  def post(self,request):
    user = get_user_from_token(request)
    CartModel.objects.get(user=user)

class CheckoutView(APIView):
  permission_classes = [IsAuthenticated]
  queryset = CartModel.objects.all()
  def post(self,request):
    pass




class ListView(generics.ListAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = [AllowAny]


