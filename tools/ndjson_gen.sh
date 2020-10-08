#/bin/bash

rm -f ./fhir-json-samples/*.ndjson
FILES=./fhir-json-samples/*.json


for f in $FILES
do
    echo "Processing $f file ..."
    cat $f | jq -c '.' >> ./fhir-json-samples/files.ndjson
done

gsutil cp fhir-json-samples/files.ndjson gs://cabral-healthcare/fhir-json-samples/
