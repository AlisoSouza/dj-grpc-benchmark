# dj-grpc-benchmark

| Variable | Type | Default | Description |
|--|--|--|--|
|CERTIFICATE_GRPC_CRT|```string```|  ```None```|Caminho para o certificado ssl|
|CERTIFICATE_GRPC_KEY|```string```|  ```None```|Caminho para a key do certificado ssl|

## gerar certificado ssl

```sh
./generate_ssl_cert.sh
```

Gera o certificado em `client/` e em `server/`

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
python client/client.py secure
# insecure
python client/client.py insecure
```
