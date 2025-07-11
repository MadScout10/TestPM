import json
import os
import shutil
from pathlib import Path
from telegram import Bot
import asyncio

def prepare_telegram_report(source_dir="results", target_dir="telegram_report"):
    """Копирует только свежие результаты в отдельную папку"""
    Path(target_dir).mkdir(exist_ok=True)
    
    # Очищаем предыдущие отчеты
    for f in Path(target_dir).glob("*"):
        f.unlink()
    
    # Копируем только result-файлы
    for result_file in Path(source_dir).glob("*result.*"):
        shutil.copy2(result_file, target_dir)
    
    return target_dir

def parse_report_files(report_dir):
    stats = {"passed": 0, "failed": 0, "broken": 0, "skipped": 0, "total": 0}
    
    for result_file in Path(report_dir).glob("*"):
        try:
            with open(result_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                status = data.get("status", "").lower()
                
                if status in stats:
                    stats[status] += 1
                    stats["total"] += 1
        except Exception as e:
            print(f"Ошибка обработки {result_file}: {str(e)}")
    
    stats["success_rate"] = (stats["passed"] / stats["total"] * 100) if stats["total"] > 0 else 0
    return stats

async def send_to_telegram(token, chat_id, report):
    bot = Bot(token=token)
    message = (
        "📊 Актуальные результаты\n"
        f"✅ Успешно: {report['passed']}\n"
        f"❌ Упавшие: {report['failed']}\n"
        f"⚠️ Проблемные: {report['broken']}\n"
        f"⏩ Пропущенные: {report['skipped']}\n"
        f"🔢 Всего тестов: {report['total']}\n"
        f"📈 Успешность: {report['success_rate']:.2f}%"
    )
    await bot.send_message(chat_id=chat_id, text=message)

if __name__ == "__main__":
    report_dir = prepare_telegram_report()
    report = parse_report_files(report_dir)
    
    asyncio.run(send_to_telegram(
        os.getenv("TELEGRAM_BOT_TOKEN"),
        os.getenv("TELEGRAM_CHAT_ID"),
        report
    ))
    
