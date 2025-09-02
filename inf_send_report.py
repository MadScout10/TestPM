import json
import os
from pathlib import Path
from telegram import Bot
import asyncio
import time

def parse_infinite_results(results_dir="results"):
    """Анализирует результаты бесконечного прогона с учетом истории"""
    stats = {"passed": 0, "failed": 0, "broken": 0, "skipped": 0, "total": 0}
    latest_files = []
    
    # Получаем все файлы и сортируем по времени изменения
    all_files = list(Path(results_dir).glob("*-result.*"))
    if not all_files:
        return {"error": "No result files found"}
    
    # Сортируем по времени изменения (сначала самые новые)
    all_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    
    # Берем только файлы последнего часа (для бесконечного прогона)
    current_time = time.time()
    for result_file in all_files:
        file_age = current_time - result_file.stat().st_mtime
        if file_age < 3600:  # Файлы младше 1 часа
            latest_files.append(result_file)
        else:
            break
    
    # Анализируем только свежие файлы
    for result_file in latest_files:
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
    stats["files_analyzed"] = len(latest_files)
    return stats

def should_send_notification(report):
    """Для бесконечного прогона отправляем уведомления реже"""
    # Отправляем только при серьезных проблемах или раз в N прогонов
    return report.get("failed", 0) > 2 or report.get("broken", 0) > 1

async def send_infinite_telegram_report(token, chat_id, report, report_url=None):
    """Специальное уведомление для бесконечного прогона"""
    bot = Bot(token=token)
    
    if report.get("error"):
        message = f"❌ Ошибка в бесконечном прогоне: {report['error']}"
    else:
        message = (
            "♾️ Бесконечный прогон - Статистика\n"
            f"⏰ Анализ: последний час\n"
            f"📊 Файлов проанализировано: {report['files_analyzed']}\n"
            f"✅ Успешно: {report['passed']}\n"
            f"❌ Упавшие: {report['failed']}\n"
            f"⚠️ Проблемные: {report['broken']}\n"
            f"📈 Успешность: {report['success_rate']:.2f}%"
        )
        
        if report_url:
            message += f"\n\n📄 Полный отчет: {report_url}"
    
    await bot.send_message(chat_id=chat_id, text=message)

if __name__ == "__main__":
    print("Анализ результатов бесконечного прогона...")
    report = parse_infinite_results()
    print(f"Результаты: {report}")
    
    if should_send_notification(report):
        print("Отправляем уведомление о прогоне")
        asyncio.run(send_infinite_telegram_report(
            os.getenv("TELEGRAM_BOT_TOKEN"),
            os.getenv("TELEGRAM_CHAT_ID"),
            report,
            os.getenv("ALLURE_REPORT_URL")
        ))
    else:
        print("Уведомление не требуется (мало ошибок)")
