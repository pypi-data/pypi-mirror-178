import boto3

def get_load_balancers_ips(client: str):
    print("in func")
    load_balancers = {}
    response = client.describe_load_balancers()
    print(response)
    for res in response.get("LoadBalancers"):
        ips = []
        for az in res["AvailabilityZones"]:
            for ip_addresses in az["LoadBalancerAddresses"]:
                ips.add(ip_addresses["IpAddress"])
        load_balancers[res["LoadBalancerName"]] = ips
    return load_balancers


def main():
    print("starting")
    client = boto3.client("elbv2", region_name="us-west-2")
    response = get_load_balancers_ips(client)
    print(response)


if __name__ == "__main__":
    main()