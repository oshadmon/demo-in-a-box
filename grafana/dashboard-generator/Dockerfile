FROM grafana/grafana-oss:latest

# Install the simpod-json-datasource plugin
RUN grafana-cli plugins install simpod-json-datasource

# Create provisioning and dashboard directories
RUN mkdir -p /etc/grafana/provisioning/datasources \
             /etc/grafana/provisioning/dashboards \
             /var/lib/grafana/dashboards

# Copy provisioning files
COPY datasource.yaml /etc/grafana/provisioning/datasources/datasource.yaml
COPY dashboards.yaml /etc/grafana/provisioning/dashboards/dashboards.yaml
COPY grafana.ini /etc/grafana/grafana.ini

# Copy dashboard JSON files
COPY *.json /var/lib/grafana/dashboards/

# Fix permissions using UID:GID instead of grafana:grafana
USER root
RUN chown -R 472:472 /etc/grafana /var/lib/grafana
USER 472

