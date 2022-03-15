import sys
import grpc
from protos import books_pb2_grpc, books_pb2

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

def ssl_client(path, port, cert):
    with open(cert, 'rb') as f:
        creds = grpc.ssl_channel_credentials(f.read())
    channel = grpc.secure_channel(f'{path}:{port}', creds)
    stub = books_pb2_grpc.BookControllerStub(channel)
    response = stub.ListBook(
            books_pb2.BookListRequest(), None
        )
    print(f'[+] List books: {len(list(response))}')

if __name__ == "__main__":
    _ , host, port, cert = sys.argv
    ssl_client(host, port, cert)

    
