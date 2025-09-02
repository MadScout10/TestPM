import subprocess
import os
from telegram import Bot
import asyncio

def run_tests_and_parse():
    """Запускает тесты и парсит вывод напрямую"""
    try:
        # Запускаем тесты и получаем вывод
        result = subprocess.run(
            ['pytest', '-v', '-m', 'smoke', '--tb=short'],
            capture_output=True,
            text=True,
            timeout=3600  # 1 час таймаут
        )
        
        # Парсим вывод
        output = result.stdout + result.stderr
        return parse_pytest_output(output), output
        
    except subprocess.TimeoutExpired:
        return {"error": "Таймаут выполнения тестов"}, ""
    except Exception as e:
        return {"error": str(e)}, ""

def parse_pytest_output(output):
    """Парсит вывод pytest"""
    stats = {
        "passed": 0,
        "failed": 0, 
        "skipped": 0,
        "xfailed": 0,
        "xpassed": 0,
        "errors": 0,
        "total": 0
    }
    
    lines = output.split('\n')
    for line in lines:
        line = line.strip()
        
        if line.startswith('FAILED'):
            stats["failed"] += 1
            stats["total"] += 1
        elif line.startswith('PASSED'):
            stats["passed"] += 1
            stats["total"] += 1
        elif line.startswith('SKIPPED'):
            stats["skipped"] += 1
            stats["total"] += 1
        elif 'XFAIL' in line:
            stats["xfailed"] += 1
            stats["total"] += 1
        elif 'XPASS' in line:
            stats["xpassed"] += 1
            stats["total"] += 1
        elif 'ERROR' in line:
            stats["errors"] += 1
            stats["total"] += 1
    
    # Дополнительный парсинг для итоговой строки
    for line in reversed(lines):
        if 'passed' in line and 'failed' in line:
            parts = line.split()
            for i, part in enumerate(parts):
                if part == 'passed':
                    stats["passed"] = int(parts[i-1])
                elif part == 'failed':
                    stats["failed"] = int(parts[i-1])
                elif part == 'skipped':
                    stats["skipped"] = int(parts[i-1])
            break
    
    stats["success_rate"] = (stats["passed"] / stats["total"] * 100) if stats["total"] > 0 else 0
    return stats

async def send_telegram_report(token, chat_id, report, raw_output=""):
    """Отправляет уведомление в Telegram"""
    bot = Bot(token=token)
    
    if "error" in report:
        message = f"❌ Ошибка запуска тестов: {report['error']}"
    else:
        message = (
            "🔍 Прямой отчет Selenium\n"
            f"✅ Успешно: {report['passed']}\n"
            f"❌ Упавшие: {report['failed']}\n"
            f"⚠️ Ошибки: {report['errors']}\n"
            f"⏩ Пропущенные: {report['skipped']}\n"
            f"🔶 XFAIL: {report['xfailed']}\n"
            f"🔢 Всего тестов: {report['total']}\n"
            f"📈 Успешность: {report['success_rate']:.2f}%"
        )
    
    # Добавляем краткую информацию об ошибках если есть
    if report.get('failed', 0) > 0 and raw_output:
        failed_tests = []
        lines = raw_output.split('\n')
        for line in lines:
            if 'FAILED' in line and len(failed_tests) < 3:  # Первые 3 упавших теста
                failed_tests.append(line.strip())
        
        if failed_tests:
            message += "\n\n💥 Упавшие тесты:\n" + "\n".join(failed_tests[:3])
    
    await bot.send_message(chat_id=chat_id, text=message)

if __name__ == "__main__":
    print("Запуск Selenium тестов и парсинг результатов...")
    report, raw_output = run_tests_and_parse()
    print(f"Результаты: {report}")
    
    asyncio.run(send_telegram_report(
        os.getenv("TELEGRAM_BOT_TOKEN"),
        os.getenv("TELEGRAM_CHAT_ID"),
        report,
        raw_output
    ))

