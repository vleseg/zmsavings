# Zenmoney Savings Visualizer

## What's This? / Что это такое?

**Zenmoney Savings Visualizer**, or **ZMSV**, or **zmsavings** is a Python-based tool to visualize growth of your special-purpose savings account within the [Zenmoney personal accounting service](https://zenmoney.ru).

--------------------------------------

**Zenmoney Savings Visualizer**, также **ZMSV** или **zmsavings** — это написанный на Python инструмент для визуализации процесса накопления средств на накопительном счёте в сервисе [Дзен-мани](https://zenmoney.ru).

## How Does It Work / Как это работает

* It loads goals from CSV file of special format (this file should contains the following headers: goalName, accountName, total).
* It loads transactions from CSV transaction dump, which can be exported manually from within Zenmoney webapp GUI.
* It extracts all transactions of special-purpose savings accounts and passes them further for visualization.

--------------------------------------

* Цели накопления загружаются из особым образом структурированного CSV-файла (необходимые заголовки: goalName, accountName, total).
* Транзакции загружаются из дампа транзакций, который можно сформировать вручную в веб-приложении "Дзен-мани" (*ещё* -> *Экспорт* в строке навигации).
* Извлекаются все транзакции по целевым накопительным счетам и передаются дальше для визуализации.

## TODO
* Authenticate via OAuth and retrieve data via Zenmoney API