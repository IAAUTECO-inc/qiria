#!/bin/bash

# 🇬🇧 English:
# This script generates gRPC code for Go and Python from the .proto file.
#
# Prerequisites:
# 1. Install protoc: https://grpc.io/docs/protoc-installation/
# 2. Install Go plugins:
#    go install google.golang.org/protobuf/cmd/protoc-gen-go@v1.28
#    go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@v1.2
# 3. Install Python tools:
#    pip install grpcio-tools

# 🇫🇷 Français:
# Ce script génère le code gRPC pour Go et Python à partir du fichier .proto.
#
# Prérequis :
# 1. Installer protoc : https://grpc.io/docs/protoc-installation/
# 2. Installer les plugins Go :
#    go install google.golang.org/protobuf/cmd/protoc-gen-go@v1.28
#    go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@v1.2
# 3. Installer les outils Python :
#    pip install grpcio-tools

echo "Generating Go code..."
protoc --go_out=. --go_opt=paths=source_relative --go-grpc_out=. --go-grpc_opt=paths=source_relative qiria.proto

echo "Generating Python code..."
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. qiria.proto
