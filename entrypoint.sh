#!/bin/bash

var='curl --header "X-Vault-Token: <token>"  http://<ip-address-vault>/v1/secret/data/env'
REQ=${var/%env/$ENV}

VAR=`eval $REQ| jq '.data.data'`
for s in $(echo $VAR | jq -r "to_entries|map(\"\(.key)=\(.value|tostring)\")|.[]" ); do
    export $s
done

exec "$@"