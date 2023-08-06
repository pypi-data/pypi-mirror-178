import typer
from kubernetes import config
from rich.pretty import pprint

from .benchmarks import IPerfBenchmark
from .kubernetes_integration import KubernetesIntegration
from .util.terminal_ui import terminal_menu
from .util.yaml import load_to_dicts

app = typer.Typer(help="Benchmark runner for network benchmarks.")

config.load_kube_config()


@app.command()
def kubernetes(help="List all nodes in kubernetes cluster"):
    from kubernetes import client
    k8s_api = client.CoreV1Api()
    # nodes = [(node, 1) for node in k8s_api.list_node().items]
    nodes = k8s_api.list_node().items
    node_names = [node.metadata.name for node in nodes]

    client_node = terminal_menu("Choose a client to run on:", node_names)
    node_names = list(filter(lambda x: x != client_node, node_names))
    server_node = terminal_menu("Choose a server to run on:", node_names)
    nodes = None
    node_names = None

    input("Press enter to continue")
    benchmark_in_json = IPerfBenchmark(client_node=client_node, server_node=server_node).run()
    pprint(benchmark_in_json)


@app.command()
def k8d():
    k8 = KubernetesIntegration()

    deployment, service  = load_to_dicts("bandwidth/iperf3-server.yaml")
    #k8.create_from_dict(deployment)
    #print(f"\n[INFO] service `{service['metadata']['name']}` created.")
    #k8.wait_for_resource(deployment, "Deployment")
    #k8.delete_deployment({"metadata": {"name": "iperf3-server"}})
    #print(f"\n[INFO] service `{service['metadata']['name']}` deleted.")

    #k8.create_from_dict(service)
    #print(f"\n[INFO] service `{service['metadata']['name']}` created.")
    #k8.wait_for_resource(service, "Service")
    #k8.delete_service({"metadata": {"name": "iperf3-server"}})
    #print(f"\n[INFO] service `{service['metadata']['name']}` deleted.")

    job = load_to_dicts("bandwidth/iperf3-client.yaml")[0]
    k8.create_from_dict(job)
    print(f"\n[INFO] job `{job['metadata']['name']}` created.")
    k8.wait_for_resource(job, "Job")
    k8.delete_job({"metadata": {"name": "iperf3-client"}})
    print(f"\n[INFO] job `{job['metadata']['name']}` deleted.")




if __name__ == "__main__":
    app()
