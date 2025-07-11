import json
import os
from pathlib import Path
from telegram import Bot
import asyncio

def parse_allure_results(results_dir="telegram_report"):
    stats = {"passed": 0, "failed": 0, "broken": 0, "skipped": 0, "total": 0}
    
    for result_file in Path(results_dir).glob("*result.*"):
        try:
            with open(result_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                status = data.get("status", "").lower()
                if status in stats:
                    stats[status] += 1
                    stats["total"] += 1
        except Exception as e:
            print(f"Error processing {result_file}: {str(e)}")

    stats["success_rate"] = (stats["passed"] / stats["total"] * 100) if stats["total"] > 0 else 0
    return stats

async def send_telegram_report(token, chat_id, report):
    bot = Bot(token=token)
    message = (
        "📊 Результаты последнего прогона\n"
        f"✅ Успешно: {report['passed']}\n"
        f"❌ Упавшие: {report['failed']}\n"
        f"⚠️ Проблемные: {report['broken']}\n"
        f"⏩ Пропущенные: {report['skipped']}\n"
        f"🔢 Всего тестов: {report['total']}\n"
        f"📈 Успешность: {report['success_rate']:.2f}%"
    )
    await bot.send_message(chat_id=chat_id, text=message)

if __name__ == "__main__":
    report = parse_allure_results()
    asyncio.run(send_telegram_report(
        os.getenv("TELEGRAM_BOT_TOKEN"),
        os.getenv("TELEGRAM_CHAT_ID"),
        report
    ))
    
