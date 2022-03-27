FROM alpine:latest
RUN apk add --no-cache python3 py3-pip
RUN pip install webrcon websockets asyncio
COPY ./RustReboot.py /
ENTRYPOINT ["/usr/bin/python3", "/RustReboot.py"]
