import xml.etree.ElementTree as ET
import os
from telegram import Bot
import asyncio

def parse_junit_xml(xml_file="test-results.xml"):
    """Парсит JUnit XML отчет"""
    stats = {"passed": 0, "failed": 0, "skipped": 0, "errors": 0, "total": 0}
    
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Получаем атрибуты из корневого элемента
        stats["passed"] = int(root.get('passed', 0))
        stats["failed"] = int(root.get('failed', 0))
        stats["skipped"] = int(root.get('skipped', 0))
        stats["errors"] = int(root.get('errors', 0))
        stats["total"] = int(root.get('tests', 0))
        
        # Считаем xfailed отдельно
        stats["xfailed"] = 0
        for testcase in root.findall('.//testcase'):
            if testcase.find('skipped') is not None:
                message = testcase.find('skipped').get('message', '')
                if 'xfail' in message.lower():
                    stats["xfailed"] += 1
        
    except Exception as e:
        return {"error": f"Ошибка парсинга XML: {str(e)}"}
    
    stats["success_rate"] = (stats["passed"] / stats["total"] * 100) if stats["total"] > 0 else 0
    return stats

