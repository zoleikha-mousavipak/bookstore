from rest_framework import serializers
from .models import *


class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=True, allow_blank=False, max_length=100)

    # insert
    def create(self, validated_data):
        return Book.objects.get(**validated_data)

    # edit
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title',instance.title)
        instance.save()
        return instance


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'birth', 'death']

