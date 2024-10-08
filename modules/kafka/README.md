## Installation

### Install helm chart

If you haven't installed Helm yet, you can do so by following the official [Helm installation guide](https://helm.sh/docs/intro/install/).

### Add the Bitnami Repository

Bitnami provides a well-maintained Helm chart for Kafka. First, add the Bitnami repository:
```
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
```

### Install Kafka

You can install Kafka using the following command. This will install Kafka along with Zookeeper:

```
helm install my-kafka bitnami/kafka
```

Result you will get:

```
NAME: my-kafka
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

    my-kafka.default.svc.cluster.local

Each Kafka broker can be accessed by producers via port 9092 on the following DNS name(s) from within your cluster:

    my-kafka-controller-0.my-kafka-controller-headless.default.svc.cluster.local:9092
    my-kafka-controller-1.my-kafka-controller-headless.default.svc.cluster.local:9092
    my-kafka-controller-2.my-kafka-controller-headless.default.svc.cluster.local:9092

The CLIENT listener for Kafka client connections from within your cluster have been configured with the following security settings:
    - SASL authentication

To connect a client to your Kafka, you need to create the 'client.properties' configuration files with the content below:

security.protocol=SASL_PLAINTEXT
sasl.mechanism=SCRAM-SHA-256
sasl.jaas.config=org.apache.kafka.common.security.scram.ScramLoginModule required \
    username="user1" \
    password="$(kubectl get secret my-kafka-user-passwords --namespace default -o jsonpath='{.data.client-passwords}' | base64 -d | cut -d , -f 1)";

To create a pod that you can use as a Kafka client run the following commands:

    kubectl run my-kafka-client --restart='Never' --image docker.io/bitnami/kafka:3.8.0-debian-12-r5 --namespace default --command -- sleep infinity
    kubectl cp --namespace default /path/to/client.properties my-kafka-client:/tmp/client.properties
    kubectl exec --tty -i my-kafka-client --namespace default -- bash

    PRODUCER:
        kafka-console-producer.sh \
            --producer.config /tmp/client.properties \
            --broker-list my-kafka-controller-0.my-kafka-controller-headless.default.svc.cluster.local:9092,my-kafka-controller-1.my-kafka-controller-headless.default.svc.cluster.local:9092,my-kafka-controller-2.my-kafka-controller-headless.default.svc.cluster.local:9092 \
            --topic test

    CONSUMER:
        kafka-console-consumer.sh \
            --consumer.config /tmp/client.properties \
            --bootstrap-server my-kafka.default.svc.cluster.local:9092 \
            --topic test \
            --from-beginning

WARNING: There are "resources" sections in the chart not set. Using "resourcesPreset" is not recommended for production. For production installations, please set the following values according to your workload needs:
  - controller.resources
+info https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
```

### Verify the Installation

You can check the status of your Kafka installation by running:

```
kubectl get pods
```

[kafka](../../images/kafka.PNG)

### Uninstalling Kafka
If you ever need to uninstall Kafka, you can do so with the following command:

```
helm uninstall my-kafka
```


