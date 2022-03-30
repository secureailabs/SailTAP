# --------------------------------------------------------------------------
# Leveraging AZURE SDK to setup azure resources from Empty Subscription
# Run az login before executing this script from powershell
#
# Written by Stanley Lin 12/09/2021
# --------------------------------------------------------------------------
from azure.identity import AzureCliCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient

# from azure.mgmt.compute import ComputeManagementClient


import os

# Change subscription_id to the necessary subscription
SUBSCRIPTION_ID = "7d646433-6ff0-451c-867a-f46bdfdaf2b0"  # Stanley Playground
GROUP_NAME = "SCRIPTED_rg"
IP_CONFIGURATION_NAME = "default"

VIRTUAL_NETWORK_NAME = "virtualnetwork_stan2"
GATEWAY_SUBNET = "GatewaySubnet"  # Has to be named GatewaySubnet
VIRTUAL_PRIVATE_NETWORK_GATEWAY_NAME = "virtual_network_gateway_stan2"
VPN_PUBLIC_IP_ADDRESS_NAME = "virtual_network_gateway_stan_pip"
FIREWALL_NAME = "stanley_firewall_2"
FIREWALL_SUBNET = "AzureFirewallSubnet"  # Has to be named AzureFirewallSubnet
FIREWALL_PUBLIC_IP_ADDRESS_NAME = "stanley_firewall_pip"
FIREWALL_POLICY_NAME = "stanley_fire_policy"

# Eventually we should get user to input these following values maybe as env.
# SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)

# subscription_id for Stanley Playground
# subscription_id = "7d646433-6ff0-451c-867a-f46bdfdaf2b0"
# resource_group = "Test_RG"
# appid = "aae23cae-73ab-4bbc-ad9d-ee788a08cea9"
# password = "GCnJMDss~5FMQ0-Rj_qwRAA-q9twWYBu2-"

# Network and IP address names required for vm
VNET_NAME = "python-example-vnet"
IP_NAME = "python-example-ip"
IP_CONFIG_NAME = "python-example-ip-config"
NIC_NAME = "python-example-nic"


# Acquire a credential object using CLI-based authentication.
credential = AzureCliCredential()
# Obtain the management object for resources.
resource_client = ResourceManagementClient(credential, SUBSCRIPTION_ID)
network_client = NetworkManagementClient(credential, SUBSCRIPTION_ID)

# Create resource group
resource_client.resource_groups.create_or_update(GROUP_NAME, {"location": "eastus"})
# Retrieve the list of resource groups
group_list = resource_client.resource_groups.list()

# Show the groups in formatted output
column_width = 40
print("Resource Group".ljust(column_width) + "Location")
print("-" * (column_width * 2))

for group in list(group_list):
    print(f"{group.name:<{column_width}}{group.location}")


