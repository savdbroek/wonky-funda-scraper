# Wonky Funda Scraper

This script scrapes property listings from Funda based on a specified funda URL and sends new listings to a Discord channel via a webhook. It's designed to run periodically, checking for new listings and notifying you when they appear. It is not designed to have no bugs. Always make sure to use this within the limitations of [Funda's Terms and Conditions](https://www.funda.nl/en/gebruiksvoorwaarden).

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
  - [Funda Search URL](#funda-search-url)
  - [Discord Webhook](#discord-webhook)
  - [Discord User ID](#discord-user-id)
- [Scheduling with Windows Task Scheduler](#scheduling-with-windows-task-scheduler)
- [Usage](#usage)

## Installation

1. Clone this repository:
   ```git clone https://github.com/savdbroek/wonky-funda-scraper.git```

2. Navigate to the project directory:
   ```cd wonky-funda-scraper```

3. Install the required Python packages:
   ```pip install -r requirements.txt```

4. Download the appropriate [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/) for your version of Chrome and place it in the project directory or in your system's PATH.

## Configuration

### Funda Search URL

1. Navigate to (https://funda.nl)
2. Enter any search query you like (pro tip, include a radius for the search).
3. Click search.
4. Add any filters you need.
5. Finally add the filter to only show houses that have been posted in the last 24-hours.
5. When you are happy with your search result, copy the full URL and place it within the correct variable in the script. e.g.

```URL = "https://www.funda.nl/zoeken/koop/?selected_area=%5B%22zwolle%22%5D"```

### Discord Webhook

1. Go to your Discord server settings.
2. Navigate to the `Integrations` tab.
3. Click on `Webhooks` and then `New Webhook`.
4. Set up the name, channel where messages will be sent, and copy the Webhook URL.
5. Replace the `WEBHOOK_URL` value in the script with your copied Webhook URL.

### Discord User ID

1. Go to your Discord settings.
2. Under the `Appearance` tab, enable `Developer Mode`.
3. Right-click on any user in your server and select `Copy ID`.
4. Replace the user IDs in the script with the copied IDs to tag these users in the notification.

## Scheduling with Windows Task Scheduler

1. Open `Task Scheduler` from the Start menu.
2. In the Actions pane, click `Create Basic Task`.
3. Name your task and provide a description if desired.
4. Check the box "run whether user is logged on or not" to hide the Command Prompt.
5. Choose the `Trigger`, for example every 30 minutes.
6. In the `Action` step, select `Start a program`.
7. Browse and select your Python executable path (e.g., C:/Users/USER/AppData/Local/Programs/Python/Python39/python.exe).
8. In the `Add arguments` field, input the path to the script, e.g., C:/projects/wonky-funda-scraper/main.py.
9. Finish the setup and your script will run at the specified intervals.

## Usage

Once everything is set up and the task is scheduled, the script will run automatically at the specified intervals. When new listings are found, they will be sent to the specified Discord channel, tagging the specified users.
