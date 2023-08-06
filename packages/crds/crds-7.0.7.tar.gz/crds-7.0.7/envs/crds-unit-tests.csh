#! /bin/csh -f

# Taken from ./runtests to define a command line environment equivalent
# to the one runtests establishes prior to running nose.

setenv CRDS_SERVER_URL https://hst-crds-ops.stsci.edu

setenv CRDS_TEST_ROOT $HOME

setenv CRDS_TESTING_CACHE  $CRDS_TEST_ROOT/crds-cache-test

setenv CRDS_PATH  $CRDS_TEST_ROOT/crds-cache-default-test

setenv CRDS_DEFAULT_CACHE $CRDS_PATH

