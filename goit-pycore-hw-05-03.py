
import sys
import os
from collections import Counter

def parse_log_line(line: str) -> dict:

    parts = line.strip().split(" ", 3)
    if len(parts) < 4:
        return {}
    date, time, level, message = parts
    return {"date": date, "time": time, "level": level.upper(), "message": message}

def load_logs(file_path: str) -> list[dict]:

    try:
        with open(file_path, encoding="utf-8") as f:
            logs = [
                parsed
                for line in f
                if (parsed := parse_log_line(line))   
            ]
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не знайдено: '{file_path}'")
    except OSError as e:
        raise OSError(f"Помилка читання файлу: {e}")

    if not logs:
        raise ValueError(f"Файл '{file_path}' не містить коректних записів.")

    return logs

def filter_logs_by_level(logs: list[dict], level: str) -> list[dict]:
    return list(filter(lambda log: log["level"] == level.upper(), logs))

def count_logs_by_level(logs: list[dict]) -> dict[str, int]:
    return dict(Counter(log["level"] for log in logs))

def display_log_counts(counts: dict[str, int]) -> None:

    col_level = "Рівень логування"
    col_count = "Кількість"
    width = max(len(col_level), max(len(k) for k in counts))

    print(f"\n{col_level:<{width}} | {col_count}")
    print(f"{'-' * width}-|-{'-' * len(col_count)}")

    order = ["INFO", "DEBUG", "ERROR", "WARNING"]
    sorted_levels = sorted(counts, key=lambda lvl: (order.index(lvl) if lvl in order else 99, lvl))
    for level in sorted_levels:
        print(f"{level:<{width}} | {counts[level]}")

def main() -> None:
    if len(sys.argv) < 2:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        log_file = next(
            (os.path.join(script_dir, f) for f in os.listdir(script_dir)
             if f.lower().endswith(".log")),
            None
        )
        if log_file:
            file_path = log_file
        else:
            print("Використання: python main.py <шлях_до_логу> [рівень]")
            sys.exit(1)
        filter_level = None
    else:
        file_path    = sys.argv[1]
        filter_level = sys.argv[2].upper() if len(sys.argv) >= 3 else None

    try:
        logs = load_logs(file_path)

    except (FileNotFoundError, OSError, ValueError) as e:
        print(f"Помилка: {e}")
        sys.exit(1)

    counts = count_logs_by_level(logs)
    display_log_counts(counts)

    if filter_level:
        filtered = filter_logs_by_level(logs, filter_level)
        print(f"\nДеталі логів для рівня '{filter_level}':")
        if filtered:
            for log in filtered:
                print(f"{log['date']} {log['time']} - {log['message']}")
        else:
            print(f"  Записів рівня '{filter_level}' не знайдено.")


if __name__ == "__main__":
    main()