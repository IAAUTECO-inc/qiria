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
mkdir -p services/core/api/gen
protoc --proto_path=api/proto \
       --go_out=services/core/api/gen --go_opt=paths=source_relative \
       --go-grpc_out=services/core/api/gen --go-grpc_opt=paths=source_relative \
       api/proto/qiria.proto

echo "Generating Python code..."
mkdir -p services/ui/api/gen
python -m grpc_tools.protoc --proto_path=api/proto \
       --python_out=services/ui/api/gen \
       --pyi_out=services/ui/api/gen \
       --grpc_python_out=services/ui/api/gen \
       api/proto/qiria.proto