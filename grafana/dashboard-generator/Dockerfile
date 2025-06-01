FROM grafana/grafana-oss:latest

WORKDIR /app

# Install envsubst for Alpine-based image
USER root
RUN apk add --no-cache gettext

# Install the simpod-json-datasource plugin
RUN /usr/share/grafana/bin/grafana-cli --homepath=/usr/share/grafana plugins install simpod-json-datasource

# Create provisioning and dashboard directories
RUN mkdir -p /etc/grafana/provisioning/datasources \
             /etc/grafana/provisioning/dashboards \
             /var/lib/grafana/dashboards

# Copy provisioning templates and dashboards
COPY datasource.yaml.tpl /etc/grafana/provisioning/datasources/datasource.yaml.tpl
COPY dashboards.yaml /etc/grafana/provisioning/dashboards/dashboards.yaml
COPY grafana.ini /etc/grafana/grafana.ini

# Copy dashboard JSON files
COPY *.json /var/lib/grafana/dashboards/

# Copy and set entrypoint
COPY entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh \
    && chown -R 472:472 /etc/grafana /var/lib/grafana /app/entrypoint.sh /etc/grafana/grafana.ini

USER 472

ENTRYPOINT ["/app/entrypoint.sh"]
