def generate_masscan_config_file(networks, masscan_output_filepath):
    range_part = [f"range = {network}" for network in networks]
    other_parts = [
        "ports = 80,443,U:53",
        "ping = true",
        "output-format = json",
        "output-status = all",
        f"output-filename = {masscan_output_filepath}",
        "pfring",
        "rate = 8192",
        "http-user-agent = Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/107.0.0.0 Safari/537.36",
        "wait = 60",
    ]
    template = "\n".join(range_part + other_parts)
    return template
