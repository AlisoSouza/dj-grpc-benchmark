# dj-grpc-benchmark

| Variable | Type | Default | Description |
|--|--|--|--|
|CERTIFICATE_GRPC_CRT|```string```|  ```None```|Caminho para o certificado ssl|
|CERTIFICATE_GRPC_KEY|```string```|  ```None```|Caminho para a key do certificado ssl|
|CERTIFICATE_GRPC_ROOT|```string```|  ```None```|Caminho para o root CA|

## [gerar certificado ssl](https://gist.github.com/fntlnz/cf14feb5a46b2eda428e000157447309)

certificados em `server/certificates`

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
python client/client.py host port certificate
```
