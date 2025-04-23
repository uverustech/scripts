#!/bin/bash
# Script: set_permissions.sh
# Description: Apply secure or dev permissions using current directory as WEB_ROOT

WEB_ROOT="$(pwd)"
APACHE_USER="www-data"
MODE="secure"

# Check for dev flag
if [[ "$1" == "--dev" ]]; then
  MODE="dev"
fi

echo "Using current directory as WEB_ROOT: $WEB_ROOT"
echo "Applying $MODE permissions..."

# Set ownership to Apache user
echo "Setting ownership to $APACHE_USER..."
chown -R $APACHE_USER:$APACHE_USER "$WEB_ROOT"

if [[ "$MODE" == "dev" ]]; then
  # Dev mode: chmod 777 everything
  find "$WEB_ROOT" -type d -exec chmod 777 {} \;
  find "$WEB_ROOT" -type f -exec chmod 777 {} \;
  mkdir -p "$WEB_ROOT/xml"
  chmod -R 777 "$WEB_ROOT/xml"

  # Ensure writable paths for dev
  chmod 777 "$WEB_ROOT/sitemap.xml"
  chmod 777 "$WEB_ROOT/sitemap-index.xml"
  chmod -R 777 "$WEB_ROOT/themes/joinda-classic/img"
else
  # Secure mode: directories 775, files 664
  find "$WEB_ROOT" -type d -exec chmod 775 {} \;
  find "$WEB_ROOT" -type f -exec chmod 664 {} \;

  # Additional writable paths required by the app
  chmod 777 "$WEB_ROOT/sitemap.xml"
  chmod 777 "$WEB_ROOT/sitemap-index.xml"
  chmod -R 777 "$WEB_ROOT/themes/joinda-classic/img"
fi

echo "$MODE permissions applied to $WEB_ROOT."
