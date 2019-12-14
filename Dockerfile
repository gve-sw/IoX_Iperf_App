FROM alpine:3.7
RUN apk add --no-cache python3
RUN apk add --no-cache iperf3
COPY . /app
WORKDIR /app
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
CMD ["gunicorn","-b 0.0.0.0:5500", "app:app"]