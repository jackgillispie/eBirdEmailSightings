@echo off
rem Schedule this script with schtasks, cron, etc.
python C:/path/to/your/python/script.py 1> C:\Path\to\collect\errors.txt 2>&1
exit