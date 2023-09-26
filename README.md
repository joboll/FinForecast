# FinForecast


# README #
Python Module for Stock Forecast 

### What is this repository for? ###

1. This is a portefolio repo to allow external peek into some of my python programming skills.
2. This repo includes an ETL pipeline with analytics made at Transform step.
    - FinForecast Python Module
        - FinForecast.ArimaForecast is a wrapper package to make stock forcasting easier with ARIMA model. Similar to R autoARIMA, but finer grained and some transformation functions.
        - FinForecast.BackTraderStrategy WIP of a BackTrader Module wrapper to ease use in the context of our investment strategy. Still in progress.
        - FinForecast.DcStats includes useful reusable functions to keep code clean
        - FinForecast.Historical_stock include extracting functions to return stock data.
        - FinForecast.InvestStrat WIP impletementing the logic of a potential investment strategy automation.
        - FinForecast.Share include functions to automate the Loading part of the pipeline.
    - Scripts to be Cron into production. 
        - Note: I had a Cron job running the gSheet_post_ohlc.script.py script on a Raspberry Pi for 2 years.

### How do I get set up? ###

* Install Anaconda or miniConda to create virtual environment and manage package easily
* Create a venv using the requirements.txt as a reference to install required dependencies ($ conda create --name <env> --file requirements.txt)


### Contribution guidelines ###

* I stoped working on that project, but if you're interested in reviving it, feel free to contact me.

### Who do I talk to? ###

* Repo owner: Jonathan Beaulieu, finboys.news@gmail.com
