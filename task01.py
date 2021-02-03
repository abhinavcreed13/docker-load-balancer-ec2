import docker

# pull image
client = docker.from_env()
image = client.images.pull("nclcloudcomputing/javabenchmarkapp")
print(f"Image pulled: {image.id}")

# run container
container = client.containers.run("nclcloudcomputing/javabenchmarkapp", detach=True, 
                                    ports={'8080/tcp':8080})
print(f"Container started: {container.id}")


