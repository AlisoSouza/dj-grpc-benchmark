#!/bin/sh
cd $WORKDIR
if [ -z "$CERTIFICATE_GRPC_CRT" ] || [ -z "$CERTIFICATE_GRPC_KEY" ]
then
    echo Insecure channel
    python manage.py grpcrunserver
else
    echo Secure channel
    python manage.py grpcrunserver --server-key $CERTIFICATE_GRPC_KEY --server-crt $CERTIFICATE_GRPC_CRT
fi