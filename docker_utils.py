import docker

class DockerManager:

    #constructor
    def __init__(self):

        self.client=docker.from_env() #connect to docker deamon,initializes docker client
    
    # create node
    # Creates a container simulating a cluster node
    def create_node(self,name,cpu_cores):

        #run() - starts new 
        # alpine - linux distro
        container= self.client.containers.run(
            "alpine:latest",
            command= " tail -f /dev/null", # keep container running
            detach=True, # run in background
            name=name,
            cpuset_cpus=f"0-{cpu_cores-1}" if cpu_cores > 1 else "0",
            mem_limit='256m'
        )

        return container


        