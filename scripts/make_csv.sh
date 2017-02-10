#!/bin/bash

PERFECT_MERGES=0

pushd conflerge_results
  FILES=actual_*
  for FILE in $FILES
  do  
    if [[ $FILE =~ actual_(.*.java.*) ]]
    then 
      FILE="${BASH_REMATCH[1]}" 
      DIFF=$(diff -U 0 -B -w actual_$FILE expected_$FILE | grep @ | wc -l)
      if [[ $DIFF == 0 ]]
      then
        PERFECT_MERGES=$(($PERFECT_MERGES + 1))
      fi  
    fi
  done
popd

REPO=$(basename "$PWD")

CONFLICTS=$(grep FAILURE res.txt | wc -l)

SUCCESSES=$(grep SUCCESS res.txt | wc -l)

CONFLICTS=$(($CONFLICTS + $SUCCESSES))

PERCENT_RESOLVED=$[SUCCESSES*100/CONFLICTS]

PERCENT_PERFECT=$[PERFECT_MERGES*100/SUCCESSES]

echo ",Conflicts Found,Conflicts Resolved,Perfect Resolutions,% Conflicts Resolved,% Perfect Resolutions" > $REPO.csv
printf "%s,%d,%d,%d,%d,%d" "$REPO" "$CONFLICTS" "$SUCCESSES" "$PERFECT_MERGES" "$PERCENT_RESOLVED" "$PERCENT_PERFECT" >> $REPO.csv