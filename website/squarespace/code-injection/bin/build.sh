#!/bin/bash

# Navigate to shell script directory
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"

# Create build output directory
mkdir ../bundle/

# Create empty HTML file
touch ../bundle/bundle.html

# Concatenate minified CSS
MINIFIED_CSS=$(uglifycss ../styles/styles.css)
echo "<style>" >> ../bundle/bundle.html
echo "  ${MINIFIED_CSS}" >> ../bundle/bundle.html
echo "</style>" >> ../bundle/bundle.html

# Concatenate minified JavaScript
MINIFIED_JS=$(uglifyjs ../scripts/scripts.js)
echo "<script>" >> ../bundle/bundle.html
echo "  ${MINIFIED_JS}" >> ../bundle/bundle.html
echo "</script>" >> ../bundle/bundle.html
