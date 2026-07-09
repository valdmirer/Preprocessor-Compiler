@echo off
setlocal enabledelayedexpansion

REM Prompt user for confirmation
echo This script will delete all .exe files named after their parent folder in every folder on your system.
echo Please ensure you have backed up any important data before proceeding.
pause

REM Iterate through all directories recursively
for /r %%i in (*) do (
    REM Get the folder name
    set "folderName=%%~nxi"
    REM Construct the full path to the .exe file
    set "exeFilePath=%%i\!folderName!.exe"
    REM Check if the .exe file exists
    echo Checking folder: %%i
    if exist "!exeFilePath!" (.
        echo Found file: !exeFilePath!
        echo Deleting file: !exeFilePath!
        del /f /q "!exeFilePath!"
        if exist "!exeFilePath!" (
            echo Failed to delete file: !exeFilePath!
        ) else (
            echo Successfully deleted file: !exeFilePath!
        )
    ) else (
        echo No matching file found in: %%i
    )
)

echo Process completed.
pause