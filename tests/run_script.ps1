# Array for the years
$years = @(2016, 2017, 2018, 2019, 2022, 2023, 2024)

# Loop over each year and call the Python script
foreach ($year in $years) {
    python speedAtt2.py $year
}