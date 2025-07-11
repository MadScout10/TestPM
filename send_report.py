import yaml
import json
import time
from pathlib import Path
from telegram import Bot
import asyncio
import os

def parse_allure_results(results_dir="results"):
    print(f"\nАнализируем ТОЛЬКО ПОСЛЕДНИЙ прогон в {results_dir}...")
    
    stats = {
        "passed": 0,
        "failed": 0,
        "broken": 0,
        "skipped": 0,
        "total": 0
    }

    # Получаем только самые свежие файлы (сортировка по времени изменения)
    result_files = sorted(
        Path(results_dir).glob("*result.*"),
        key=lambda f: f.stat().st_mtime,
        reverse=True  # Сначала самые новые
    )

    if not result_files:
        return {"error": "No result files found"}

    # Берем только файлы, созданные в последние 10 минут
    latest_files = [
        f for f in result_files
        if time.time() - f.stat().st_mtime < 600
    ]

    for result_file in latest_files:
        try:
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
        f"📊 *Test Results Report*\n"
        f"✅ Passed: {report['passed']}\n"
        f"❌ Failed: {report['failed']}\n"
        f"⚠️ Broken: {report['broken']}\n"
        f"⏭ Skipped: {report['skipped']}\n"
        f"🔢 Total: {report['total']}\n"
        f"📈 Success Rate: {report['success_rate']:.2f}%"
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
