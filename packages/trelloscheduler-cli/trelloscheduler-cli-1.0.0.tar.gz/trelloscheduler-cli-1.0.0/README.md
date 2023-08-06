# trelloscheduler-cli
Bot for automating schedule management in Trello.  Intended use is to place the bot skeleton on a cloud server, set up commands with cron, and let it do 
its thing.

Primarily a personal project, but if you can use it by all means do.  

## Supported features:
1. buildweek - Builds the infrastructure (a "Weekly Schedule" board and "Recycle Bin" board) for the bot.
2. startweek - Starts the week by adding empty lists with the day names and dates to the "Weekly Schedule" board.
3. endweek - Archives the lists in "Weekly Schedule" by moving them to the "Recycle Bin" (AFAIK you can't delete boards through the API)
4. loadweek - Loads a schedule file to add to the "Weekly Schedule" board.  Currently supports named days and numerical days.

## Usage:

*[Usage]*

 ``` trelloschedulercli [command : startweek OR buildweek OR endweek OR loadweek] [schedule file IF loadweek]```
 
  Trello scheduler CLI is a command line interface used to automate tasks related to creating a weekly schedule in Trello.
  All you need is a valid Trello account to access the various commands.
  
*[Commands]*

  **buildweek**
  
  EX: ```trelloschedulercli buildweek```

  Create a new weekly schedule board and recycle bin board.  They will show up as "Weekly Schedule"
 and "Recycle Bin" in Trello.
  Does not need to be executed more than once.

  **startweek**
  
  EX: ```trelloschedulercli startweek```

  Starts a week by adding empty lists to the "Weekly Schedule" board.

  **endweek**
  
  EX: ```trelloschedulercli endweek```

  Archives all of the lists in the "Weekly Schedule" board.

  **loadweek**
  
  EX: ```trelloschedulercli loadweek "filename"```

  Loads a schedule file in JSON format into the "Weekly Schedule" board.
  Currently supports named days and numerical days.

## Installation:
0. Install the Trello Scheduler CLI through pip as shown above.
1.  Run ```nano ~/.bashrc``` to open up bash, then add the enivornment variables "TRELLO_API_KEY", "TRELLO_API_SECRET", and "TRELLO_TOKEN".  For more information on getting them, please see: http://www.trello.org/help.html
3.  Run ```python3 trellobotrunner.py buildweek``` to create the necessary infrastructure.

## Schedule.json File

The schedule file follows the following format in JSON:
```
"tasks": [
     {
          "name": "task name",    
          "description": "task description",
          "day": Either shorthand day names "MoTuWeThFrSaSu" or day numbers (for now)
     }
]
```
Please see schedule.json for an example.

## TODO:

1.  Add more options for day parsing, ie multiple days for the same event both comma delimited and day ranges.
2.   Add due dates for tasks.

** These are not planned though, currently I don't need these features. **
