from flask import Flask, jsonify
from flask_cors import CORS
from kubernetes import client, config

app = Flask(__name__)
CORS(app)

# SAFE CONFIG LOADING
try:
    config.load_incluster_config()
except:
    config.load_kube_config()

v1 = client.CoreV1Api()
apps_v1 = client.AppsV1Api()


# ROOT (helps debugging)
@app.route('/')
def root():
    return jsonify({
        "message": "Backend is running"
    })


@app.route('/api')
def home():
    return jsonify({
        "message": "Kubernetes Dashboard Backend Running!"
    })


@app.route('/pods')
def get_pods():
    pods = v1.list_namespaced_pod(namespace="kubedeploy")

    pod_list = []
    for pod in pods.items:
        pod_list.append({
            "name": pod.metadata.name,
            "status": pod.status.phase
        })

    return jsonify(pod_list)


@app.route('/services')
def get_services():
    services = v1.list_namespaced_service(namespace="kubedeploy")

    service_list = []
    for svc in services.items:
        service_list.append({
            "name": svc.metadata.name,
            "type": svc.spec.type
        })

    return jsonify(service_list)


@app.route('/deployments')
def get_deployments():
    deployments = apps_v1.list_namespaced_deployment(namespace="kubedeploy")

    deploy_list = []
    for deploy in deployments.items:
        deploy_list.append({
            "name": deploy.metadata.name,
            "replicas": deploy.status.ready_replicas or 0
        })

    return jsonify(deploy_list)


@app.route('/health')
def health():
    return "OK"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)