# sumup
stock price visualization

## requirements
* <code>python3.6</code>
* <code>sqlite3</code>

## instructions
*  install and create a virtual environment (optional): <br>
   <code>$pip3.6 install virtualenv</code> <br>
   <code>$virtualenv -p python3.6 venv</code> <br>
   <code>$source venv/bin/activate</code> <br>

*  install dependencies: <br>
   <code>$pip3.6 install -r requirements.txt</code>

*  run the server: <br>
   <code>$python3.6 run.py</code>

* the server can be accessed at [http://localhost:7777/](http://localhost:7777/)

## logic
* uses flask as a web framework, sqlalchemy as an orm
* the tickers table is an in memory db which stores all the tickers and is used for autocomplete lookup
* the chart data is obtained using quandl api and has different granularity based on how far into the past the data is obtained from
* the front end uses bootstrap v4 to design the layout, jquery.autocomplete for the search box autocomplete, toastr to throw error toasts and c3 for rendering the graph
* the graphs are rendered using ajax
