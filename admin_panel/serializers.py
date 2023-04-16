from rest_framework import serializers

class PieceSerializerAll(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    date = serializers.IntegerField(min_value=1847, max_value=1885)
    genre = serializers.CharField(max_length=50)
    description = serializers.CharField(max_length=9999)


class PieceSerializerName(serializers.Serializer):
    name = serializers.CharField(max_length=100)

class PieceSerializerDesc(serializers.Serializer):
    description = serializers.CharField(max_length=9999)