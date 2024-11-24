# Define the URL of the Knative service
$KNATIVE_SERVICE_URL = "http://knative-mongodb.default.svc.cluster.local"

# Generate a UUID for the Cloud Event ID
$UUID = [guid]::NewGuid().ToString()

# Define the Cloud Event headers
$headers = @{
    "Content-Type" = "application/json"
    "Ce-Specversion" = "1.0"
    "Ce-Type" = "com.example.event"
    "Ce-Source" = "/my-source"
    "Ce-Id" = $UUID
}

# Define the payload
$body = @"
{
    "message": "Hello World",
    "collection_name": "testing",
    "hello": "nihao"
}
"@

# Send the HTTP POST request
Invoke-WebRequest -Uri $KNATIVE_SERVICE_URL -Method POST -Headers $headers -Body $body
