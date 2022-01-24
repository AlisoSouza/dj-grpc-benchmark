import os
import grpc
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "base.settings")
django.setup()

from grpc_server.proto import books_pb2_grpc
from concurrent import futures
from books.models import Book


class BookService(
    books_pb2_grpc.BookControllerServicer
):
    queryset = Book.objects
    def ListBook(self, request, context):
        # return self.queryset.all()
        for book in self.queryset.all():
            yield book






    def CreateBook(self, request, context):
        return self.queryset.create(
            author = request.author,
            country = request.country,
            language = request.language,
            link = request.link,
            pages = request.pages,
            title = request.title,
            year = request.year,
        )

    def RetrieveBook(self, request, context):
        return self.queryset.get(id=request.book_id)
 


def serve():
    port = "[::]:50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    books_pb2_grpc.add_BookControllerServicer_to_server(
        BookService(), server
    )
    server.add_insecure_port(port)
    server.start()
    print(f"Running server on port {port}")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()