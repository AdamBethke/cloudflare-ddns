from time import sleep

from cloudflare_ddns.cloudflare import DNSEntryManager
from cloudflare_ddns.configuration import Configuration
from cloudflare_ddns.metrics import dns_entry_checked
from prometheus_client import start_http_server


def main():
    configuration: Configuration = Configuration()
    manager: DNSEntryManager = DNSEntryManager(configuration=configuration)
    if configuration.metrics_port:
        start_http_server(configuration.metrics_port)

    while True:
        if not manager.record:
            exists = manager.get_current_entry()
            if exists is False:
                manager.create_entry()
        current_ip_address = manager.get_current_ip_address()
        if manager.record.ip_address != current_ip_address:
            manager.update_entry(current_ip_address)
        dns_entry_checked()
        sleep(configuration.update_interval_in_seconds)

if __name__ == "__main__":
    main()
