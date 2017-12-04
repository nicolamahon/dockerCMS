# dockerCMS

Task is to build a container management system (DockerCMS) using a restful API that will manage containers, images, services and stacks by defining several routes for each task:
<br><br>
Available API endpoints:<br><br>
	0. EXIT					Exit script.py<br>
        1. GET /containers                      List all containers<br>
        2. GET /containers?state=running        List running containers (only)<br>
        3. GET /containers/<id>                 Inspect a specific container<br>
        4. GET /containers/<id>/log             Dump specific container logs<br>
        5. GET /services                        List all service<br>
        6. GET /nodes                           List all nodes in the swarm<br>
        7. POST /containers                     Create a new container<br>
        8. PATCH /containers/<id>               Change a container's state<br>
        9. DELETE /containers/<id>              Delete a specific container<br>
        10. DELETE /containers                  Delete all containers (including running)<br>
        11. GET /images                         List all images<br>
        12. POST /images                        Create a new image<br>
        13. PATCH /images/<id>                  Change a specific image's attributes<br>
        14. DELETE /images/<id>                 Delete a specific image<br>
        15. DELETE /images                      Delete all images<br><br>

run the app.py file in a VM <br>
Command: python3 app.py<br><br>

External IP: http://35.205.85.250:8080<br><br>

run the python script to control the API<br>
Command: python script.py

