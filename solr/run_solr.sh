#!/bin/bash
#Go to SOLR folder
# cd solr/solr-6.4.1/example
#Report to user
echo "Starting SOLR server."
# java -jar start.jar
./solr/solr-6.4.1/bin/solr create_collection -c default -p 8983
./solr/solr-6.4.1/bin/solr start -e cloud -noprompt
