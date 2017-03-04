#!/bin/bash
#Go to SOLR folder
# cd solr/solr-6.4.1/example
#Report to user
echo "Stopping SOLR server."
# java -jar start.jar
./solr/solr-6.4.1/bin/solr stop -all -e cloud -noprompt
