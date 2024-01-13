from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel
from pydantic import Field
from pydantic.networks import IPvAnyAddress


class Trace(BaseModel):
    fl: str
    h: str
    ip: IPvAnyAddress
    ts: str
    visit_scheme: str
    uag: str
    colo: str
    sliver: str
    http: str
    loc: str
    tls: str
    sni: str
    warp: str
    gateway: bool
    rbi: bool
    kex: str


class Pagination(BaseModel):
  page: int
  per_page: int
  count: int
  total_count: int
  total_pages: int


class DNSEntryType(str, Enum):
	CNAME = "CNAME"
	A = "A"
	AAAA = "AAAA"
	CAA = "CAA"
	CERT = "CERT"
	DNSKEY = "DNSKEY"
	DS = "DS"
	HTTPS = "HTTPS"
	LOC = "LOC"
	MX = "MX"
	NAPTR = "NAPTR"
	NS = "NS"
	PIR = "PIR"
	SMIMEA = "SMIMEA"
	SRV = "SRV"
	SSHFP = "SSHFP"
	SVCB = "SVCB"
	TLSA = "TLSA"
	TXT = "TXT"
	URI = "URI"


class DNSEntry(BaseModel):
    id: str
    zone_id: str
    zone_name: str
    name: str
    type: DNSEntryType
    content: str
    proxiable: bool
    proxied: bool
    ttl: int
    locked: bool
    meta: dict[str, Any]
    comment: str | None
    tags: list[str]
    created_on: datetime
    modified_on: datetime
    @property
    def ip_address(self) -> IPvAnyAddress:
        if self.type in (DNSEntryType.A, DNSEntryType.AAAA):
            return IPvAnyAddress(self.content)


class DNSEntries(BaseModel):
    result: list[DNSEntry]
    success: bool
    errors: list
    messages: list
    result_info: Pagination
