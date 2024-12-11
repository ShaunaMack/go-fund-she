from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from projects.models import Project, Pledge
from .serializers import CustomUserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserList(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class CustomUserDetail(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        if not request.user.is_superuser and request.user.pk != user.pk:
            return Response(
                {"403: Forbidden. You are not authorized to update this user."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = CustomUserSerializer(
            instance=user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        if not request.user.is_superuser and request.user.pk != user.pk:
            return Response(
                {"403: Forbidden. You are not authorized to delete this user."},
                status=status.HTTP_403_FORBIDDEN,
            )

        user.delete()
        return Response({"200: User deleted successfully"}, status=status.HTTP_200_OK)

class MeDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        projects = Project.objects.filter(owner=user)
        pledges = Pledge.objects.filter(supporter=user)

        project_data = [
            {
                "id": project.id,
                "title": project.title,
                "description": project.description,
                "goal": project.goal,
                "is_open": project.is_open,
                "date_created": project.date_created,
            }
            for project in projects
        ]

        pledge_data = [
            {
                "id": pledge.id,
                "amount": pledge.amount,
                "anonymous": pledge.anonymous,
                "comment": pledge.comment,
                "project": {
                    "id": pledge.project.id,
                    "title": pledge.project.title,
                },
            }
            for pledge in pledges
        ]

        return Response(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "projects": project_data,
                "pledges": pledge_data,
            }
        )
