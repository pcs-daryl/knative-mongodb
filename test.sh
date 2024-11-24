KNATIVE_SERVICE_URL="http://knative-mongodb.default.svc.cluster.local"
UUID=$(uuidgen)

curl -X POST $KNATIVE_SERVICE_URL \
  -H "Content-Type: application/json" \
  -H "Ce-Specversion: 1.0" \
  -H "Ce-Type: com.example.event" \
  -H "Ce-Source: /my-source" \
  -H "Ce-Id: $UUID" \
  -d '{
    "message": "Hello World",
    "collection_name": "test",
    "hello": "nihao"
  }'