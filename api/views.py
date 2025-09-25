from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Product, Cart
from .serializers import RegisterSerializer, UserSerializer, ProductSerializer, CartSerializer

# Register
class RegisterAPI(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

# Current User
class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

# Products
class ProductListAPI(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# Cart APIs
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404

class CartAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        return Response(CartSerializer(cart_items, many=True).data)

    def post(self, request):
        product_id = request.data.get("product_id")
        qty = int(request.data.get("quantity", 1))

        if not product_id:
            return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, id=product_id)

        cart, created = Cart.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart.quantity += qty
        cart.save()

        return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        cart_id = request.data.get("cart_id")
        Cart.objects.filter(id=cart_id, user=request.user).delete()
        return Response({"message": "Item deleted"})

class ClearCartAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        Cart.objects.filter(user=request.user).delete()
        return Response({"message": "Cart cleared"})