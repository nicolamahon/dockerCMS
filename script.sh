curl -s -X GET -H 'Accept: application/json' http://35.205.85.250:8080/containers | python3 -mjson.tool
#curl -s -X GET -H 'Accept: application/json' http://35.205.85.250:8080/containers?state=running | python3 -mjson.tool
#curl -s -X GET -H 'Accept: application/json' http://35.205.85.250:8080/containers/635d2d467002 | python3 -mjson.tool
#curl -s -X GET -H 'Accept: application/json' http://35.205.85.250:8080/containers/12cca45831fd/logs | python3 -mjson.tool
#curl -s -X GET -H 'Accept: application/json' http://35.205.85.250:8080/services
#curl -s -X GET -H 'Accept: application/json' http://35.205.85.250:8080/nodes
#curl -X POST -H 'Content-Type: application/json' http://35.205.85.250:8080/containers -d '{"image": "lab5-todo-image"}' | python3 -mjson.tool
#curl -X PATCH -H 'Content-Type: application/json' http://35.205.85.250:8080/containers/b6cd8ea512c8 -d '{"state": "running"}' | python3 -mjson.tool
#curl -s -X GET -H 'Accept: application/json' http://35.205.85.250:8080/containers/b6cd8ea512c8 | python3 -mjson.tool
#curl -X PATCH -H 'Content-Type: application/json' http://35.205.85.250:8080/containers/b6cd8ea512c8 -d '{"state": "stopped"}' | python3 -mjson.tool
#curl -s -X GET -H 'Accept: application/json' http://35.205.85.250:8080/containers/b6cd8ea512c8 | python3 -mjson.tool
#curl -s -f -X DELETE -H 'Accept: application/json' http://35.205.85.250:8080/containers/b6cd8ea512c8 | python3 -mjson.tool
#curl -f -X DELETE -H 'Accept: application/json' http://35.205.85.250:8080/containers
#curl -s -X GET -H 'Accept: application/json' http://35.205.85.250:8080/images | python3 -mjson.tool
#curl -H 'Accept: application/json' -F file=@dockerfiles/sshd.Dockerfile http://35.205.85.250:8080/images
#curl -s -X PATCH -H 'Content-Type: application/json' http://35.205.85.250:8080/images/6b362a9f73eb -d '{"tag":"test:1.0"}' | python3 -mjson.tool
#curl -s -f -X DELETE -H 'Accept: application/json' http://35.205.85.250:8080/images/6b362a9f73eb | python3 -mjson.tool
#curl -f -X DELETE -H 'Accept: application/json' http://35.205.85.250:8080/images | python3 -mjson.tool