from rest_framework import serializers
from .models import Project, Pledge


class PledgeSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    amount = serializers.IntegerField()
    comment = serializers.CharField(max_length=200)
    anonymous = serializers.BooleanField()
    supporter = serializers.CharField(max_length=200)
    project_id = serializers.IntegerField()

    # this will be called for POST /pledges to create a new pledge
    def create(self, validated_data):
        return Pledge.objects.create(**validated_data)


class ProjectSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=None)
    goal = serializers.IntegerField()
    image = serializers.URLField()
    is_open = serializers.BooleanField()
    date_created = serializers.DateTimeField()
    owner = serializers.CharField(max_length=200)
    # leaving the pledges out of list view so that we don't have to get
    # all of the pledges and all of the projects in one go
    # pledges = PledgeSerializer(many=True, read_only=True)

    # this will be called for POST /projects to create a new project

    def create(self, validated_data):
        return Project.objects.create(**validated_data)


class ProjectDetailSerializer(ProjectSerializer):
    # many=True tells the nested serializer to include a list of items
    # read_only=True means it's only used for GET, not PUT
    #   (which means you don't/can't provide pledges when updating a project)
    pledges = PledgeSerializer(many=True, read_only=True)
