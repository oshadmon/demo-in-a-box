apiVersion: 1

datasources:
  - name: simpod-json-datasource
    type: simpod-json-datasource
    access: proxy
    url: ${DATASOURCE_URL}
    isDefault: true
    editable: true
    uid: default_json_ds

