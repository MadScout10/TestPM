import yaml
import json
import time
from pathlib import Path
from telegram import Bot
import asyncio
import os

def parse_allure_results(results_dir="results"):
    CURRENT_TIME = time.time()  # Фиксируем текущее время
    
    stats = {
        "passed": 0,
        "failed": 0,
        "broken": 0,
        "skipped": 0,
        "total": 0
    }

    # Максимальный возраст файлов (в секундах)
    MAX_FILE_AGE = 600  # 10 минут
    
    for result_file in Path(results_dir).glob("*result.*"):
        try:
            file_age = CURRENT_TIME - result_file.stat().st_mtime
            
            if file_age > MAX_FILE_AGE:
                print(f"Пропускаем старый файл: {result_file.name} ({file_age:.0f} сек.)")
                continue
                
            with open(result_file, "r", encoding="utf-8") as f:
                data = json.load(f) if result_file.suffix == ".json" else yaml.safe_load(f)
                
                status = data.get("status", "").lower()
                if status in stats:
                    stats[status] += 1
                    stats["total"] += 1
                    
        except Exception as e:
            print(f"Ошибка при обработке {result_file}: {str(e)}")

    stats["success_rate"] = (stats["passed"] / stats["total"] * 100) if stats["total"] > 0 else 0
    return stats

async def send_telegram_report(token, chat_id, report, report_url=None):
    bot = Bot(token=token)
    message = (
        "Привет, работяги)\n"
        "📊 Результаты ПОСЛЕДНЕГО прогона\n"
        f"✅ Успешно: {report['passed']}\n"
        f"❌ Упавшие: {report['failed']}\n"
        f"⚠️ Проблемные: {report['broken']}\n"
        f"⏩ Пропущенные: {report['skipped']}\n"
        f"🔢 Всего тестов: {report['total']}\n"
        f"📈 Успешность: {report['success_rate']:.2f}%"
    )
    if report_url:
        message += f"\n📄 [View Full Report]({report_url})"
    await bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")

if __name__ == "__main__":
    report = parse_allure_results()
    asyncio.run(
        send_telegram_report(
            os.getenv("TELEGRAM_BOT_TOKEN"),
            os.getenv("TELEGRAM_CHAT_ID"),
            report
        )
    )
