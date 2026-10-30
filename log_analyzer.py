#!/usr/bin/env python3
"""
Log Analyzer & Error Triage Tool
Author: Dmitrii
Description: Parses application/server log files, extracts errors and warnings,
             normalizes messages, and generates a ranked triage report.
"""

import argparse
from collections import Counter
from pathlib import Path
import re
import sys

# Стандартный паттерн для логов вида: 2026-10-29 12:34:56 [ERROR] Connection timeout
LOG_PATTERN = re.compile(
    r'^(?P<timestamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s+'
    r'\[(?P<level>ERROR|WARNING|INFO|DEBUG)\]\s+'
    r'(?P<message>.*)$'
)

def parse_logs(file_path: Path):
    """Читает лог-файл построчно, фильтрует и агрегирует ошибки и предупреждения."""
    stats = Counter()
    total_lines = 0
    parsed_lines = 0

    if not file_path.exists():
        print(f"Ошибка: Файл '{file_path}' не найден.", file=sys.stderr)
        sys.exit(1)

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            total_lines += 1
            match = LOG_PATTERN.match(line.strip())
            if match:
                parsed_lines += 1
                data = match.groupdict()
                level = data['level']
                message = data['message']

                # Фокусируемся на инцидентах (ERROR и WARNING)
                if level in ('ERROR', 'WARNING'):
                    # Нормализация: убираем конкретные ID/числа для правильной группировки
                    normalized_msg = re.sub(r'\b\d+\b', '<NUM>', message)
                    stats[(level, normalized_msg)] += 1

    return total_lines, parsed_lines, stats

def generate_report(file_path: Path, total_lines: int, parsed_lines: int, stats: Counter, top_n: int):
    """Выводит структурированный отчет в консоль."""
    print("=" * 65)
    print(f" ОТЧЕТ АНАЛИЗА ЛОГОВ: {file_path.name}")
    print("=" * 65)
    print(f" Всего строк просканировано: {total_lines}")
    print(f" Успешно распарсено строк:    {parsed_lines}")
    print(f" Пропущено/Другие форматы:   {total_lines - parsed_lines}")
    print("-" * 65)

    if not stats:
        print(" Критических ошибок или предупреждений не обнаружено!")
        return

    print(f" ТОП-{top_n} ПРОБЛЕМ ПО ЧАСТОТЕ ВХОЖДЕНИЯ:")
    print("-" * 65)
    
    sorted_issues = stats.most_common(top_n)
    for idx, ((level, msg), count) in enumerate(sorted_issues, 1):
        print(f"{idx}. [{level}] Встречалось раз: {count}")
        print(f"   Шаблон: {msg}")
        print()
    print("=" * 65)

def main():
    parser = argparse.ArgumentParser(description="Интеллектуальный анализатор логов для инженеров техподдержки")
    parser.add_argument("logfile", type=Path, help="Путь к файлу лога для анализа")
    parser.add_argument("-n", "--top", type=int, default=10, help="Количество топовых проблем для вывода (по умолчанию: 10)")
    args = parser.parse_args()

    total, parsed, stats = parse_logs(args.logfile)
    generate_report(args.logfile, total, parsed, stats, args.top)

if __name__ == "__main__":
    main()