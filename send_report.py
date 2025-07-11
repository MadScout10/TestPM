import yaml
from pathlib import Path
from telegram import Bot
import asyncio
import os

def parse_allure_results(results_dir="allure-results"):
    passed = failed = broken = skipped = total = 0

    for result_file in Path(results_dir).glob("*-result.yaml"):
        with open(result_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        
        status = data.get("status", "unknown")
        
        if status == "passed":
            passed += 1
        elif status == "failed":
            failed += 1
        elif status == "broken":
            broken += 1
        elif status == "skipped":
            skipped += 1
        total += 1

    return {
        "passed": passed,
        "failed": failed,
        "broken": broken,
        "skipped": skipped,
        "total": total,
        "success_rate": (passed / total * 100) if total > 0 else 0,
    }

async def send_telegram_report(token, chat_id, report, report_url=None):
    bot = Bot(token=token)
    message = (
        "📊 *Test Results Report*\n"
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
