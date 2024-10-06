kubectl exec --stdin --tty [pod-name] -- /bin/sh

kubectl exec --stdin --tty kafka-0 -- /bin/sh

kafka-topics --bootstrap-server kafka:29092 --topic [topic-name] --create --partitions [number] --replication-factor [number]

kafka-topics --bootstrap-server kafka:29092 --topic test --create --partitions 3 --replication-factor 3

