from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from .serializers import CustomUserSerializer

# /users


class CustomUserList(APIView):
    # GET method - retrieve all users
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)

    # POST method - create a new user
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

# /users/<pk>


class CustomUserDetail(APIView):

    # helper method for getting a user and raising a 404 if that user does not exist
    def get_object(self, pk):
        # try getting the user with the specified pk
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            # raise an Http404 exception so that Django knows to show a 404
            raise Http404

    # GET a single user's detail
    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    # PUT method – update user if the User has permission (authorization)
    def put(self, request, pk):
        user = self.get_object(pk)
        if not request.user.is_superuser and request.user.pk != user.pk:
            return Response({"403: Forbidden. You are not authorized to update this user."}, status=status.HTTP_403_FORBIDDEN)

        serializer = CustomUserSerializer(
            instance=user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE method – delete user if the User has permission (authorization)
    def delete(self, request, pk):
        user = self.get_object(pk)
        if not request.user.is_superuser and request.user.pk != user.pk:
            return Response({"403: Forbidden. You are not authorized to delete this user."}, status=status.HTTP_403_FORBIDDEN)

        user.delete()
        return Response({"200: User deleted successfully"}, status=status.HTTP_200_OK)


# /users/me

class MeDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
        })
