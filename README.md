# Cloudflare DDNS

Create dynamic DNS entry for a domain using Cloudflare's API.

Requires three inputs:

* API_TOKEN: a Cloudflake API token with permission to create, list, and update DNS records in the zone where you're placing the dynamic DNS entry
* NAME: hostname for dynamic DNS entry
* ZONE_ID: the Cloudflare DNS zone where the dynamic DNS entry will be written
