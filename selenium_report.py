import json
import os
from pathlib import Path
from telegram import Bot
import asyncio

def parse_existing_pytest_run():
    """Парсит результаты уже выполненных тестов из вывода"""
    # Читаем логи выполнения тестов
    log_file = "pytest_output.log"
    
    if not os.path.exists(log_file):
        return {"error": "Лог тестов не найден"}, ""
    
    with open(log_file, 'r', encoding='utf-8') as f:
        output = f.read()
    
    return parse_pytest_output(output), output

def parse_pytest_output(output):
    """Парсит вывод pytest"""
    stats = {
        "passed": 0,
        "failed": 0, 
        "skipped": 0,
        "xfailed": 0,
        "xpassed": 0,
        "errors": 0,
        "total": 0
    }
    
    # Ищем итоговую строку pytest
    lines = output.split('\n')
    for line in reversed(lines):
        if 'passed' in line and 'failed' in line and '=' in line:
            # Пример: "=== 5 passed, 2 failed, 1 skipped in 10.20s ==="
            try:
                parts = line.split('=')
                if len(parts) >= 2:
                    result_part = parts[-2].strip()
                    for item in result_part.split(','):
                        item = item.strip()
                        if 'passed' in item:
                            stats["passed"] = int(item.split()[0])
                        elif 'failed' in item:
                            stats["failed"] = int(item.split()[0])
                        elif 'skipped' in item:
                            stats["skipped"] = int(item.split()[0])
                        elif 'xfailed' in item:
                            stats["xfailed"] = int(item.split()[0])
                        elif 'xpassed' in item:
                            stats["xpassed"] = int(item.split()[0])
                        elif 'error' in item:
                            stats["errors"] = int(item.split()[0])
                
                stats["total"] = stats["passed"] + stats["failed"] + stats["skipped"] + stats["xfailed"] + stats["xpassed"]
                break
            except (ValueError, IndexError):
                continue
    
    # Если не нашли итоговую строку, парсим по строчкам
    if stats["total"] == 0:
        for line in lines:
            if 'PASSED' in line:
                stats["passed"] += 1
                stats["total"] += 1
            elif 'FAILED' in line:
                stats["failed"] += 1
                stats["total"] += 1
            elif 'SKIPPED' in line:
                stats["skipped"] += 1
                stats["total"] += 1
            elif 'XFAIL' in line:
                stats["xfailed"] += 1
                stats["total"] += 1
    
    stats["success_rate"] = (stats["passed"] / stats["total"] * 100) if stats["total"] > 0 else 0
    return stats

async def send_telegram_report(token, chat_id, report, raw_output=""):
    """Отправляет уведомление в Telegram"""
    bot = Bot(token=token)
    
    if "error" in report:
        message = f"❌ Ошибка: {report['error']}"
    else:
        message = (
            "📊 Результаты тестов\n"
            f"✅ Успешно: {report['passed']}\n"
            f"❌ Упавшие: {report['failed']}\n"
            f"⏩ Пропущенные: {report['skipped']}\n"
            f"🔶 Ожидаемые падения: {report.get('xfailed', 0)}\n"
            f"🔢 Всего тестов: {report['total']}\n"
            f"📈 Успешность: {report['success_rate']:.2f}%"
        )
    
    await bot.send_message(chat_id=chat_id, text=message)

if __name__ == "__main__":
    print("Парсинг результатов уже выполненных тестов...")
    report, raw_output = parse_existing_pytest_run()
    print(f"Результаты: {report}")
    
    asyncio.run(send_telegram_report(
        os.getenv("TELEGRAM_BOT_TOKEN"),
        os.getenv("TELEGRAM_CHAT_ID"),
        report,
        raw_output
    ))

