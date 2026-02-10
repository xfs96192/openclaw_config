# AI and GitHub Daily Report Setup

This guide explains how to set up a cron job to run the AI and GitHub daily report every weekday at 9 AM.

## Scripts Location

- Main Python script: `/Users/fanshengxia/clawd/scripts/ai_github_daily_report.py`
- Execution wrapper: `/Users/fanshengxia/clawd/scripts/run_ai_daily_report.sh`

## To Schedule the Task

Since the Clawdbot cron functionality appears to be having connection issues, please manually add the following entry to your system's crontab:

1. Open terminal and run: `crontab -e`
2. Add the following line to schedule the task for weekdays at 9 AM:
   ```
   0 9 * * 1-5 /Users/fanshengxia/clawd/scripts/run_ai_daily_report.sh
   ```
3. Save and exit the editor

## Cron Expression Breakdown

- `0`: At minute 0
- `9`: At hour 9 (9 AM)
- `*`: Every day of the month
- `*`: Every month
- `1-5`: Only on weekdays (Monday through Friday)

## Notes

- The script will search for the latest AI developments and trending GitHub projects
- Output will appear in the terminal (you can modify the script to log to a file if desired)
- The script uses your configured Anaconda Python environment

## Troubleshooting

If the script fails to run:
1. Ensure the execution wrapper has proper permissions: `chmod +x /Users/fanshengxia/clawd/scripts/run_ai_daily_report.sh`
2. Verify the paths in the execution wrapper script are correct
3. Test the script manually: `/Users/fanshengxia/clawd/scripts/run_ai_daily_report.sh`