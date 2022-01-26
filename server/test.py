from urllib import response
from server import BookService
from grpc_server.proto.books_pb2 import BookCreateRequest, BookListRequest, BookRetrieveRequest


def test_list_books():
    service = BookService()
    request = BookListRequest()
    response = service.ListBook(request, None)
    assert len(list(response)) == 102

def test_retrieve_book():
    service = BookService()
    request = BookRetrieveRequest(book_id=5)
    response = service.RetrieveBook(request, None)
    assert response.id == 5

def test_create_book():
    service = BookService()
    request = BookCreateRequest(
        author = "Test Author",
        country = "Test country",
        language = "Test Language",
        link = "https://www.test.com",
        pages = 595,
        title = "Test Book",
        year = 2099,
    )
    response = service.CreateBook(request, None)

    assert response.title == 'Test Book'

def test_list_books_per_year():
    service = BookService()
    request = BookListRequest(start=600, end=2010)
    response = service.ListBook(request, None)
    print((next(response)))

# test_retrieve_book()
# test_list_books()
# test_create_book()
test_list_books_per_year()