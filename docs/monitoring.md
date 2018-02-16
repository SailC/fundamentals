# Monitoring demo

This demo explains how to leverage ICP's monitoring stack by using statsd exporter to ship statsd metrics to ICP prometheus server to monitor the status of your applications. If your application is using other format of metrics other than statsd, please refer to [ICP content playbook](http://icp-content-playbook.rch.stglabs.ibm.com/monitoring/) for other alternatives.

The related code is under [icp-content-demos/monitoring-demo](https://github.ibm.com/watson-foundation-services/icp-content-demos/tree/master/monitoring-demo)

## Getting started

- clone repo
```
    git clone git@github.ibm.com:watson-foundation-services/icp-content-demos.git
    cd icp-content-demos
```

- build image & push image to icp docker registry
```
    docker build -t mycluster.icp:8500/default/olympus ./monitoring-demo/olympus-app
    docker pull prom/statsd-exporter:latest
    docker tag prom/statsd-exporter:latest mycluster.icp:8500/default/statsd-exporter:latest
    docker push mycluster.icp:8500/default/olympus:latest
    docker push mycluster.icp:8500/default/statsd-exporter:latest
```

- create k8s deployment and check if the pod is running
```
    //create deployment
    kubectl apply -f ./monitoring-demo/kube/olympus-app/deployment.yml
    // check pod is running
    kubectl get pod
    //you should see something like :
    // olympus-deployment-675455594b-rdxfh 2/2 Running 0 16s
```

- check the application end point and metrics end point locally
```
    //port forward your localhost port 8000 to the app server end point port.
    kubectl port-forward <podName> 8000:80
    //podName is the same as above

    open http://localhost:8000/hello in your browser
    // you should see 'hello world'

    //port forward your localhost port 9102 to the statsD exporter metrics port.
    kubectl port-forward <podName> 9102
    //podName something like olympus-deployment-675455594b-dg2l2

    open http://localhost:9102/metrics in your browser
    // you should see prometheus metrics there including `hello_requests_total`
    // the value of this key indicates how many times you've hit `/hello` end point
```

- enable Prometheus scraping by exposing metrics end point as a k8s service
```
    //expose metric endpoint as a service for Prometheus server to scrape
    kubectl apply -f ./monitoring-demo/kube/olympus-app/metrics-service.yaml
```

- check the metrics scraped by the ICP Prometheus server
```
    //port forward your localhost port 9090 to ICP prometheus server UI endpoint
    //note that the exact prometheus server name is different on your ICP cluster
    //use "kubectl get pod -n kube-system" to check the pod name
    kubectl port-forward -n kube-system monitoring-prometheus-5dd997d76b-jbqt6 9090

    open http://localhost:9090/targets
    // you should see http://10.1.242.142:9102/metrics being UP in kubernetes-service-endpoints
    // which means the app metrics is now being cralwed by prometheus server

    open http://localhost:9090/graph?g0.range_input=1h&g0.expr=hello_requests_total&g0.tab=0
    // you should see app metrics being visualized by Prometheus simeple built-in UI

    open http://localhost:9090/graph?g0.range_input=1h&g0.expr=hello_requests_total&g0.tab=1e
    and you can see the query statement in the console tab.
```

- create a new graphana dashboard and copy & paste the same query statement to the graph
and you should be able to see the metrics in the UI.

## Metrics Data flow
```
+----------+                         +-------------------+                        +--------------+
|  StatsD  |---(UDP/TCP repeater)--->|  statsd_exporter  |<---(scrape /metrics)---|  Prometheus  |
+----------+                         +-------------------+                        +--------------+
```
- Our Django application sends StatsD metrics to statsd_exporter daemon. We [deploy](https://github.ibm.com/watson-foundation-services/icp-content-demos/blob/master/monitoring-demo/kube/olympus-app/deployment.yml) our Django application wtih statsd_exporter running in the same K8s Pod. It exposes 8000 (uWSGI) and 9102 (statsd_exporter's generated Prometheus metrics) container ports.
- We enable Prometheus scraping by exposing metrics end point as a k8s [service](https://github.ibm.com/watson-foundation-services/icp-content-demos/blob/master/monitoring-demo/kube/olympus-app/metrics-service.yaml) with the annotation: `prometheus.io/scrape: 'true'`.
- The metrics will be scraped by the Prometheus server and you can check ICP's graphana dashboard to query the exposed metrics.

## References
- [Instrumenting Django with Prometheus and StatsD](http://marselester.com/django-prometheus-via-statsd.html)
- [StatsD to Prometheus metrics exporter](https://github.com/prometheus/statsd_exporter)
- [ICP content playbook monitoring](http://icp-content-playbook.rch.stglabs.ibm.com/monitoring/)
