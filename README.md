# Zenmoney Savings Visualizer

## What's This?

**Zenmoney Savings Visualizer**, or **ZMSV**, or **zmsavings** is a Python-based tool to visualize growth of your special-purpose savings account within the [Zenmoney personal accounting service](https://zenmoney.ru).

## How Does It Work?

* It loads goals from CSV file of special format (this file should contains the following headers: goalName, accountName, total).
* It loads transactions from CSV transaction dump, which can be exported manually from within Zenmoney webapp GUI (*ещё* -> *Экспорт* in the upper navigation menu).
* It extracts all transactions of special-purpose savings accounts, calculates progressive total, and passes it further for visualization.
* Visualization is done with the help of [Bokeh](http://bokeh.pydata.org/en/latest/) library.

## How Do I Use It?

1. [Download](https://www.python.org/downloads/) and install Python 2.7.
2. Clone this repository into folder of your choice:

        git clone https://github.com/vleseg/zmsavings.git <LOCAL_REPO_FOLDER>
3. Install virtualenv:

        pip install virtualenv
4. Use it to create virtual environment in another folder of your choice.

        cd <VENV_FOLDER_PARENT>
        virtualenv <VENV_FOLDER>
5. Activate the virtual environment.

        (Windows) <VENV_FOLDER>\Scripts\activate
        (Linux)   source <VENV_FOLDER>\bin\activate
6. Install the requirements (might take some time):

        cd <LOCAL_REPO_FOLDER>
        pip install -r requirements.txt
7. Export CSV with all transactions in the Zenmoney GUI (*ещё* -> *Экспорт* in the upper navigation menu).
8. Compose a CSV with goals, see table format below.
9. Run the script (you'll be prompted for paths to transactions CSV and goals CSV:

        cd <LOCAL_REPO_FOLDER>
        python core.py

In the bright future everything should become much more simpler, I promise :)

## CSV Goals Table Format

goalName | accountName | total | startDate
-------- | ----------- | ----- | ---------
\<goal name in ZM\> | \<name of goal account in ZM\> | \<goal total\> | \<goal start date in format DD.MM.YYYY\>
