#!/bin/bash

# Initialize EB CLI repository
eb init -p python2.7 twittmap

# Create an environment and deploy the application to elastic beanstalk
eb create twittmap-env

# Open in the browser
eb open
