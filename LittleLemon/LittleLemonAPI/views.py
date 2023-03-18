from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from .models import Order, MenuItem, Cart, OrderItem, Category
from .serializers import MenuItemSerializer, CartSerializer, OrderSerializer
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes, api_view
from django.contrib.auth.models import User, Group
from django.forms.models import model_to_dict
from .permissions import *
from rest_framework.response import Response


# @permission_classes([IsAuthenticated])
class MenuItemView(generics.ListAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price']
    filterset_fields = ['price']
    search_fields = ['title']

    def get_permissions(self):
       order = OrderItem.objects.get(pk=self.kwargs['pk'])
       if self.request.method == 'GET' and self.request.user == order.user:
           permission_classes = [IsAuthenticated]
       elif self.request.method == 'PUT' or self.request.method == 'DELETE':
           permission_classes = [IsAuthenticated, IsManager | IsAdminUser]
       else:
           permission_classes = [IsAuthenticated, IsDeliveryCrew | IsManager | IsAdminUser]
       return [permission() for permission in permission_classes]

    def get_queryset(self, *args, **kwargs):
        query = OrderItem.objects.filter(order_id=self.kwargs['pk'])
        return query

    def patch(self, request, *args, **kwargs):
        order = OrderItem.objects.get(pk=self.kwargs['pk'])
        order.status = not order.status
        order.save()
        return Response({'message': 'Status :' + str(order.status)}, status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        order = OrderItem.objects.get(pk=self.kwargs['pk'])
        order.delete()
        return Response({'message': 'Order deleted'}, status.HTTP_200_OK)


# @permission_classes([IsAuthenticated])
class SingleMenuItemView(generics.RetrieveAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

# Manger menu items view


# @permission_classes([IsAuthenticated])
@permission_classes([IsAdminUser])
class ManagerMenuItemView(generics.CreateAPIView, generics.ListAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        if(self.request.method == 'GET'):
            return []

        return [IsAdminUser()]


# @permission_classes([IsAuthenticated])
@permission_classes([IsAdminUser])
class ManagerSingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


# Create Cart Views.
class CartView(generics.ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

# Create Order Views.


class OrderView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return HttpResponse({"message":"Some secret message"})
    
@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([TenCallsPerMinute])
def throttle_check_auth(request):
    return HttpResponse({"message":"Successful"})

@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
	return Response({'message':'Only Manager should see this'})	

@api_view()(['POST'])
@permission_classes([IsAdminUser])
def managers(request):
    username = request.data['username']
    if username:
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name='manager')
        if request.method == 'POST':
            managers.user_set.add(user)
        elif request.method == 'DELETE':
            managers.user_set.remove(user)
        return Response({'message': "ok"})
    return Response({'message': "error"}, status.HTTP_400_BAD_REQUEST)
