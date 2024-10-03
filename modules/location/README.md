- Install `grpc-io` with `pip install grpcio-tools`
- Install `grpcio` with `pip install grpcio`
- Using `grpcio-tools`, generate a pair of files that can be directly imported into our Python code:
```
python -m grpc_tools.protoc -I./ --python_out=./ --grpc_python_out=./ location.proto
```
The path `./`, can be replaced with another path or an absolute path to your `.proto` file.

The files `locaton_pb2.py` and `location_pb2_grpc.py` should have been generated.








