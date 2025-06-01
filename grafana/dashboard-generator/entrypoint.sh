#!/bin/bash
set -e

# Render the datasource.yaml from the template using envsubst
envsubst < /etc/grafana/provisioning/datasources/datasource.yaml.tpl > /etc/grafana/provisioning/datasources/datasource.yaml

# Start Grafana
exec /usr/share/grafana/bin/grafana-server --config=/etc/grafana/grafana.ini --homepath=/usr/share/grafana "$@"

