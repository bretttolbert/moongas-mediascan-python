#!/bin/bash
set -euo pipefail
HOST=$MEDIASERVER_DROPLET_IP
DEST_USER=root
SVC=mediaserver
ssh -o ConnectTimeout=10 $DEST_USER@$HOST "systemctl stop $SVC && sleep 1 && systemctl start $SVC; echo 'Restarted $SVC'"
echo 'Restarted mediaserver'
echo 'Done'
