FROM golang:1.23-alpine AS build

WORKDIR /app

COPY go.mod .

RUN go mod download

COPY . .

RUN go build -o inventory-service .


FROM alpine:3.20

WORKDIR /app

COPY --from=build /app/inventory-service .

EXPOSE 3005

CMD ["./inventory-service"]