from datetime import datetime , timedelta #for heartbeats
import threading # for running health monitor in background
from docker_utils import DockerManager # for adding nodes
import time

# NodeManager class for creating managing and adding nodes

class NodeManager:
     
    def __init__(self):

        self.nodes={}
        self.docker=DockerManager() # instance of DockerManager
        self.start_health_monitor() #start background thread for heartbeats

    def add_node(self,cpu_cores):
        
        n=len(self.nodes)
        node_id=f"node_{n+1}"
        container= self.docker.create_node(node_id,cpu_cores)
        # new container created

        self.nodes[node_id]={
            'id':node_id,
            'container_id':container.id,
            'cpu_cores':cpu_cores,
            'available_cpu':cpu_cores,
            'pods':[],
            'status':'healthy',
            'last_heartbeat':datetime.now()
        }

        return node_id
    
    def start_health_monitor(self):

        def monitor():

            while True:
                for node_id,node in list(self.nodes.items()):
                    if datetime.now() - node['last_heartbeat']> timedelta(seconds=10):
                        self.handle_node_failure(node_id)

                time.sleep(5)

        threading.Thread(target=monitor, daemon=True).start()

    def handle_node_failure(self, node_id):
        """Handles a failed node"""
        self.nodes[node_id]['status'] = 'unhealthy'
        # Pod rescheduling will be added later




