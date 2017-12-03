# dockerCMS

Task is to build a container management system (DockerCMS) using a restful API that will manage containers, images, services and stacks by defining several routes for each task:

Available API endpoints:
		    0. EXIT
        1. GET /containers                      List all containers
        2. GET /containers?state=running        List running containers (only)
        3. GET /containers/<id>                 Inspect a specific container
        4. GET /containers/<id>/log             Dump specific container logs
        5. GET /services                        List all service
        6. GET /nodes                           List all nodes in the swarm
        7. POST /containers                     Create a new container
        8. PATCH /containers/<id>               Change a container's state
        9. DELETE /containers/<id>              Delete a specific container
        10. DELETE /containers                  Delete all containers (including running)
        11. GET /images                         List all images
        12. POST /images                        Create a new image
        13. PATCH /images/<id>                  Change a specific image's attributes
        14. DELETE /images/<id>                 Delete a specific image
        15. DELETE /images                      Delete all images

run the app.py file in a VM 
Command: python3 app.py

External IP: http://35.205.85.250:8080

run the python script to control the API
Command: python script.py

