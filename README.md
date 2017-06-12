# iot-thing_aws_gateway

simple MQTT forwarder, reads a message from a mqtt server and forwards it to AWS IoT

```
usage:
    -e, --endpoint aws IoT endpoint
    -r, --rootCA   root CA file path
    -c, --cert     certificate file path
    -k, --key      private key file path
    -t, --topic    topic, default: '*'
    -m, --mqtt     mqtt server, default: 127.0.0.1
    -p, --port     mqtt port, default: 1883
    -h, --help
```

## requirements
* Python 2 or 3
* AWSIoTPythonSDK ``pip install AWSIoTPythonSDK``
* paho-mqtt ``pip install paho-mqtt``

## docker
* mosquitto
```sh
docker run --rm -it -p 127.0.0.1:1883:1883 eclipse-mosquitto
```
* rabbitmq
```sh
docker run --rm -p 127.0.0.1:1883:1883 --name rabbitmq rabbitmq:3.6.10-alpine
docker exec -ti rabbitmq rabbitmq-plugins enable rabbitmq_mqtt
```
* gateway
```sh
docker run \
    --rm \
    -it \
    --net=host \
    -v ${CERTS_PATH}:/certs \
    my/gateway  -e ${AWSIOT_ENDPOINT} -t ${TOPIC} \
        -r /certs/root.pem \
        -c /certs/certificate.pem.crt \
        -k /certs/private.pem.key
```

