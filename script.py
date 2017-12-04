import os

# main()
if __name__ == "__main__":

    while True:
        print ("""
        Available API endpoints:
	0. Exit					Exit script.py
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
        """)

        # get user's options
        option = int(input("Enter an option: "))
		
		# to exit the program
        if option == 0:
            exit (0)

		# display all containers
        elif option == 1:
            result = os.system("curl -s -X GET -H 'Accept: application/json' http://35.205.85.250:8080/containers | python3 -mjson.tool")

		# diaplay running containers
        elif option == 2:
            result = os.system("curl -s -X GET -H 'Accept: application/json' http://35.205.85.250:8080/containers?state=running | python3 -mjson.tool")

		# inspect a specific container
        elif option == 3:
            result = os.system("curl -s -X GET -H 'Accept: application/json' http://35.205.85.250:8080/containers/635d2d467002 | python3 -mjson.tool")

		# dump a containers logs
        elif option == 4:
            result = os.system("curl -s -X GET -H 'Accept: application/json' http://35.205.85.250:8080/containers/635d2d467002/logs | python3 -mjson.tool")

		# list all services
        elif option == 5:
            result = os.system("curl -s -X GET -H 'Accept: application/json' http://35.205.85.250:8080/services")

		# list all nodes
        elif option == 6:
            result = os.system("curl -s -X GET -H 'Accept: application/json' http://35.205.85.250:8080/nodes")

		# create new container
        elif option == 7:
            result = os.system("""curl -X POST -H 'Content-Type: application/json' http://35.205.85.250:8080/containers -d '{"image": "lab5-todo-image"}' | python3 -mjson.tool""")

		# change a containers state
        elif option == 8:
            state = int(input("Enter 1 to start or 2 to stop: "))
            if state == 1:
                result = os.system("""curl -X PATCH -H 'Content-Type: application/json' http://35.205.85.250:8080/containers/b6cd8ea512c8 -d '{"state": "running"}' | python3 -mjson.tool""")
            else:
                result = os.system("""curl -X PATCH -H 'Content-Type: application/json' http://35.205.85.250:8080/containers/b6cd8ea512c8 -d '{"state": "stopped"}' | python3 -mjson.tool""")
		
		# delete a container
        elif option == 9:
            result = os.system("curl -s -f -X DELETE -H 'Accept: application/json' http://35.205.85.250:8080/containers/b6cd8ea512c8 | python3 -mjson.tool")
		
		# delete all containers
        elif option == 10:
            result = os.system("curl -f -X DELETE -H 'Accept: application/json' http://35.205.85.250:8080/containers")

		# show all images
        elif option == 11:
            result = os.system("curl -s -X GET -H 'Accept: application/json' http://35.205.85.250:8080/images | python3 -mjson.tool")

		# build an image
        elif option == 12:
            result = os.system("curl -H 'Accept: application/json' -F file=@dockerfiles/sshd.Dockerfile http://35.205.85.250:8080/images")

		# change an images attributes
        elif option == 13:
            result = os.system("""curl -s -X PATCH -H 'Content-Type: application/json' http://35.205.85.250:8080/images/9e7424e5dbae -d '{"tag":"test:1.0"}' | python3 -mjson.tool""")

		# delete an image
        elif option == 14:
            result = os.system("curl -s -f -X DELETE -H 'Accept: application/json' http://35.205.85.250:8080/images/6b362a9f73eb | python3 -mjson.tool")

		# delete all images
        elif option == 15:
            result = os.system("curl -f -X DELETE -H 'Accept: application/json' http://35.205.85.250:8080/images | python3 -mjson.tool")

