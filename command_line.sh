#!/bin/bash

myArray=("Italy" "Spain" "France" "England" "United|States")

for i in ${!myArray[@]}; do
  echo $(grep -cE ${myArray[$i]}  places.tsv | cut -f10)
  #echo $(grep address places.tsv | grep ${myArray[$i]} |cut -f5 |paste -s -d+ |bc)
done