def main():
    """
    Provision or Updates resources in the Subscription
    Order matters
    """
    # VPN Public IP
    network_client.public_ip_addresses.begin_create_or_update(
        GROUP_NAME,
        VPN_PUBLIC_IP_ADDRESS_NAME,
        {
            "location": "eastus",
            "sku": {"name": "Standard"},
            "public_ip_allocation_method": "Static",
            "public_ip_address_version": "IPV4",
            "idle_timeout_in_minutes": 4,
        },
    )
    # Virtual Network
    network = network_client.virtual_networks.begin_create_or_update(
        GROUP_NAME,
        VIRTUAL_NETWORK_NAME,
        {
            "address_space": {"address_prefixes": ["10.0.0.0/16"]},
            "subnets": [
                {
                    "name": "Default",
                    "properties": {
                        "addressPrefix": "10.0.0.0/24",
                    },
                },
                {
                    "name": "test-subnet",
                    "properties": {
                        "addressPrefix": "10.0.1.0/24",
                    },
                },
                {
                    "name": FIREWALL_SUBNET,
                    "properties": {
                        "addressPrefix": "10.0.2.0/24",
                    },
                },
            ],
            "location": "eastus",
        },
    ).result()
    print(f"\nCreate virtual network:\n{network}")

    # Create gateway subnet
    network_client.subnets.begin_create_or_update(
        GROUP_NAME, VIRTUAL_NETWORK_NAME, GATEWAY_SUBNET, {"address_prefix": "10.0.128.0/17"}
    ).result()
    # Create virtual network gateway
    virtual_network_gateway = network_client.virtual_network_gateways.begin_create_or_update(
        GROUP_NAME,
        VIRTUAL_PRIVATE_NETWORK_GATEWAY_NAME,
        {
            "ip_configurations": [
                {
                    "private_ip_allocation_method": "Dynamic",
                    "subnet": {
                        "id": f"/subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{GROUP_NAME}/providers/Microsoft.Network/virtualNetworks/{VIRTUAL_NETWORK_NAME}/subnets/{GATEWAY_SUBNET}"
                    },
                    "public_ip_address": {
                        "id": f"/subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{GROUP_NAME}/providers/Microsoft.Network/publicIPAddresses/{VPN_PUBLIC_IP_ADDRESS_NAME}"
                    },
                    "name": IP_CONFIGURATION_NAME,
                }
            ],
            "gateway_type": "Vpn",
            "vpn_type": "RouteBased",
            "enable_bgp": False,
            "active_active": False,
            "enable_dns_forwarding": False,
            "sku": {"name": "VpnGw1", "tier": "VpnGw1"},
            # "bgp_settings": {"asn": "65515", "bgp_peering_address": "10.0.255.254", "peer_weight": "0"},
            "location": "eastus",
        },
    ).result()
    print("\nCreate virtual network gateway:\n{}".format(virtual_network_gateway))
    # Get virtual network gateway
    virtual_network_gateway = network_client.virtual_network_gateways.get(
        GROUP_NAME, VIRTUAL_PRIVATE_NETWORK_GATEWAY_NAME
    )
    print("\nGet virtual network gateway:\n{}".format(virtual_network_gateway))

    # Firewall Public IP
    network_client.public_ip_addresses.begin_create_or_update(
        GROUP_NAME,
        FIREWALL_PUBLIC_IP_ADDRESS_NAME,
        {
            "location": "eastus",
            "sku": {"name": "Standard"},
            "public_ip_allocation_method": "Static",
            "public_ip_address_version": "IPV4",
            "idle_timeout_in_minutes": 4,
        },
    )
    # Basic Firewall Policy
    network_client.firewall_policies.begin_create_or_update(
        GROUP_NAME, FIREWALL_POLICY_NAME, {"location": "eastus", "threat_intel_mode": "Alert"}
    ).result()
    # Firewall
    azure_firewall = network_client.azure_firewalls.begin_create_or_update(
        GROUP_NAME,
        FIREWALL_NAME,
        {
            "location": "eastus",
            "zones": [],
            "properties": {
                "sku": {"name": "AZFW_VNet", "tier": "Standard"},
                "threat_intel_mode": "Alert",
                "ip_configurations": [
                    {
                        "private_ip_allocation_method": "Dynamic",
                        "subnet": {
                            "id": f"/subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{GROUP_NAME}/providers/Microsoft.Network/virtualNetworks/{VIRTUAL_NETWORK_NAME}/subnets/{FIREWALL_SUBNET}"
                        },
                        "public_ip_address": {
                            "id": f"/subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{GROUP_NAME}/providers/Microsoft.Network/publicIPAddresses/{FIREWALL_PUBLIC_IP_ADDRESS_NAME}"
                        },
                        "name": IP_CONFIGURATION_NAME,
                    }
                ],
                "firewall_policy": {
                    "id": f"/subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{GROUP_NAME}/providers/Microsoft.Network/firewallPolicies/{FIREWALL_POLICY_NAME}"
                },
            },
        },
    ).result()
    print("Create azure firewall:\n{}".format(azure_firewall))


if __name__ == "__main__":
    main()
