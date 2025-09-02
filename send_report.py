import json
import os
from pathlib import Path
from telegram import Bot
import asyncio

def parse_fresh_results(results_dir="telegram_temp"):
    """Анализирует результаты и возвращает статистику"""
    stats = {"passed": 0, "failed": 0, "broken": 0, "skipped": 0, "total": 0}
    
    for result_file in Path(results_dir).glob("*-result.*"):
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

def should_send_notification(report):
    """Определяет, нужно ли отправлять уведомление"""
    # Отправляем только если есть упавшие или проблемные тесты
    return report.get("failed", 0) > 0 or report.get("broken", 0) > 0

async def send_telegram_report(token, chat_id, report, report_url=None):
    """Отправляет уведомление в Telegram"""
    bot = Bot(token=token)
    
    if report["failed"] > 0 and report["broken"] > 0:
        emoji = "🔥"
        status = "Критические ошибки"
    elif report["failed"] > 0:
        emoji = "❌"
        status = "Упавшие тесты"
    elif report["broken"] > 0:
        emoji = "⚠️"
        status = "Проблемные тесты"
    else:
        emoji = "✅"
        status = "Все тесты прошли успешно"
    
    message = (
        f"{emoji} {status}\n"
        f"✅ Успешно: {report['passed']}\n"
        f"❌ Упавшие: {report['failed']}\n"
        f"⚠️ Проблемные: {report['broken']}\n"
        f"⏩ Пропущенные: {report['skipped']}\n"
        f"🔢 Всего тестов: {report['total']}\n"
        f"📈 Успешность: {report['success_rate']:.2f}%"
    )
    
    if report_url:
        message += f"\n\n📄 Отчет: {report_url}"
    
    await bot.send_message(chat_id=chat_id, text=message)

async def send_success_notification(token, chat_id, report_url=None):
    """Отправляет краткое уведомление об успешном прогоне (опционально)"""
    bot = Bot(token=token)
    message = "✅ Все тесты прошли успешно!"
    if report_url:
        message += f"\n📄 Отчет: {report_url}"
    
    # Раскомментируйте следующую строку, если хотите получать уведомления об успешных прогонах
    # await bot.send_message(chat_id=chat_id, text=message)

if __name__ == "__main__":
    print("Анализ результатов тестов...")
    report = parse_fresh_results()
    print(f"Результаты: {report}")
    
    if should_send_notification(report):
        print("Обнаружены проблемы - отправляем уведомление")
        asyncio.run(send_telegram_report(
            os.getenv("TELEGRAM_BOT_TOKEN"),
            os.getenv("TELEGRAM_CHAT_ID"),
            report,
            os.getenv("ALLURE_REPORT_URL")
        ))
    else:
        print("Все тесты успешны - уведомление не отправляется")
        # Раскомментируйте для отправки успешных уведомлений:
        # asyncio.run(send_success_notification(
        #     os.getenv("TELEGRAM_BOT_TOKEN"),
        #     os.getenv("TELEGRAM_CHAT_ID"),
        #     os.getenv("ALLURE_REPORT_URL")
        # ))
