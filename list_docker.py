from flask import Flask, request, abort, jsonify
from flask_cors import CORS  # Import the CORS extension
import docker
import json

app = Flask(__name__)
#CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

def get_container_info():
    hosts = ["192.168.1.187", "192.168.1.4"]
    container_info_list = []

    for host in hosts:
        remote_docker_host = "tcp://" + host + ":2375"
        client = docker.DockerClient(base_url=remote_docker_host)

        containers = client.containers.list(all=True)

        for container in containers:
            labels = container.labels
            for label, value in labels.items():
                if "webui" in label.lower():
                    if "unraid" in label.lower():
                        url = f"http://{host}:{value[18:].replace(']', '')}"
                    else:
                        url = f"http://{host}:{value}"
                    container_name = container.name
                    container_state = container.status  # Get the container state
                    container_info = {
                        "ContainerName": container_name,
                        "URL": url,
                        "State": container_state,
                        "Host": host
                    }
                    container_info_list.append(container_info)

        client.close()

    return container_info_list

def perform_container_action(container_name, action, host):
    #host = "192.168.1.187"  # Update with the actual host IP
    remote_docker_host = f"tcp://{host}:2375"
    
    client = docker.DockerClient(base_url=remote_docker_host)
    try:
        target_container = client.containers.get(container_name)
        
        if action == "stop":
            target_container.stop()
            response = {"message": f"Stopped container: {container_name}"}
        elif action == "start":
            target_container.start()
            response = {"message": f"Started container: {container_name}"}
        elif action == "restart":
            target_container.restart()
            response = {"message": f"Restarted container: {container_name}"}
        else:
            response = {"message": "Invalid action provided"}
    except docker.errors.NotFound:
        response = {"message": f"Container not found: {container_name}"}
    
    client.close()
    return response

@app.route('/containers', methods=['GET'])
def containers():
    container_info = get_container_info()
    return jsonify(container_info)

@app.route('/containers/<container_name>', methods=['POST'])
def post_container(container_name):
    data = request.get_json()
    action = data.get("action", "")
    host = data.get("host", "")

    # Check if the container exists
    container = next((c for c in get_container_info() if c["ContainerName"] == container_name), None)
    if container is None:
        abort(404)

    response = perform_container_action(container_name, action, host)
    
    return jsonify(response)


if __name__ == '__main__':
    app.run(host="192.168.1.187", debug=True, port=5008)
