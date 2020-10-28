"""Main handler for clients"""
# Created by Жасулан Бердибеков <zhasulan87@gmail.com> at 10/28/20 9:33 PM
from time import sleep

from app import logger


def handler(code, content):
    """
    Здесь вы должны писать собственный обработчик

    Каждый code - это отдельный сервис ПКБ и каждый из них должен обрабатываться отдельно или высылаться в другую
    программу

    if code == 'MON':  # Банковский мониторинг
        mon_handler(content)
    if code == 'BCO':  # Бэкофис ПКБ
        bco_handler(content)

    и т.д.

    :rtype: object
    """
    sleep(10)
    # Конвертируем byte в string
    content = content.decode("utf-8")
    logger.info("Сообщение обработано. Код: %s; Контент: %s", code, content)
