#!/bin/bash

# Arrays for the first and second arguments
years=(2016 2017 2018 2019 2022 2023 2024)
codes=(1623 1622 1585 1609 504)

# Loop over each combination of the values
for year in "${years[@]}"; do
  for code in "${codes[@]}"; do
    python speedAtt2.py "$((10#$year))" "$((10#$code))"
  done
done

