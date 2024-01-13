FROM python:3.11-slim

ARG USER=ddns
ARG USER_UID=50000
RUN useradd ${USER} --uid ${USER_UID} --create-home
USER ${USER}

ENV PATH="/home/${USER}/.local/bin/:$PATH"

WORKDIR /home/${USER}/cloudflare-ddns
COPY --chown=${USER} pyproject.toml .
COPY --chown=${USER} src/ ./src/
RUN python -m pip install --upgrade pip && pip install --user --editable .

ENV NAME=
ENV API_TOKEN=
ENV ZONE_ID=
ENV METRICS_PORT=9100

ENTRYPOINT ["python", "-u", "src/cloudflare_ddns/main.py"]
