```shell
# Command for generate private key as file jwt-private.pem size 2048 
openssl genrsa -out private.pem 2048

```shell
# Create public key based on private key, which verify that private key is correct
openssl rsa -in private.pem -outform PEM -pubout -out public.pem