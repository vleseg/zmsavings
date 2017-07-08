# Zenmoney Savings Visualizer

## What's This? / Что это такое?

**Zenmoney Savings Visualizer**, or **ZMSV**, or **zmsavings** is a Python-based tool to visualize growth of your special-purpose savings account within the [Zenmoney personal accounting service](https://zenmoney.ru).

--------------------------------------

**Zenmoney Savings Visualizer**, также **ZMSV** или **zmsavings** — это написанный на Python инструмент для визуализации процесса накопления средств на накопительном счёте в сервисе [Дзен-мани](https://zenmoney.ru).

## How Does It Work / Как это работает

* It uses Zenmoney's OAuth for authentication.
* It uses Zenmoney's API to fetch accounts and savings goals; goals with linked account are then passed further.
* It extracts all transactions for the account and passes them further for visualization.

--------------------------------------

* Для аутентификации используется протокол OAuth.
* Через API Zenmoney достаются счета и цели, затем цели, связанные с каким-нибудь счётом передаются для дальнейшей обработки.
* Скрипт получает все транзакции для счёта и передаёт их дальше для визуализации.