#!/bin/bash
set -euo pipefail
SVC=mediaserver
systemctl stop $SVC && sleep 1 && systemctl start $SVC; echo "Restarted $SVC"
echo 'Restarted mediaserver'
echo 'Done'
