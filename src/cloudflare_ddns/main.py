from time import sleep

from ddns.cloudflare import DNSEntryManager
from ddns.configuration import Configuration
from ddns.metrics import dns_entry_checked
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
        if not manager.is_current:
            manager.update_entry()
        dns_entry_checked()
        sleep(configuration.update_interval_in_seconds)

if __name__ == "__main__":
    main()
