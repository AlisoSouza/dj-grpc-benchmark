from .models import Book
from django_grpc_framework import proto_serializers
from rest_framework import serializers
from grpc_server.proto import books_pb2


class CreateBookProtoSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = Book
        proto_class = books_pb2.BookResponse
        fields = '__all__'

class RetrieveBookRequestSerializer(proto_serializers.ProtoSerializer):
    book_id = serializers.IntegerField(required=True)

    def validate_book_id(self, value):
        try:
            Book.objects.get(id=value)
        except Book.DoesNotExist:
            raise serializers.ValidationError("This book does not exist")
        return value

    class Meta:
        proto_class = books_pb2.BookResponse

class ListBookRequestSerializer(proto_serializers.ProtoSerializer):
    start = serializers.IntegerField()
    end = serializers.IntegerField()

    class Meta:
        proto_class = books_pb2.BookResponse

