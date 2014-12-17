#!/bin/bash

REPOS=( \
    ioos/compliance-checker \
    ioos/catalog \
    ioos/pyoos \
    ioos/wicken \
    ioos/petulant-bear \
    ioos/metamap \
    asascience-open/sci-wms \
    asascience-open/ncsos \
    asascience-open/paegan \
    nctoolbox/nctoolbox \
    )

BASE=https://api.github.com/repos

START=2014-09-01T00:00:00
END=2014-10-01T00:00:00

echo "- iO iC prO prC iCo C R"



for r in ${REPOS[@]}; do
    SAFE=${r/\//-}
    echo "$BASE/$r/issues?state=all&since=$START"

    #
    # ISSUES
    # 
    if [ ! -f $SAFE-issues.json ]; then
        curl -s -o $SAFE-issues.json $BASE/$r/issues?state=all&since=$START
    fi


    #
    # ISSUE COMMENTS
    #
    if [ ! -f $SAFE-comments.json ]; then
        curl -s -o $SAFE-comments.json $BASE/$r/issues/comments?since=$START
    fi


    #
    # COMMITS
    #
    if [ ! -f $SAFE-commits.json ]; then
        curl -s -o $SAFE-commits.json $BASE/$r/commits?since=$START&until=$END
    fi

    
    #
    # RELEASES
    #
    if [ ! -f $SAFE-releases.json ]; then
        curl -s -o $SAFE-releases.json $BASE/$r/releases?since=$START&until=$END
    fi



done

for r in ${REPOS[@]}; do

    SAFE=${r/\//-}
    echo $r

    ISSUES_OPENED=`cat $SAFE-issues.json | jq "[.[] | select(.created_at >= \"$START\" and .created_at < \"$END\") | .title] | length"`

    ISSUES_CLOSED=`cat $SAFE-issues.json | jq "[.[] | select(.closed_at >= \"$START\" and .closed_at < \"$END\" and (has(\"pull_request\") | not)) | .title] | length"`

    PRS_OPENED=`cat $SAFE-issues.json | jq "[.[] | select(.created_at >= \"$START\" and .created_at < \"$END\" and has(\"pull_request\")) | .title] | length"`

    PRS_CLOSED=`cat $SAFE-issues.json | jq "[.[] | select(.closed_at >= \"$START\" and .closed_at < \"$END\" and has(\"pull_request\")) | .title] | length"`

    ISSUE_COMMENTS=`cat $SAFE-comments.json | jq "[.[] | select(.created_at >= \"$START\" and .created_at < \"$END\") | .url ] | length"`

    COMMITS=`cat $SAFE-commits.json | jq 'length'`

    RELEASES=`cat $SAFE-releases.json | jq "[.[] | select(.created_at >= \"$START\" and .created_at < \"$END\") | .title] | length"`
    echo $r $ISSUES_OPENED $ISSUES_CLOSED $PRS_OPENED $PRS_CLOSED $ISSUE_COMMENTS $COMMITS $RELEASES

done
