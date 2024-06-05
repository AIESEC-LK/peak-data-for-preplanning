# Define the list of years and ey-codes
$years = 2024, 2023, 2022, 2021
$ey_codes = 1559,1622, 504, 1585, 1609

# Path to the Python script
$pythonScript = ".\speedAtt2.py"

# Loop through each year and ey-code combination
foreach ($year in $years) {
    foreach ($ey_code in $ey_codes) {
        # Construct the command
        $command = "python $pythonScript $year $ey_code"
        
        # Write the command to the console (optional)
        Write-Output "Running: $command"
        
        # Execute the command
        Invoke-Expression $command
    }
}
