import xml.etree.ElementTree as ET
import os
from telegram import Bot
import asyncio

def parse_junit_xml(xml_file="test-results.xml"):
    """Парсит JUnit XML отчет (последний запуск перезаписывает предыдущий)"""
    stats = {"passed": 0, "failed": 0, "skipped": 0, "errors": 0, "xfailed": 0, "total": 0}
    
    if not os.path.exists(xml_file):
        return {"error": "JUnit XML отчет не найден"}
    
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Получаем общую статистику
        stats["total"] = int(root.get('tests', 0))
        stats["passed"] = int(root.get('passed', 0))
        stats["failed"] = int(root.get('failed', 0))
        stats["skipped"] = int(root.get('skipped', 0))
        stats["errors"] = int(root.get('errors', 0))
        
        # Считаем xfailed
        for testcase in root.findall('.//testcase'):
            skip_node = testcase.find('skipped')
            if skip_node is not None:
                message = skip_node.get('message', '').lower()
                if 'xfail' in message or 'expected fail' in message:
                    stats["xfailed"] += 1
        
        # Корректируем skipped (исключаем xfailed)
        stats["skipped"] = max(0, stats["skipped"] - stats["xfailed"])
        
    except Exception as e:
        return {"error": f"Ошибка парсинга XML: {str(e)}"}
    
    # Успешность считаем на основе выполненных тестов
    executed_tests = stats["passed"] + stats["failed"] + stats["errors"]
    stats["success_rate"] = (stats["passed"] / executed_tests * 100) if executed_tests > 0 else 0
    
    return stats

async def send_telegram_report(token, chat_id, report):
    """Отправляет уведомление в Telegram"""
    bot = Bot(token=token)
    
    if "error" in report:
        message = f"❌ Ошибка: {report['error']}"
    else:
        message = (
            "📊 Итоги тестирования\n"
            f"✅ Успешно: {report['passed']}\n"
            f"❌ Упавшие: {report['failed']}\n"
            f"⚠️ Ошибки: {report['errors']}\n"
            f"⏩ Пропущенные: {report['skipped']}\n"
            f"🔶 XFAIL: {report['xfailed']}\n"
            f"🔢 Всего тестов: {report['total']}\n"
            f"📈 Успешность: {report['success_rate']:.2f}%"
        )
    
    await bot.send_message(chat_id=chat_id, text=message)

if __name__ == "__main__":
    print("Парсинг JUnit XML отчета...")
    report = parse_junit_xml()
    print(f"Результаты: {report}")
    
    asyncio.run(send_telegram_report(
        os.getenv("TELEGRAM_BOT_TOKEN"),
        os.getenv("TELEGRAM_CHAT_ID"),
        report
    ))
    
