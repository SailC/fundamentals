# Logging demo

This demo explains how to leverage ICP's logging stack to ship your application logs with two examples. Please refer to [ICP content playbook](http://icp-content-playbook.rch.stglabs.ibm.com/logging/) for more info.

The related code is under [icp-content-demos/logging-demo](https://github.ibm.com/watson-foundation-services/icp-content-demos/tree/master/logging-demo)

## Getting started (Option 1: Automatic log collection)
- The [`kubectl run`](https://kubernetes.io/docs/user-guide/kubectl/kubectl_run.md) line below will create a [nginx](https://registry.hub.docker.com/_/nginx/) [pods](https://kubernetes.io/docs/user-guide/pods.md) listening on port 80. It will also create a [deployment](https://kubernetes.io/docs/user-guide/deployments.md) named `my-nginx` to ensure that there are always two pods running.

```bash
kubectl run my-nginx --image=nginx --replicas=1 --port=80
```

- The nginx server ships the log directly to stdout/stderr
To see the logs, first you need to hit the nginx end point to generate logs.

```bash
kubectl port-forward <nginx-pod-name> 8000:80
```

- Open `localhost:8000` in your browser, and you can see the welcome page from nginx, a log entry will be generated at the same time.

- To check the logs via Kibana, go to `https://<icp cluster ip>:8443/kibana/` and search for `my-nginx`, you can see the log entries.

## Logging Data flow
Option 1: Automatic log collection
```
+-----+                      +---------------+                        +------------+
| App |---(stdout/stderr)--->| host log file |---(Filebeat daemon)--->|  Logstash  |
+-----+                      +---------------+                        +------------+
```
Option2: Using a Filebeat sidecar
```
+-----+                           +--------------------+                         +------------+
| App |---(store logs locally)--->| container log file |---(Filebeat sidecar)--->|  Logstash  |
+-----+                           +--------------------+                         +------------+
```

## References
- [ICP content playbook monitoring](http://icp-content-playbook.rch.stglabs.ibm.com/monitoring/)
- [ICP knowledge center](https://www.ibm.com/support/knowledgecenter/en/SSBS6K_2.1.0/manage_metrics/logging_elk.html)
