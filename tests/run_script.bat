@echo off
setlocal EnableDelayedExpansion

set "years=2016 2017 2018 2019 2022 2023 2024"

for %%Y in (%years%) do (
    python speedAtt2.py %%Y
)

endlocal