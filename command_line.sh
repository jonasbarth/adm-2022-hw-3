#!/bin/bash

countries=("Italy" "Spain" "France" "England" "United States")

for i in ${!countries[@]}; do
        # get number of places.
        # 1. get the address column
        # 2. grep rows that match the country
        # 3. count the number of lines

        places=$(awk -F '\t' '{if (NR>1) printf ("%d\t%d\t%s\n", $4, $5, $10)}' places.tsv | grep "${countries[$i]}")

        if [[ -z "$places" ]]; then
                echo ${countries[$i]}:
                echo "Number of places: 0"
                echo "Average visitors per place: 0"
                echo "Number of people that want to go: 0"
                continue
        fi
                number_of_places=$(awk -F '\t' '{if (NR>1) printf ("%d\t%d\t%s\n", $5, $6, $10)}' places.tsv | grep "${countries[$i]}" | wc -l)

        # get total visitors.
        # 1. get the number of people went column (skip the first line)
        # 2. sum the values
        # awk -F '\t' '{if (NR>1) printf ("%d\t%d\t%s\n", $4, $5, $9)}' places.tsv |
        total_visitors=$(awk -F '\t' '{if (NR>1) printf ("%d\t%d\t%s\n", $5, $6, $10)}' places.tsv | grep "${countries[$i]}" | awk '{s+=$1} END {print s}')

        # get average number of visitors
        # 1. divide total visitors by number of places
        avg_visitors=$(($total_visitors / $number_of_places))

        # get number of people that want to go
        total_want_to_visit=$(awk -F '\t' '{if (NR>1) printf ("%d\t%d\t%s\n", $5, $6, $10)}' places.tsv | grep "${countries[$i]}" | awk '{s+=$2} END {print s}')
        echo ${countries[$i]}:
        echo "Number of places: $number_of_places"
        echo "Average visitors per place: $avg_visitors"
        echo "Number of people that want to go: $total_want_to_visit"

done