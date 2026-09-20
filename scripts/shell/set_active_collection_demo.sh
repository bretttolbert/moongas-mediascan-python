#!/bin/bash

set -euo pipefail

echo "Setting active media collection to demo..."
export MEDIA_COLLECTION_ROOTDIR=$MEDIA_COLLECTION_DEMO
echo "Media collection rootdir is now set to: ${MEDIA_COLLECTION_ROOTDIR:-}"
