import os
import re
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
    """Парсит содержимое лога pytest с улучшенной логикой"""
    stats = {"passed": 0, "failed": 0, "skipped": 0, "xfailed": 0, "deselected": 0, "total": 0}
    
    lines = content.split('\n')
    
    # 1. Парсим итоговые строки (самый надежный способ)
    final_results = []
    for line in reversed(lines):
        if ('passed' in line and 'failed' in line) or ('seconds' in line and ('passed' in line or 'failed' in line)):
            final_results.append(line.strip())
            if len(final_results) >= 3:  # Берем несколько последних итогов
                break
    
    # Обрабатываем все найденные итоговые строки
    for result_line in final_results:
        parse_final_line(result_line, stats)
    
    # 2. Дополнительный парсинг по строчкам (для проверки)
    if stats["total"] == 0:
        for line in lines:
            if 'FAILED' in line and '.py::' in line:
                stats["failed"] += 1
            elif 'PASSED' in line and '.py::' in line:
                stats["passed"] += 1
            elif 'SKIPPED' in line and '.py::' in line:
                stats["skipped"] += 1
            elif 'XFAIL' in line and '.py::' in line:
                stats["xfailed"] += 1
    
    # 3. Расчет общих значений
    stats["total"] = stats["passed"] + stats["failed"] + stats["skipped"] + stats["xfailed"] + stats["deselected"]
    
    # Успешность считаем только на основе выполненных тестов
    executed_tests = stats["passed"] + stats["failed"] + stats["skipped"] + stats["xfailed"]
    stats["success_rate"] = (stats["passed"] / executed_tests * 100) if executed_tests > 0 else 0
    
    return stats

def parse_final_line(line, stats):
    """Парсит итоговую строку pytest"""
    # Различные форматы итоговых строк:
    # "5 passed, 2 failed, 1 skipped, 1 xfailed in 10.20s"
    # "=== 12 passed, 3 failed, 2 skipped in 45.12s ==="
    # "8 passed, 4 deselected in 30.50s"
    
    patterns = {
        'passed': r'(\d+)\s+passed',
        'failed': r'(\d+)\s+failed',
        'skipped': r'(\d+)\s+skipped', 
        'xfailed': r'(\d+)\s+xfailed',
        'deselected': r'(\d+)\s+deselected',
        'errors': r'(\d+)\s+errors'
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, line)
        if match:
            stats[key] = int(match.group(1))

async def send_telegram_report(token, chat_id, report):
    """Отправляет уведомление в Telegram"""
    bot = Bot(token=token)
    
    if "error" in report:
        message = f"❌ Ошибка парсинга: {report['error']}"
    else:
        message = (
            "📊 Итоги тестирования\n"
            f"✅ Успешно: {report['passed']}\n"
            f"❌ Упавшие: {report['failed']}\n"
            f"⏩ Пропущенные: {report['skipped']}\n"
            f"🔶 XFAIL: {report['xfailed']}\n"
            f"🚫 Deselected: {report['deselected']}\n"
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

