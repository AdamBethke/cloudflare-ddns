from prometheus_client import Counter
from prometheus_client import Info
from prometheus_client import Gauge
from pydantic.networks import IPvAnyAddress


DNS_ENTRY_INFO = Info("dns_entry", "Information about the current DNS entry")
DNS_ENTRY_LAST_CHECKED_AT = Gauge("dns_entry_last_checked_at", "Last time the entry was checked for dynamic updates")
DNS_ENTRY_LAST_UPDATED_AT = Gauge("dns_entry_last_updated_at", "Last time the entry was created or updated by this program")
DNS_ENTRY_UPDATED = Counter("dns_entry_updated", "Number of times the DNS entry has been updated")
FAILED_REQUESTS = Counter("failed_requests", "Number of failed requests made by the service")


def dns_entry_checked(
	checked_at: Gauge = DNS_ENTRY_LAST_CHECKED_AT
) -> None:
	checked_at.set_to_current_time()


def dns_entry_updated(
	name: str,
	ip_address: IPvAnyAddress,
	info: Info = DNS_ENTRY_INFO,
	updated_at: Gauge = DNS_ENTRY_LAST_UPDATED_AT,
	updated_counter: Counter = DNS_ENTRY_UPDATED
) -> None:
	info.info({
		"name": name,
		"ip_address": ip_address.exploded,
	})
	updated_at.set_to_current_time()
	updated_counter.inc()


def failed_request(
    *labels,
    metric: Counter = FAILED_REQUESTS,
) -> None:
    metric.labels(labels).inc()
