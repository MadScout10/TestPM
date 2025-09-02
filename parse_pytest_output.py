import os
from telegram import Bot
import asyncio

def parse_pytest_log():
    """Парсит объединенный лог всех тестов"""
    log_file = "pytest_output.log"
    
    if not os.path.exists(log_file):
        return {"error": "Лог тестов не найден"}, ""
    
    with open(log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    return parse_pytest_content(content), content

def parse_pytest_content(content):
    """Парсит содержимое лога pytest"""
    stats = {"passed": 0, "failed": 0, "skipped": 0, "xfailed": 0, "total": 0}
    
    lines = content.split('\n')
    
    # Счетчики из вывода тестов
    for line in lines:
        if line.startswith('FAILED') or '.py::' in line and 'FAILED' in line:
            stats["failed"] += 1
            stats["total"] += 1
        elif line.startswith('PASSED') or '.py::' in line and 'PASSED' in line:
            stats["passed"] += 1
            stats["total"] += 1
        elif line.startswith('SKIPPED') or '.py::' in line and 'SKIPPED' in line:
            stats["skipped"] += 1
            stats["total"] += 1
        elif 'XFAIL' in line or 'xfail' in line:
            stats["xfailed"] += 1
            stats["total"] += 1
    
    # Ищем итоговые строки (могут быть несколько для каждого запуска)
    for line in lines:
        if 'passed' in line and 'failed' in line and ('in' in line or 'seconds' in line):
            try:
                # Пример: "12 passed, 3 failed, 2 skipped in 45.12s"
                parts = line.split()
                for i, part in enumerate(parts):
                    if part.isdigit():
                        count = int(part)
                        if i + 1 < len(parts):
                            if 'passed' in parts[i+1]:
                                stats["passed"] = count
                            elif 'failed' in parts[i+1]:
                                stats["failed"] = count
                            elif 'skipped' in parts[i+1]:
                                stats["skipped"] = count
                            elif 'xfailed' in parts[i+1]:
                                stats["xfailed"] = count
            except (ValueError, IndexError):
                continue
    
    stats["total"] = stats["passed"] + stats["failed"] + stats["skipped"] + stats["xfailed"]
    stats["success_rate"] = (stats["passed"] / stats["total"] * 100) if stats["total"] > 0 else 0
    
    return stats

async def send_telegram_report(token, chat_id, report):
    """Отправляет уведомление в Telegram"""
    bot = Bot(token=token)
    
    if "error" in report:
        message = f"❌ Ошибка парсинга: {report['error']}"
    else:
        message = (
            "📊 Сводка всех тестов\n"
            f"✅ Успешно: {report['passed']}\n"
            f"❌ Упавшие: {report['failed']}\n"
            f"⏩ Пропущенные: {report['skipped']}\n"
            f"🔶 XFAIL: {report['xfailed']}\n"
            f"🔢 Всего тестов: {report['total']}\n"
            f"📈 Успешность: {report['success_rate']:.2f}%"
        )
    
    await bot.send_message(chat_id=chat_id, text=message)

if __name__ == "__main__":
    print("Парсинг логов pytest...")
    report, content = parse_pytest_log()
    print(f"Результаты: {report}")
    
    asyncio.run(send_telegram_report(
        os.getenv("TELEGRAM_BOT_TOKEN"),
        os.getenv("TELEGRAM_CHAT_ID"),
        report
    ))

