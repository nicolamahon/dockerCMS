from flask import Flask, Response, render_template, request
import json
from subprocess import Popen, PIPE
import os
from tempfile import mkdtemp
from werkzeug import secure_filename

app = Flask(__name__)

@app.route("/")
def index():
    return """

Available API endpoints:

1. GET /containers                     	List all containers
2. GET /containers?state=running       	List running containers (only)
3. GET /containers/<id>			Inspect a specific container
4. GET /containers/<id>/log		Dump specific container logs
5. GET /services			List all service
6. GET /nodes				List all nodes in the swarm
7. POST /containers			Create a new container
8. PATCH /containers/<id>              	Change a container's state
9. DELETE /containers/<id>		Delete a specific container
10. DELETE /containers                 	Delete all containers (including running)
11. GET /images				List all images
12. POST /images			Create a new image
13. PATCH /images/<id>			Change a specific image's attributes
14. DELETE /images/<id>			Delete a specific image
15. DELETE /images                     	Delete all images

"""




# LIST ALL CONTAINERS
@app.route('/containers', methods=['GET'])
def containers_index():
    """
    List all containers
    curl -s -X GET -H 'Accept: application/json' http://localhost:8080/containers | python -mjson.tool
    curl -s -X GET -H 'Accept: application/json' http://localhost:8080/containers?state=running | python -mjson.tool
    """
    if request.args.get('state') == 'running':
        output = docker('ps')
        resp = json.dumps(docker_ps_to_array(output))
    else:
        output = docker('ps', '-a')
        resp = json.dumps(docker_ps_to_array(output))
    return Response(response=resp, mimetype="application/json")


# INSPECT SPECIFIC CONTAINER
@app.route('/containers/<id>', methods=['GET'])
def containers_show(id):
    """
    Inspect specific container
    docker inspect returns json array so no need to convert
    curl -s -X GET -H 'Accept: application/json' http://localhost:8080/container/6992570b2e96 | python -mjson.tool
    """
    resp = docker('inspect', id)
    return Response(response=resp, mimetype="application/json")


# DUMP SPECIFIC CONTAINER LOG
@app.route('/containers/<id>/logs', methods=['GET'])
def containers_log(id):
    """
    Dump specific container logs
    curl -s -X GET -H 'Accept: application/json' http://localhost:8080/container/6992670b2e96/logs | python -mjson.tool
    """
    output = docker('logs', id).decode()
    resp = json.dumps(docker_logs_to_object(id, output))
    return Response(response=resp, mimetype="application/json")


# LIST ALL SERVICES
@app.route('/services', methods=['GET'])
def services_index():
    """
    List all containers
    curl -s -X GET -H 'Accept: application/json http://localhost:8080/services
    """
    resp = docker('service', 'ls')
    return Response(response=resp, mimetype="application/json")


# LIST ALL NODES IN THE SWARM
@app.route('/nodes', methods=['GET'])
def nodes_index():
    """
    List all containers
    curl -s -X GET -H 'Accept: application/json http://localhost:8080/nodes
    """
    resp = docker('node', 'ls')
    return Response(response=resp, mimetype="application/json")


# CREATE A CONTAINER
@app.route('/containers', methods=['POST'])
def containers_create():
    """
    Create container (from existing image using id or name)
    curl -X POST -H 'Content-Type: application/json' http://localhost:8080/containers -d '{"image": "lab5-image"}'
    curl -X POST -H 'Content-Type: application/json' http://localhost:8080/containers -d '{"image":"b14752a6590e"}'
    """
    body = request.get_json(force=True)
    image = body['image']
    if 'publish' in body:
        port = body['publish']
        id = docker('run', '-d', '-p', port, image)
    else:
        id = docker('run', '-d', image)
    id = id[0:12]
    return Response(response='{"id": "%s"}' % id, mimetype="application/json")


# UPDATE A CONTAINER'S STATE
@app.route('/containers/<id>', methods=['PATCH'])
def containers_update(id):
    """
    Update container attributes (support: state=running|stopped)
    curl -X PATCH -H 'Content-Type: application/json' http://localhost:8080/containers/b6cd8ea512c8 -d '{"state": "running"}'
    curl -X PATCH -H 'Content-Type: application/json' http://localhost:8080/containers/b6cd8ea512c8 -d '{"state": "stopped"}'

    """
    body = request.get_json(force=True)
    try:
        state = body['state']
        if state == 'running':
            docker('restart', id)
        if state == 'stopped':
            docker('stop', id)
    except:
        pass
    resp = '{"id": "%s"}' % id
    return Response(response=resp, mimetype="application/json")


# DELETE A SPECIFIC CONTAINER BY ID
@app.route('/containers/<id>', methods=['DELETE'])
def containers_remove(id):
    """
    Delete a specific container - must be already stopped/killed
    curl -s -X DELETE -H 'Accept: application/json' http://localhost:8080/containers/b6cd8ea512c8 | python -mjson.tool
    """
    docker('stop', id)
    docker('rm', '-f', id)
    resp = '{"id": "%s"}' % id
    return Response(response=resp, mimetype="application/json")


