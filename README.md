# dj-grpc-benchmark

Requirements:

```sh
python = "^3.9"
Django = "2.2.17"
grpcio-tools = "^1.43.0"
djangorestframework = "^3.13.1"
djangogrpcframework = "^0.2.1"

```

## Run gRPC server

```sh
python base/server.py
```

## Run gGRPC server w/ `djangogrpcframework`

```sh
python base/manage.py grpcrunserver --dev
```

## Run client

```sh
python client/client.py
```