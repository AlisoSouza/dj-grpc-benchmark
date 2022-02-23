openssl req -newkey rsa:4096 \
            -x509 \
            -sha256 \
            -days 3650 \
            -nodes \
            -out djgrpc.crt \
            -keyout djgrpc.key \

cp djgrpc.crt client/
cp djgrpc.key client/
cp djgrpc.crt server/
cp djgrpc.key server/

