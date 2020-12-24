build:
	python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/api.proto
buildgo:
	protoc -I protos --go_out=plugins=grpc:pkg/api protos/api.proto
buildjs:
	@echo "пока не готово"