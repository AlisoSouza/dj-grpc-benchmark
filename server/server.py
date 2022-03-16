import os
import grpc
import django
import sys
from concurrent import futures
from grpc_reflection.v1alpha import reflection

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

from django.conf import settings
from grpc_server.proto import books_pb2_grpc, books_pb2
from books.models import Book
from django.db.models import Q


class BookService(
    books_pb2_grpc.BookControllerServicer
):
    queryset = Book.objects

    def ListBook(self, request, context):
        if request.start and request.end:
            filter = Q(year__gte=request.start) & Q(year__lte=request.end)
            for book in self.queryset.filter(filter):
                yield books_pb2.BookResponse(
                    book_id=book.id,
                    author=book.author,
                    country=book.country,
                    language=book.language,
                    link=book.link,
                    pages=book.pages,
                    title=book.title,
                    year=book.year,
                )

        else:
            for book in self.queryset.all():
                yield books_pb2.BookResponse(
                    book_id=book.id,
                    author=book.author,
                    country=book.country,
                    language=book.language,
                    link=book.link,
                    pages=book.pages,
                    title=book.title,
                    year=book.year,
                )

    def CreateBook(self, request, context):
        book = self.queryset.create(
            author=request.author,
            country=request.country,
            language=request.language,
            link=request.link,
            pages=request.pages,
            title=request.title,
            year=request.year,
        )
        return books_pb2.BookResponse(
            book_id=book.id,
            author=book.author,
            country=book.country,
            language=book.language,
            link=book.link,
            pages=book.pages,
            title=book.title,
            year=book.year,
        )

    def RetrieveBook(self, request, context):
        book = self.queryset.get(id=request.book_id)

        return books_pb2.BookResponse(
            book_id=book.id,
            author=book.author,
            country=book.country,
            language=book.language,
            link=book.link,
            pages=book.pages,
            title=book.title,
            year=book.year,
        )


def serve():
    port = "[::]:50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    books_pb2_grpc.add_BookControllerServicer_to_server(
        BookService(), server
    )
    SERVICE_NAMES = (
        books_pb2.DESCRIPTOR.services_by_name['BookController'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    server.add_insecure_port(port)
    server.start()
    print(f"Running server on port {port}")
    server.wait_for_termination()


def secure_serve():
    port = "[::]:50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    books_pb2_grpc.add_BookControllerServicer_to_server(
        BookService(), server
    )
    with open(settings.CERTIFICATE_GRPC_KEY, 'rb') as f:
        private_key = f.read()
    with open(settings.CERTIFICATE_GRPC_CRT, 'rb') as f:
        certificate_chain = f.read()
    with open(settings.CERTIFICATE_GRPC_ROOT, 'rb') as f:
        root_ca = f.read()
    server_credentials = grpc.ssl_server_credentials(
        ((private_key, certificate_chain), ),
        root_certificates=root_ca,
        require_client_auth=True)

    server.add_secure_port("[::]:50051", server_credentials)

    server.start()
    print(f"Running server on port {port}")
    server.wait_for_termination()


if __name__ == "__main__":
    if settings.CERTIFICATE_GRPC_CRT and settings.CERTIFICATE_GRPC_KEY:
        print("Secure")
        sys.stdout.flush()
        secure_serve()
    else:
        print("Insecure")
        sys.stdout.flush()
        serve()
