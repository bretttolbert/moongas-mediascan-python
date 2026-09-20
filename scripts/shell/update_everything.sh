#!/bin/bash
set -euo pipefail
./run-scan-to-files-yaml-yaml
./run-scan-to-artists-yaml-yaml
./run-scan-to-db
./upload-scan-to-db
./update-covers
./upload-covers
./restart-remote-services
sudo ./restart-local-services
