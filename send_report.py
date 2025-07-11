import yaml
import json
from pathlib import Path
from telegram import Bot
import asyncio
import os
import argparse
import time

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run-id', help='GitHub Actions Run ID', default=None)
    parser.add_argument('--results-dir', help='Path to results directory', default='results')
    return parser.parse_args()

def parse_allure_results(results_dir, run_id=None):
    print(f"\nАнализируем результаты в '{results_dir}' для run_id={run_id}")
    
    stats = {
        "passed": 0,
        "failed": 0,
        "broken": 0,
        "skipped": 0,
        "total": 0
    }

    # Счетчик для отладки
    processed_files = 0

    for result_file in Path(results_dir).glob("*result.*"):
        try:
            # Если передан run_id, проверяем его наличие в имени файла
            if run_id and f"run_{run_id}" not in str(result_file):
                continue
                
            with open(result_file, "r", encoding="utf-8") as f:
                data = json.load(f) if result_file.suffix == ".json" else yaml.safe_load(f)
                
                status = data.get("status", "").lower()
                if status in stats:
                    stats[status] += 1
                    stats["total"] += 1
                    processed_files += 1
                    
                print(f"Обработан {result_file.name}: статус={status}")
                
        except Exception as e:
            print(f"Ошибка при обработке {result_file}: {str(e)}")

    print(f"\nИтого обработано файлов: {processed_files}")
    
    stats["success_rate"] = (stats["passed"] / stats["total"] * 100) if stats["total"] > 0 else 0
    return stats

async def send_telegram_report(token, chat_id, report, report_url=None):
    bot = Bot(token=token)
    
    if "error" in report:
        message = "❌ Ошибка при анализе результатов тестов\n" + report["error"]
    else:
        message = (
            "📊 Результаты ТЕКУЩЕГО прогона\n"
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

if __name__ == "__main__":
    args = parse_args()
    print(f"\nЗапуск анализа результатов (Run ID: {args.run_id})...")
    
    # Добавляем метку run_id в имена файлов (для тестирования)
    if args.run_id:
        test_file = Path(args.results_dir) / f"run_{args.run_id}_test-result.json"
        test_file.touch()
    
    report = parse_allure_results(args.results_dir, args.run_id)
    print("\nИтоговый отчет:", report)
    
    asyncio.run(send_telegram_report(
        os.getenv("TELEGRAM_BOT_TOKEN"),
        os.getenv("TELEGRAM_CHAT_ID"),
        report,
        os.getenv("ALLURE_REPORT_URL")
    ))
    
