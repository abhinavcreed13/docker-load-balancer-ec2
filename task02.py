# loading modules
import docker
import argparse
from util import get_args

# setting up client 
client = docker.from_env()

# argument parser
args = get_args()

if args.mode == "deploy":
    if args.init_swarm == "True":
        # initialising the swarm 
        client.swarm.init()

    # specifying service options
    es_prime = docker.types.EndpointSpec(ports={80:8080})
    sm_prime = docker.types.ServiceMode('replicated',args.replicate)
    es_viz = docker.types.EndpointSpec(ports={88:8080})
    mount_viz = ["/var/run/docker.sock:/var/run/docker.sock"]
    es_mongo = docker.types.EndpointSpec(ports={3306:27017})
    mount_mongo = [f"{args.mount_mongo}:/data/db"]
    manager = ["node.role == manager"]

    # creating the services 
    client.services.create('nclcloudcomputing/javabenchmarkapp',name='prime',endpoint_spec=es_prime,mode=sm_prime)
    client.services.create('dockersamples/visualizer',name='viz',endpoint_spec=es_viz,constraints=manager,mounts=mount_viz)
    client.services.create('mongo',name='mongo',endpoint_spec=es_mongo,constraints=manager,mounts=mount_mongo)

elif args.mode == "display":
    # show services
    print(client.services.list())
    print(client.containers.list(all=True))

elif args.mode == "leave":
    # removing from the swarm 
    client.swarm.leave(force=True)

