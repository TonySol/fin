#!/bin/bash

curl --location --request PUT 'https://api.github.com/repos/'"$TRAVIS_REPO_SLUG"'/pulls/'"$TRAVIS_PULL_REQUEST"'/merge' \
--header 'Authorization: Bearer '"$GH_TOKEN"'' \