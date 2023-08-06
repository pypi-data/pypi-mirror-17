#!/bin/bash
set -ex
# This script runs ara-specific integration tests.
export PATH=$PATH:/usr/local/sbin:/usr/sbin
LOGROOT=${WORKSPACE:-/tmp}
LOGDIR="${LOGROOT}/logs"
BUILD_DIR="${LOGDIR}/build"
export ANSIBLE_TMP_DIR="${LOGDIR}/ansible"
DATABASE="${LOGDIR}/ansible.sqlite"

# Cleanup any previous runs
rm -rf $LOGDIR
mkdir -p $LOGDIR

# Install ARA so it can be used from a virtual environment
tox -e venv --notest
source .tox/venv/bin/activate

# Setup ARA
export ANSIBLE_CALLBACK_PLUGINS="ara/callback"
export ARA_DATABASE="sqlite:///${DATABASE}"

# Run test playbooks
ansible-playbook -vv tests/integration/smoke.yml
ansible-playbook -vv tests/integration/hosts.yml

# Run test commands
pbid=$(ara playbook list -c ID -f value |head -n1)

ara playbook show $pbid
ara host list -b $pbid
ara host show -b $pbid localhost
ara host facts -b $pbid localhost
ara play show $(ara play list -a -c ID -f value |head -n1)
ara result show $(ara result list -a -c ID -f value |tail -n1) --long
ara stats show $(ara stats list -c ID -f value |head -n1)
ara task show $(ara task list -a -c ID -f value |head -n1)
ara file list -b $pbid
ara file show $(ara file list -b $pbid -c ID -f value|head -n1)
ara generate ${BUILD_DIR} && tree ${BUILD_DIR}
