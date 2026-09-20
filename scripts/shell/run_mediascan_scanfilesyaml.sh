#!/bin/bash
set -euo pipefail

pushd moongas-mediascan-golang > /dev/null
go run cmd/mediascan-files-yaml/main.go "$MOONGAS_COLLECTION_ROOTDIR/mediascan-config.yml" "$MOONGAS_COLLECTION_ROOTDIR/mediascan-files.yml"
popd > /dev/null