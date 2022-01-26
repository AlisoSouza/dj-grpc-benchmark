from django.contrib import admin
from django.urls import path
from grpc_server.proto import books_pb2_grpc
from books.services import BookService


def grpc_handlers(server):
    books_pb2_grpc.add_BookControllerServicer_to_server(BookService.as_servicer(), server)


urlpatterns = [
    path('admin/', admin.site.urls),
]
