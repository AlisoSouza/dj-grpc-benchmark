# dj-grpc-benchmark

## Server Environment Variables

| Variable | Type | Default | Description |
|--|--|--|--|
|CERTIFICATE_GRPC_CRT|```string```|  ```None```|Caminho para o certificado ssl|
|CERTIFICATE_GRPC_KEY|```string```|  ```None```|Caminho para a key do certificado ssl|
|CERTIFICATE_GRPC_ROOT|```string```|  ```None```|Caminho para o root CA|

<hr>

## Client Environment Variables

| Variable | Type | Default | Description |
|--|--|--|--|
|CERTIFICATE_GRPC_CRT|```string```|  ```None```|Caminho para o certificado ssl|
|CERTIFICATE_GRPC_KEY|```string```|  ```None```|Caminho para a key do certificado ssl|
|CERTIFICATE_GRPC_ROOT|```string```|  ```None```|Caminho para o root CA|
|HOST|```string```|  ```None```| Host |
|PORT|```string```|  ```None```| Port |

## [Gerar certificado ssl](https://gist.github.com/fntlnz/cf14feb5a46b2eda428e000157447309)

certificados em `server/certs` e `client/certs`

## Run server

```sh
cd server
docker-compose up --build
```

> Caso as variáveis de ambiente não sejam configuradas o servidor irá iniciar uma conexão insegura.

## Run client

```sh
cd client
# ssl 
python client.py
```
