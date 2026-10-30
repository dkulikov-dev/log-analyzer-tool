# Log Analyzer & Error Triage Tool

A lightweight, dependency-free Python CLI tool designed for support engineers, SREs, and backend developers to quickly parse, triage, and summarize errors and warnings from application or server logs.

## 🚀 Features

- **Regex-based Parsing:** Extracts timestamps, log levels (`ERROR`, `WARNING`, `INFO`, `DEBUG`), and messages.
- **Error Normalization:** Automatically strips dynamic data (such as specific IDs or numbers) using regular expressions to group identical error patterns accurately.
- **Ranked Triage Report:** Aggregates issues and lists the top most frequent errors to help engineers prioritize troubleshooting (Root Cause Analysis).
- **Zero Dependencies:** Built entirely with Python standard library (`argparse`, `re`, `collections`, `pathlib`) — no external packages (`pip install`) required.

## 📋 Requirements

- Python 3.6 or higher

## ⚙️ Usage

Run the script from the command line by passing the path to your log file:

```bash
python log_analyzer.py path/to/your/logfile.log

Options
-n, --top: Specify how many top issues to display (default: 10).

Example:

Bash
py log_analyzer.py sample.log -n 3
📊 Sample Output
Plaintext
=================================================================
 ОТЧЕТ АНАЛИЗА ЛОГОВ: sample.log
=================================================================
 Всего строк просканировано: 10
 Успешно распарсено строк:    10
 Пропущено/Другие форматы:   0
-----------------------------------------------------------------
 ТОП-3 ПРОБЛЕМ ПО ЧАСТОТЕ ВХОЖДЕНИЯ:
-----------------------------------------------------------------
1. [ERROR] Встречалось раз: 3
   Шаблон: Database connection failed to host db.internal:<NUM>

2. [ERROR] Встречалось раз: 2
   Шаблон: Failed to process payment for transaction_id=<NUM>: Timeout

3. [WARNING] Встречалось раз: 1
   Шаблон: High memory usage detected: <NUM>% on node-<NUM>

=================================================================
🛠️ Author
Created by Dmitrii. Feel free to use and adapt this tool for your operational workflows!