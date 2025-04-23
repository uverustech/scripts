#!/bin/bash
# Script: set_permissions_secure.sh
# Description: Secure permission setup for production

WEB_ROOT="$(pwd)"
APACHE_USER="www-data"

# Set ownership to Apache user
echo "Setting ownership to $APACHE_USER..."
chown -R $APACHE_USER:$APACHE_USER "$WEB_ROOT"

# Set folder permissions to 775
find "$WEB_ROOT" -type d -exec chmod 775 {} \;

# Set file permissions to 664
find "$WEB_ROOT" -type f -exec chmod 664 {} \;

# Done
echo "Secure permissions applied to $WEB_ROOT."
