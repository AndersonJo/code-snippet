import ray


@ray.remote
def hello_world():
    print(ray.cluster_resources())
    return "hello world"


ray.init()
print(ray.get(hello_world.remote()))
