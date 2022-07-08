from django.shortcuts import get_object_or_404, render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from .serializers import OrderCreationSerializer, OrderDetailSerializer, OrderStatusUpdateSerializer
from .models import Order
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema

User = get_user_model()

# Create your views here.

# class HelloOrdersView(generics.GenericAPIView):
#     def get(self, request):
#         return Response(data={"message":"Hello Orders"}, status=status.HTTP_200_OK)


class OrderCreateListView(generics.GenericAPIView):
    queryset = Order
    serializer_class = OrderCreationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


    @swagger_auto_schema(operation_summary="List all orders")
    def get(self, request):
        orders = Order.objects.all()
        serializer = self.serializer_class(instance=orders, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Create a new order")
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)

        user = request.user

        
        if serializer.is_valid():
            serializer.save(customer=user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(generics.GenericAPIView):
    serializer_class = OrderDetailSerializer
    queryset = Order
    permission_classes = [IsAdminUser]
    
    @swagger_auto_schema(operation_summary="Retrieve an order")
    def get(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        serializer = self.serializer_class(instance=order)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
 
    @swagger_auto_schema(operation_summary="Update an order by id")
    def put(self, request, order_id):
        data = request.data
        order = get_object_or_404(Order, pk=order_id)
       
        serializer = self.serializer_class(data=data, instance=order)

        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="Remove/Delete an order by id")
    def delete(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        order.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdateOrderStatus(generics.GenericAPIView):
    serializer_class = OrderStatusUpdateSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(operation_summary="Update order status")
    def put(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        data = request.data

        serializer = self.serializer_class(data=data, instance=order)

        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserOrdersView(generics.GenericAPIView):
    serializer_class = OrderDetailSerializer

    @swagger_auto_schema(operation_summary="Get all users for a user")
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)

        orders = Order.objects.all().filter(customer=user)
        serializer = self.serializer_class(instance=orders, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserOrderDetail(generics.GenericAPIView):
    serializer_class = OrderDetailSerializer

    @swagger_auto_schema(operation_summary="Get a user's specific order")
    def get(self, request, user_id, order_id):
        user = User.objects.get(pk=user_id)

        order = Order.objects.all().filter(customer=user).get(pk=order_id)
        serializer = self.serializer_class(instance=order)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
