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