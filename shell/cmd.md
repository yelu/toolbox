
## copy dir and sub-dirs recursively
    # /Y Suppress prompt to confirm overwriting a file.
    # /I If in doubt always assume the destination is a folder
    # /E Copy folders and subfolders, including Empty folders.
    # /R Overwrite read-only files.
    # /S Copy folders and subfolders
    xcopy "$(ProjectDir)model" "$(TargetDir)model" /y /i /r /s /e

## for loop

    loop for a range of number.

      for /l %x in (1, 1, 100) do (
          echo %x
      )

loop through a list

    FOR %G IN (Myfile.txt SecondFile.txt) DO copy %G d:\backups\

Use two %s if it's in a batch file

    for /l %%x in (1, 1, 100) do (
        echo %%x
    )