# FORCE REMOVE ALL CONTAINERS
@app.route('/containers', methods=['DELETE'])
def containers_remove_all():
    """
    Force remove all containers - dangerous!
    curl -X DELETE -H 'Accept: application/json' http://localhost:8080/containers | python -mjson.tool
    """
    output = docker('ps', '-a')
    list = docker_ps_to_array(output)
    idS = []
    for c in list:
        id = c['id']
        docker('stop', id)
        docker('rm', id)
        idS.append(id)
    resp = json.dumps(idS)
    return Response(response=resp, mimetype="application/json")


# LIST ALL IMAGES
@app.route('/images', methods=['GET'])
def images_index():
    """
    List all images
    curl -s -X GET -H 'Accept: application/json' http://localhost:8080/images | python -mjson.tool
    """
    output = docker('images')
    resp = json.dumps(docker_images_to_array(output))
    return Response(response=resp, mimetype="application/json")


# CREATE IMAGE FROM DOCKERFILE
@app.route('/images', methods=['POST'])
def images_create():
    """
    Create image (from uploaded Dockerfile)
    curl -H 'Accept: application/json' -F file=@dockerfiles/sshd.Dockerfile http://localhost:8080/images
    curl -H 'Accept: application/json' -F file=@dockerfiles/whale-say.Dockerfile http://localhost:8080/images
   """
    dockerfile = request.files['file']
    dirpath = mkdtemp()
    filename = secure_filename(dockerfile.filename)
    file_path = os.path.join(dirpath, filename)
    context_path = os.path.join(dirpath, '.')
    dockerfile.save(file_path)
    resp = docker('build', '-t', filename.lower(), '-f', file_path, context_path)
    return Response(response=resp, mimetype="application/json")


# UPDATE IMAGE ATTRIBUTE
@app.route('/images/<id>', methods=['PATCH'])
def images_update(id):
    """
    Update image attributes (support: name[:tag])  tag name should be lowercase $
    curl -s -X PATCH -H 'Content-Type: application/json' http://localhost:8080/images/6b362a9f73eb -d '{"tag":"test:1.0"}'
    """
    body = request.get_json(force=True)
    try:
        newTag = body['tag']
        docker ('tag', id, newTag)
    except:
        pass
    resp = '{"id": "%s"}' % id
    return Response(response=resp, mimetype="application/json")


# DELETE A SPECIFIC IMAGE BY ID
@app.route('/images/<id>', methods=['DELETE'])
def images_remove(id):
    """
    Delete a specific image
    curl -s -X DELETE -H 'Accept: application/json' http://localhost:8080/images/<id>
    """
    docker ('rmi', id)
    resp = '{"id": "%s"}' % id
    return Response(response=resp, mimetype="application/json")


# FORCE REMOVE ALL IMAGES
@app.route('/images', methods=['DELETE'])
def images_remove_all():
    """
    Force remove all images - dangerous!
    curl -X DELETE -H 'Accept: application/json' http://localhost:8080/images
    """
    output = docker('images')
    list = docker_images_to_array(output)
    idS = []
    for c in list:
        id = c['id']
        docker('rmi', id)
        idS.append(id)
    resp = json.dumps(idS)
    return Response(response=resp, mimetype="application/json")


#### Docker output parsing helpers ###

# for parsing the docker commands above
def docker(*args):
    cmd = ['docker']
    for sub in args:
        cmd.append(sub)
    process = Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    if stderr.startswith(b'Error'):
        print ('Error: {0} -> {1}'.format(' '.join(cmd), stderr))
    return stderr + stdout


# Parses the output of a Docker PS command to a python List
def docker_ps_to_array(output):
    all = []
    for c in [line.split() for line in output.splitlines()[1:]]:
        each = {}
        each['id'] = c[0].decode('utf-8')
        each['image'] = c[1].decode('utf-8')
        each['name'] = c[-1].decode('utf-8')
        each['ports'] = c[-2].decode('utf-8')
        all.append(each)
    return all


# Parses the output of a Docker logs command to a python Dictionary
# (Key Value Pair object)
def docker_logs_to_object(id, output):
    logs = {}
    logs['id'] = id
    all = []
    for line in output.splitlines():
        all.append(line)
    logs['logs'] = all
    return logs


# Parses the output of a Docker image command to a python List
#
def docker_images_to_array(output):
    all = []
    for c in [line.split() for line in output.splitlines()[1:]]:
        each = {}
        each['id'] = c[2].decode('utf-8')
        each['tag'] = c[1].decode('utf-8')
        each['name'] = c[0].decode('utf-8')
        all.append(each)
    return all


# main_method
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080, debug=True)
