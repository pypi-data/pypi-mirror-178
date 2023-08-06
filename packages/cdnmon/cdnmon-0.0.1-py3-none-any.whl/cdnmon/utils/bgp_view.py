from cdnmon.utils.http_client import http_cached_requests
import json
import ipaddress


def query_asns(query_term):
    """
    [1] https://bgpview.docs.apiary.io/#reference/0/asn-prefixes/view-asn-prefixes
    [2] https://api.bgpview.io/search
    """
    url = "https://bgpview.walless.online/search"
    params = {
        "query_term": query_term,
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/107.0.0.0 Safari/537.36 "
    }
    cache_folder = f"ip_ranges/bgpview/{query_term}"
    response = http_cached_requests(url, params=params, headers=headers, cache_folder=cache_folder)
    return json.loads(response)


def extract_networks(data):
    ipv4_networks = []
    ipv6_networks = []
    for item in data["data"]["ipv4_prefixes"]:
        ipv4_networks.append(ipaddress.IPv4Network(item["prefix"], strict=False))
    for item in data["data"]["ipv6_prefixes"]:
        ipv6_networks.append(ipaddress.IPv6Network(item["prefix"], strict=False))
    return ipv4_networks, ipv6_networks


def main():
    query_asns("alicloud")


if __name__ == "__main__":
    main()
