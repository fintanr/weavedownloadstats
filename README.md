# Weave Download Stats

Update google spreadsheet with the latest release download number, 
overall stars treand, along with some other stats from docker hub.
You need to have a google apps account setup which has access to the
spreadsheet you are writing too.

Set the environment variables as

```
GOOGLE_KEY=<path/to/key>
GOOGLE_EMAIL=<some-prefix>@developer.gserviceaccount.com
WEAVE_STATS_SHEET=Name_of_Spreadsheet
```

and then just call the script.

# Graphs

weave_downloads_graph.R generates a cumulative graph of downloads

## Dependencies

[gspread](https://github.com/burnash/gspread)
[oauth2client](https://github.com/google/oauth2client)
