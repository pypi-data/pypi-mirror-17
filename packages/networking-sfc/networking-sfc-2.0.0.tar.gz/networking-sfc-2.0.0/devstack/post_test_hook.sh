#!/usr/bin/env bash

set -xe

GATE_DEST=$BASE/new
DEVSTACK_PATH=$GATE_DEST/devstack

source $DEVSTACK_PATH/functions
source $DEVSTACK_PATH/localrc

TEMPEST_CODE_DIR="$BASE/new/tempest"
TEMPEST_DATA_DIR="$DATA_DIR/tempest"
NETWORKING_SFC_DIR="$BASE/new/networking-sfc"

IS_GATE=$(trueorfalse False IS_GATE)
if [[ "$IS_GATE" == "True" ]]
then
    source $NETWORKING_SFC_DIR/devstack/devstackgaterc
fi

owner=stack
sudo_env="TEMPEST_CONFIG_DIR=$TEMPEST_CODE_DIR/etc"

cd $TEMPEST_CODE_DIR
sudo chown -R $owner:stack $TEMPEST_CODE_DIR
sudo mkdir -p "$TEMPEST_DATA_DIR"
sudo chown -R $owner:stack $TEMPEST_DATA_DIR
source $DEVSTACK_PATH/openrc admin admin

echo "Some pre-process info"
neutron net-list
neutron port-list
neutron subnet-list
neutron router-list

echo "Running networking-sfc test suite"
sudo -H -u $owner $sudo_env tox -eall-plugin -- $DEVSTACK_GATE_TEMPEST_REGEX

echo "Some post-process info"
neutron net-list
neutron port-list
neutron subnet-list
neutron router-list
