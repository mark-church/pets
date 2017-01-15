#!/bin/sh
consul agent -data-dir=/tmp/consul -server -advertise $(hostname -i) -client $(hostname -i) -config-file /run/secrets/consul-encrypt.json -bootstrap-expect=3 -retry-join db
