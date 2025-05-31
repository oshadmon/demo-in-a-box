docker run -it -d -p 3100:3100 \
   -e GF_SERVER_HTTP_PORT=3100 \
   -v grafana-storage:/var/lib/grafana \
   -v $(pwd)/grafana/provisioning:/etc/grafana/provisioning \
   -v $(pwd)/grafana/dashboards:/var/lib/grafana/dashboards \
--name grafana grafana/grafana-oss:latest


