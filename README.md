# dj-grpc-benchmark

# Run server

```sh
cd server
```

Para escolher qual servidor vai ser executado edite o arquivo run.sh
  - gRPC server: `python server.py`
  - gGRPC server w/ `djangogrpcframework`: `python manage.py grpcrunserver`

```sh
docker-compose build
docker-compose up
```

## Run client

```sh
cd client
python client/client.py
```

## Diferenças de implementação

### Services

Não existem muitas diferenças na implementação do servicer,
segundo a própria documentação do framework uma classe Service é basicamente o mesmo
que utilizar uma interface servicer regular gerada no grpc.

**Sem o framework:**

<details>

```python
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

```

</details>

**Com o framework:**

<details>

```python
class BookService(generics.ModelService):
    queryset = Book.objects
    serializer_class = BookProtoSerializer

    def ListBook(self, request, context):
        start_year = request.start
        end_year = request.end

        if start_year and end_year:
            filter = Q(year__gte=start_year) & Q(year__lte=end_year)
            for book in self.queryset.filter(filter):
                yield BookResponse(
                    book_id=book.id,
                    author=book.author,
                    country=book.country,
                    language=book.language,
                    link=book.link,
                    pages=book.pages,
                    title=book.title,
                    year=book.year,
                )

        for book in self.queryset.all():
            yield BookResponse(
                book_id=book.id,
                author=book.author,
                country=book.country,
                language=book.language,
                link=book.link,
                pages=book.pages,
                title=book.title,
                year=book.year,
            )

```

</details>

### Runserver

O comando `python manage.py grpcrunserver` é basicamente o código do servidor da biblioteca grpc dentro de `BaseCommand` do django. Sendo assim numa possível troca seria necessário implementar um BaseCommand para o server dos projetos.

**Sem o framework:**

[`server.py`](https://github.com/AlisoSouza/dj-grpc-benchmark/blob/main/server/server.py)

<detail>

```python
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
```

</detail>

**Com o Framework:**

[`grpcrunserver.py`](https://github.com/fengsp/django-grpc-framework/blob/master/django_grpc_framework/management/commands/grpcrunserver.py)

<detail>

```python
    ...
    def run(self, **options):
        """Run the server, using the autoreloader if needed."""
        if self.development_mode:
            if hasattr(autoreload, "run_with_reloader"):
                autoreload.run_with_reloader(self.inner_run, **options)
            else:
                autoreload.main(self.inner_run, None, options)
        else:
            self.stdout.write((
                "Starting gRPC server at %(address)s\n"
            ) % {
                "address": self.address,
            })
            self._serve()

    def _serve(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=self.max_workers),
                             interceptors=grpc_settings.SERVER_INTERCEPTORS)
        grpc_settings.ROOT_HANDLERS_HOOK(server)
        server.add_insecure_port(self.address)
        server.start()
        server.wait_for_termination()
    ...
```

</detail>

### Serializer

No exemplo não foram utilizados `Serializers`

### Benchmark

Ambos os servers rodando num container limitado a 0.5 de um núcleo de um processador i5 e 128MB de ram.

Foi feito um disparo de 500 requisições no método `RetrieveBook` com `book_id` = 1 como parâmetro.

**Com o Framework:**

![com o framework](/imgs/com_framework.png)

**Sem o Framework:**

![sem o framework](/imgs/sem_framework.png)

