#!/bin/sh
cd $WORKDIR
python manage.py grpcrunserver --server-key djgrpc.key --server-crt djgrpc.crt
# python server.py
