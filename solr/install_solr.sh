#!/bin/bash
#Go to SOLR folder
cd solr
#Download SOLR
curl -LO https://archive.apache.org/dist/lucene/solr/6.4.1/solr-6.4.1.tgz
#Uncompress SOLR
tar xvzf solr-6.4.1.tgz
#Remove the compressed folder
rm solr-6.4.1.tgz
#Return to project folder
cd ..
#Report to user
echo "SOLR downloaded successfully."
echo "Please run './solr/run_solr.sh' to run the server."