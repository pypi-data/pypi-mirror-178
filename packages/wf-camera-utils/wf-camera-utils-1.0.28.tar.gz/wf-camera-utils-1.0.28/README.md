# Camera-node

All software needed for a camera node in an environment. Includes pieces for both capture and delivery as well as proxy node that handles centralized processing of video, upload, and queuing in case of slow or down connectivity.

## Proxy

Flask service that receives data from all other camera nodes and feeds and internal queue and that sends data to honeycomb and optionally processes videos to pull out frames that are also sent to honeycomb.

## Capture

Service that runs on nodes that have cameras. Captures video clips in short segments and sends them to their internal queue where workers send the to the proxy.

## Workers

Celery service that performs tasks from the internal queue. Capture work is processed and sent to the proxy, unless it is a the proxy-node in which case it forwards the work to another task. Video segments are processes and sent to honeycomb. Processing includes tagging etc. Once uploaded the next set of processing happens, key frames are extracted at those are sent to honeycomb as child datapoint objects of the video.

If running on more capable hardware the keyframes could be evaluated for things like pose detection or object tracking. This is not planned yet but isn't out of scope specifically.

## Radio-Monitor

A python service that connects to a network of DWM1001 modules over BLE to collect data. That data is queued to be sent to honeycomb. It is expected that this service runs on the proxy node.

## CUWB-Stream

Leverages fluentd to move Ciholas sensor data to S3

Before deploying the service, update the Ciholas network config as follows:

|        | IP                | Port   | Interface           |
|--------|-------------------|--------|---------------------|
| Config | 239.255.76.67     | 7671   | <<CONTROL PC IP>>   |
| Input  | 239.255.76.67     | 7667   | <<CONTROL PC IP>>   |
| Output | 0.0.0.0           | 32222  | <<CONTROL PC IP>>   |

PS: In order to resolve an issue with the anchors disconnecting and not reconnecting, you may need to set the interface IPs of the Config and Input rows to the ethernet device's IP (Use `ifconfig`) 

### Build and push cuwb service

```
make build-cuwb-stream
```

### Deploy streaming service to k8

```
# Install envsubtr, on MacOS install through the gettext pkg
brew install gettext
brew link --force gettext 

# Create a config and secrets file with S3 and AWS ENV keys
kubectl apply -f ./k8s/kube-logging.yml
kubectl apply -f ./private/aws-s3-write-auth-config.yml
kubectl apply -f ./private/aws-s3-write-auth-secret.yml
kubectl apply -f ./k8s/fluentd.yml
kubectl apply -f ./k8s/fluentd-s3-config.yml
kubectl apply -f ./k8s/fluentd-s3.yml

TIMEZONE=US/Pacific envsubst < ./k8s/fluentd-s3-scheduler.yml | kubectl apply -f -

kubectl apply -f ./k8s/cuwb-service.yml 
```

### Test CUWB Steaming logger

See the [cdp_player README](./cuwb_stream/README.md#Test)

## CDP Player

You can use the Makefile to build or run the cdp-player. You can also [work with cdp-player directly](./cdp_player/README.md).

### Build

`make build-cdp-player REPO_NAME=<<Ciholas PPA Repository Name>>`

### Run 

`make run-cdp-player REPO_NAME=<<Ciholas PPA Repository Name>>`

## Setup cluster with Docker Hub robot

First login and then copy creds into the cluster:

    docker login
    # Provide username and PAT (personal access token)

    kubectl create secret generic regcred --from-file=.dockerconfigjson=/home/wildflowertech/.docker/config.json --type=kubernetes.io/dockerconfigjson


## Logz + Fluentd Experiment

    kubectl create namespace monitoring

    kubectl create secret generic logzio-logs-secret \
        --from-literal=logzio-log-shipping-token='<<REDACTED>>' \
        --from-literal=logzio-log-listener='https://listener.logz.io:8071' \
        -n monitoring

    # fluentd-general-config.yml contains the CLASSROOM_ENVIRONMENT env var
    kubectl apply -f ./private/fluentd-general-config.yml
    kubectl apply -f ./k8s/fluentd-general-config.yml -f ./k8s/fluentd-general-monitoring.yml
