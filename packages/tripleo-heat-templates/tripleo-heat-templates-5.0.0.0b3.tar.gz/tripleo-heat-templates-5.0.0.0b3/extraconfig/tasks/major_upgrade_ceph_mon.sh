#!/bin/bash
set -eu
set -o pipefail

echo INFO: starting $(basename "$0")

# Exit if not running
if ! pidof ceph-mon; then
    echo INFO: ceph-mon is not running, skipping
    exit 0
fi

# Exit if not Hammer
INSTALLED_VERSION=$(ceph --version | awk '{print $3}')
if ! [[ "$INSTALLED_VERSION" =~ ^0\.94.* ]]; then
    echo INFO: version of Ceph installed is not 0.94, skipping
    exit 0
fi

MON_PID=$(pidof ceph-mon)
MON_ID=$(hostname -s)

# Stop daemon using Hammer sysvinit script
service ceph stop mon.${MON_ID}

# Ensure it's stopped
timeout 60 bash -c "while kill -0 ${MON_PID} 2> /dev/null; do
  sleep 2;
done"

# Update to Jewel
yum -y -q update ceph-mon

# Restart/Exit if not on Jewel, only in that case we need the changes
UPDATED_VERSION=$(ceph --version | awk '{print $3}')
if [[ "$UPDATED_VERSION" =~ ^0\.94.* ]]; then
    echo WARNING: Ceph was not upgraded, restarting daemons
    service ceph start mon.${MON_ID}
elif [[ "$UPDATED_VERSION" =~ ^10\.2.* ]]; then
    echo INFO: Ceph was upgraded to Jewel

    # RPM could own some of these but we can't take risks on the pre-existing files
    for d in /var/lib/ceph/mon /var/log/ceph /var/run/ceph /etc/ceph; do
        chown -R ceph:ceph $d
    done

    # Replay udev events with newer rules
    udevadm trigger

    # Enable systemd unit
    systemctl enable ceph-mon.target
    systemctl enable ceph-mon@${MON_ID}
    systemctl start ceph-mon@${MON_ID}

    # Wait for daemon to be back in the quorum
    timeout 300 bash -c "until (ceph quorum_status | jq .quorum_names | grep -sq ${MON_ID}); do
      echo Waiting for mon.${MON_ID} to re-join quorum;
      sleep 10;
    done"
else
    echo ERROR: Ceph was upgraded to an unknown release, daemon is stopped, need manual intervention
    exit 1
fi
