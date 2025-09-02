import json
import os
from pathlib import Path
from telegram import Bot
import asyncio

def parse_allure_results(results_dir="results"):
    """Анализирует ВСЕ результаты из основной папки"""
    stats = {"passed": 0, "failed": 0, "broken": 0, "skipped": 0, "total": 0, "xfailed": 0}
    
    # Анализируем все файлы в основной папке results
    for result_file in Path(results_dir).glob("*-result.*"):
        try:
            with open(result_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                status = data.get("status", "").lower()
                
                # Обрабатываем xfailed (expected failure)
                if status == "skipped" and data.get("name", "").lower().startswith("xfail"):
                    stats["xfailed"] += 1
                    stats["skipped"] += 1
                elif status in stats:
                    stats[status] += 1
                
                stats["total"] += 1
                
        except Exception as e:
            print(f"Ошибка обработки {result_file}: {str(e)}")
    
    stats["success_rate"] = (stats["passed"] / (stats["total"] - stats["xfailed"]) * 100) if (stats["total"] - stats["xfailed"]) > 0 else 0
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
    
    # Добавляем информацию о xfailed, если есть
    if report.get("xfailed", 0) > 0:
        message += f"\n🔶 Ожидаемые падения: {report['xfailed']}"
    
    if report_url:
        message += f"\n\n📄 Отчет: {report_url}"
    
    await bot.send_message(chat_id=chat_id, text=message)

if __name__ == "__main__":
    print("Анализ результатов тестов из папки results...")
    report = parse_allure_results("results")  # Анализируем основную папку!
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
