export DOCKER_TLS_VERIFY=1
export DOCKER_CERT_PATH="$(pwd)"
export DOCKER_HOST=tcp://ucp.church.dckr.org:443
#
# Bundle for user admin
# UCP Instance ID 56MK:EL2I:N54C:LFUC:YCAY:COE2:CUFL:KMF6:3KHL:SNB2:7YGH:LKAE
#
# This admin cert will also work directly against Swarm and the individual
# engine proxies for troubleshooting.  After sourcing this env file, use
# "docker info" to discover the location of Swarm managers and engines.
# and use the --host option to override $DOCKER_HOST
#
# Run this command from within this directory to configure your shell:
# eval $(<env.sh)
