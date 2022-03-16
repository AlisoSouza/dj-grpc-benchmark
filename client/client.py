import os
import grpc
from dotenv import load_dotenv
from protos import books_pb2_grpc, books_pb2

# load environment variables
load_dotenv()

APP = os.getenv('APP')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
CERTIFICATE_GRPC_ROOT = os.getenv('CERTIFICATE_GRPC_ROOT')
CERTIFICATE_GRPC_CRT = os.getenv('CERTIFICATE_GRPC_CRT')
CERTIFICATE_GRPC_KEY = os.getenv('CERTIFICATE_GRPC_KEY')


def insecure_client(path, port):
    with grpc.insecure_channel(f"{path}:{port}") as channel:
        stub = books_pb2_grpc.BookControllerStub(channel)
        response = stub.ListBook(
            books_pb2.BookListRequest(start=605, end=1995), None
        )
        print(f'[+] List books per year: 605 to 1995: {len(list(response))}')
        response = stub.ListBook(
            books_pb2.BookListRequest(), None
        )
        print(f'[+] List books: {len(list(response))}')
        response = stub.RetrieveBook(
            books_pb2.BookRetrieveRequest(book_id=5), None
        )
        print(f'[+] Retrieve book id=5: {response}')
        response = stub.CreateBook(
            books_pb2.BookCreateRequest(
                author="Test Author",
                country="Test country",
                language="Test Language",
                link="https://www.test.com",
                pages=595,
                title="Test Book",
                year=605,
            )
        )
        print(f'[+] Create book: {response}')


def ssl_client():
    with open(CERTIFICATE_GRPC_CRT, 'rb') as f:
        client_cert = f.read()
    with open(CERTIFICATE_GRPC_KEY, 'rb') as f:
        client_key = f.read()
    with open(CERTIFICATE_GRPC_ROOT, 'rb') as f:
        server_cert = f.read()

    creds = grpc.ssl_channel_credentials(
        root_certificates=server_cert,
        private_key=client_key,
        certificate_chain=client_cert)

    channel = grpc.secure_channel(f'{HOST}:{PORT}', creds)
    stub = books_pb2_grpc.BookControllerStub(channel)
    response = stub.ListBook(
            books_pb2.BookListRequest(), None
        )
    print(f'[+] List books: {len(list(response))}')


if __name__ == "__main__":
    ssl_client()
