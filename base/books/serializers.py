from .models import Book
from django_grpc_framework import proto_serializers
from grpc_server.proto import books_pb2


class BookProtoSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = Book
        proto_class = books_pb2.BookResponse
        fields = [
            'id', 'author', 'country', 'language',
            'link', 'pages', 'title', 'year',
        ]
