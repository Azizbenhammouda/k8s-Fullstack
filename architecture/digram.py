from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Deployment, Pod
from diagrams.k8s.network import Service, Ingress
from diagrams.k8s.storage import PersistentVolumeClaim
from diagrams.onprem.container import Docker
from diagrams.onprem.client import User
 
with Diagram(
    "Fullstack React & Node.js on Kubernetes (Kind)",
    filename="fullstack_k8s_diagram",
    show=False,
    direction="LR",
):
    user = User("Browser / User")
 
    with Cluster("Kind Cluster: fullstackapp-cluster"):
 
        with Cluster("Frontend"):
            fe_svc = Service("frontend-service\n(NodePort)")
            fe_deploy = Deployment("frontend-deployment")
            fe_pod = Pod("React Pod")
            fe_deploy >> fe_pod
 
        with Cluster("Backend"):
            be_svc = Service("backend-service\n(ClusterIP)")
            be_deploy = Deployment("backend-deployment")
            be_pod = Pod("Node.js Pod")
            be_deploy >> be_pod
 
        with Cluster("Database"):
            pg_svc = Service("postgres-service\n(ClusterIP)")
            pg_deploy = Deployment("postgres-deployment")
            pg_pod = Pod("PostgreSQL Pod")
            pg_pvc = PersistentVolumeClaim("postgres-pvc")
            pg_deploy >> pg_pod
            pg_pod >> pg_pvc
 
    # Traffic flow
    user >> Edge(label="HTTP") >> fe_svc
    fe_svc >> fe_pod
    fe_pod >> Edge(label="API calls") >> be_svc
    be_svc >> be_pod
    be_pod >> Edge(label="SQL") >> pg_svc
    pg_svc >> pg_pod