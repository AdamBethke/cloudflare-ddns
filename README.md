# Cloudflare DDNS

Manage a dynamic DNS entry using Cloudflare's API, with optional metrics.

Requires three inputs:

* **API_TOKEN**: a Cloudflake API token with permission to create, list, and update DNS records in the zone where you're placing the dynamic DNS entry
* **NAME**: hostname for dynamic DNS entry
* **ZONE_ID**: the Cloudflare DNS zone where the dynamic DNS entry will be written

Example invocation:

```sh
podman run \
    --detach \
    --restart always \
    --name ddns \
    --publish 9100:9100 \
    --env API_TOKEN={...} \
    --env ZONE_ID={...} \
    --env NAME={...} \
    cloudflare-ddns:latest
```
