FROM golang:1.21-alpine as builder

WORKDIR /app
COPY . .

RUN go mod download
RUN go build -o operator .

FROM alpine:latest

WORKDIR /root/
COPY --from=builder /app/operator .
CMD ["main.go"]
