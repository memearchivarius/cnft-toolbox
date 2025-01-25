# syntax=docker/dockerfile:1

# Build the application from source
FROM golang:1.22 AS build-stage

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY .. .

RUN CGO_ENABLED=0 GOOS=linux go build -o /server cmd/server/main.go
RUN CGO_ENABLED=0 GOOS=linux go build -o /ctl cmd/ctl/main.go

FROM debian:12-slim AS build-release-stage

WORKDIR /

COPY --from=build-stage /server /server
COPY --from=build-stage /ctl /ctl

ENV PORT 8080

# Install CA certificates
RUN apt-get update && apt-get install -y ca-certificates

ENTRYPOINT ["/server"]