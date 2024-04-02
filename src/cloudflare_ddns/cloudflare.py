import httpx

from cloudflare_ddns.configuration import Configuration
from cloudflare_ddns.metrics import dns_entry_updated
from cloudflare_ddns.metrics import failed_request
from cloudflare_ddns.models import Trace
from cloudflare_ddns.models import DNSEntry
from cloudflare_ddns.models import DNSEntries
from pydantic import BaseModel
from pydantic.networks import IPvAnyAddress


class DNSEntryManager(BaseModel):
    configuration: Configuration
    record: DNSEntry = None
    trace_url: str = "https://cloudflare.com/cdn-cgi/trace"

    def set_record(self, value: DNSEntry) -> None:
        self.record = value
        dns_entry_updated(name=value.name, ip_address=value.ip_address)

    @property
    def api_url(self) -> str:
        return f"https://api.cloudflare.com/client/v4/zones/{self.configuration.zone_id.get_secret_value()}/dns_records"

    def call(
        self,
        method: str,
        endpoint: str,
        authenticated: bool = True,
        json: dict = None
    ) -> httpx.Response | None:
        with httpx.Client() as client:
            request = httpx.Request(method, endpoint)
            if authenticated:
                request.headers["Authorization"] = f"Bearer {self.configuration.api_token.get_secret_value()}"
            if json:
                request.json = json
            try:
                response = client.send(request)
                if response.is_success:
                    return response
            except Exception:
                pass
            failed_request(
                endpoint="cloudflare-api" if authenticated else "cloudflare-trace",
                method=method,
            )
            return None

    def get_current_ip_address(self) -> IPvAnyAddress | None:
        response = self.call("GET", self.trace_url, authenticated=False)
        if response:
            params = {}
            for pair in filter(None, response.text.split("\n")):
                key, value = tuple(pair.split("="))
                params[key] = value
            trace = Trace(**params)
            return trace.ip
        return None

    def get_current_entry(self) -> bool | None:
        response = self.call("GET", self.api_url)
        # todo: this doesn't have pagination, but the endpoint is paginated
        if response:
            records = DNSEntries(**response.json())
            for record in records.result:
                if record.name == self.configuration.name:
                    self.set_record(record)
                    return True
            return False
        return None

    def json_payload(self, ip: IPvAnyAddress | None = None) -> dict | None:
        if ip is None:
            ip = get_current_entry()

        if ip is None:
            return None

        return {
            "content": ip.exploded,
            "name": self.configuration.name,
            "type": "A" if ip.version == 4 else "AAAA",
            "comment": "DDNS Entry",
            "ttl": 1,
        }

    def create_entry(self) -> None:
        """Creates a DNS entry, setting the name to the ip address provided"""
        json = self.json_payload()
        if not json:
            return

        response = self.call("POST", self.api_url, json=json)
        self.set_record(DNSEntry(**response.json()["result"]))

    def update_entry(self, ip: IPvAnyAddress | None = None) -> None:
        json = self.json_payload(ip)
        if not json:
            return

        response = self.call("PATCH", f"{self.api_url}/{self.record.id}", json=json)
        self.set_record(DNSEntry(**response.json()["result"]))
