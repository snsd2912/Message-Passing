kubectl exec --stdin --tty [pod-name] -- /bin/sh

kubectl exec --stdin --tty kafka-0 -- /bin/sh

kafka-topics --bootstrap-server kafka:29092 --topic [topic-name] --create --partitions [number] --replication-factor [number]

kafka-topics --bootstrap-server kafka:29092 --topic test --create --partitions 3 --replication-factor 3

helm install my-kafka bitnami/kafka --set auth.enabled=false --set service.type=NodePort

NAME: kafka-release
LAST DEPLOYED: Tue Oct  8 08:23:26 2024
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
CHART NAME: kafka
CHART VERSION: 30.1.5
APP VERSION: 3.8.0

** Please be patient while the chart is being deployed **

Kafka can be accessed by consumers via port 9092 on the following DNS name from within your cluster:

    kafka-release.default.svc.cluster.local

Each Kafka broker can be accessed by producers via port 9092 on the following DNS name(s) from within your cluster:

    kafka-release-controller-0.kafka-release-controller-headless.default.svc.cluster.local:9092
    kafka-release-controller-1.kafka-release-controller-headless.default.svc.cluster.local:9092
    kafka-release-controller-2.kafka-release-controller-headless.default.svc.cluster.local:9092

The CLIENT listener for Kafka client connections from within your cluster have been configured with the following security settings:
    - SASL authentication

To connect a client to your Kafka, you need to create the 'client.properties' configuration files with the content below:

security.protocol=SASL_PLAINTEXT
sasl.mechanism=SCRAM-SHA-256
sasl.jaas.config=org.apache.kafka.common.security.scram.ScramLoginModule required \
    username="user1" \
    password="$(kubectl get secret kafka-release-user-passwords --namespace default -o jsonpath='{.data.client-passwords}' | base64 -d | cut -d , -f 1)";

To create a pod that you can use as a Kafka client run the following commands:

    kubectl run kafka-release-client --restart='Never' --image docker.io/bitnami/kafka:3.8.0-debian-12-r5 --namespace default --command -- sleep infinity
    kubectl cp --namespace default /path/to/client.properties kafka-release-client:/tmp/client.properties
    kubectl exec --tty -i kafka-release-client --namespace default -- bash

    PRODUCER:
        kafka-console-producer.sh \
            --producer.config /tmp/client.properties \
            --broker-list kafka-release-controller-0.kafka-release-controller-headless.default.svc.cluster.local:9092,kafka-release-controller-1.kafka-release-controller-headless.default.svc.cluster.local:9092,kafka-release-controller-2.kafka-release-controller-headless.default.svc.cluster.local:9092 \
            --topic test

    CONSUMER:
        kafka-console-consumer.sh \
            --consumer.config /tmp/client.properties \
            --bootstrap-server kafka-release.default.svc.cluster.local:9092 \
            --topic test \
            --from-beginning

WARNING: There are "resources" sections in the chart not set. Using "resourcesPreset" is not recommended for production. For production installations, please set the following values according to your workload needs:
  - controller.resources
+info https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
