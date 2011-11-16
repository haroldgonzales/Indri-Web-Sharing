#!/bin/bash

find queries/ -iname "*.parameters" | xargs -I '{}' IndriBuildIndex '{}'
