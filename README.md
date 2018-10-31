build trigger
===
Simple service for triggering builds

[![Build Status](https://travis-ci.org/sivakov512/build-trigger.svg?branch=master)](https://travis-ci.org/sivakov512/build-trigger)
[![Coverage Status](https://coveralls.io/repos/github/sivakov512/build-trigger/badge.svg?branch=master)](https://coveralls.io/github/sivakov512/build-trigger?branch=master)
[![Docker hub](https://img.shields.io/badge/docker%20hub-latest-blue.svg)](https://hub.docker.com/r/sivakov512/build-trigger/)

Installation
===
Service requires setting the environment variable `SPEC_PATH` which points to `yaml`-specification file.

You can use provided Docker container or install it manually.

Configuration
===
Application has support for `.env` files. You can create your own `.env` in project root or define the necessary environment variable `SPEC_PATH` in another way.

* TravisCI

TravisCI configuration must looks like this:

``` yaml
travis:  # section of travis conf
  secret_key: lolkekmakarek  # secret token for access to TravisCI via API v3

  repos:  # your repos
    awesome_repo:  # your own alias for this repo
      awesome_trigger_token: awesome%2Fawesome_repo  # your own secret token for triggering repo awesome%2Fawesome_repo
    yet_another_repo:
      yet_another_trigger_token: awesome%2Fyet_another_repo
```

Usage
===
When application configured and run you can trigger build like this:

``` shell
http GET http://127.0.0.1:5000/travis/awesome_repo/awesome_trigger_token/
# or
http POST http://127.0.0.1:5000/travis/awesome_repo/awesome_trigger_token/
```
This api call will trigger build of `awesome/wesome_repo`

For what?
===
For example, you can use it for triggering build via webhooks, like Docker Hub webhooks.

