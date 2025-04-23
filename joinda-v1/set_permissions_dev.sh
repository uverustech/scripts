#!/bin/bash
# Script: set_permissions_dev.sh
# Description: Loose 777 permission setup for development

WEB_ROOT="$(pwd)"

# Create /xml directory if it doesn't exist
if [ ! -d "$WEB_ROOT/xml" ]; then
  echo "Creating missing /xml directory..."
  mkdir "$WEB_ROOT/xml"
fi

# Set recursive 777 permissions for dev
echo "Setting 777 permissions recursively..."
chmod -R 777 "$WEB_ROOT/upload"
chmod -R 777 "$WEB_ROOT/xml"
chmod -R 777 "$WEB_ROOT/cache"
chmod -R 777 "$WEB_ROOT/nodejs/models"

# Done
echo "Development permissions applied to writable directories."
