#!/bin/bash

# This script is to be run on the ResourceSync destination server.
# It does two main things: 
# - Synchronize our local copy of each collection with updates from member institutions.
# - Propagate these changes to Solr

# Usage: ./incremental-sync.sh timestamp changeslisturl urlmapfrom filepathmapto

# https://stackoverflow.com/questions/893585/how-to-parse-xml-in-bash
read_xml () {
    local IFS=\>
    read -d \< ENTITY CONTENT
}

get_identifier() {
    while read_xml; do
        if [[ $ENTITY = "identifier" ]]; then
            echo $CONTENT
            break
        fi
    done
}

actions="$(resync --incremental --verbose --delete --from $1 --sitemap $2 $3 $4 2>&1)"
while read -r line; do
    action="$(echo $line | cut -f 1 -d " ")"
    case $action in
        created: | updated: | deleted:)
            local_file="$(echo $line | cut -f 4 -d " ")"
            identifier="$(get_identifier < $local_file)"
            case "$action" in
                created:)
                    echo "Creating Solr document for $identifier"
                    # talk to solr
                ;;
                updated:)
                    echo "Updating Solr document for $identifier"
                    # talk to solr
                    ;;
                deleted:)
                    echo "Deleting Solr document for $identifier"
                    # talk to solr
                    ;;
                *)
                    ## error
                    echo "There was a problem"
                    exit 1
                    ;;
            esac
            ;;
        *)
            continue
            ;;
        esac
done <<< "$actions"
