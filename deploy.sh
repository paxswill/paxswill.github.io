#!/bin/sh

if [ "$TRAVIS_PULL_REQUEST" == "false" ]; then
	# You better have done 'make deploy' first...
	if [ "$TRAVIS" = "true" ]; then
		export GIT_COMMITER_NAME="Travis CI"
		export GIT_COMMITER_EMAIL="travis@travis-ci.org"
		export GIT_AUTHOR_NAME="Will Ross"
		export GIT_AUTHOR_EMAIL="paxswill@paxswill.com"
	fi
	ghp-import -n -b master -m "Travis Build $TRAVIS_JOB_ID" "./output"
	if [ "$GITHUB_TOKEN" ]; then
		PUSH_LOCATION="https://$GITHUB_TOKEN@github.com/paxswill/paxswill.github.io"
	else
		PUSH_LOCATION=origin
	fi
	echo $PUSH_LOCATION
	git push -q "$PUSH_LOCATION" master >/dev/null
fi
