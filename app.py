# Created by Жасулан Бердибеков <zhasulan87@gmail.com> at 10/01/20 7:12 PM
import hashlib
import json
import os
from http import HTTPStatus
from multiprocessing import Process
from time import sleep

import requests
from flask import Flask, request

from authentication import Authentication, Auth
from log import get_logger

app = Flask(__name__)

logger = get_logger()
authentication = None


def file_read(proxy_url, code, filename):
    payload = {
        "code": code,
        "filename": filename
    }
    response = requests.post(proxy_url, data=json.dumps(payload), headers=authentication.bearer_header())
    if response.status_code == HTTPStatus.OK:
        data = response.content
        return data
    else:
        logger.error("CDN прокси вернул ошибку")
        return None


def handler(code, content):
    sleep(10)
    # Конвертируем byte в string
    content = content.decode("utf-8")
    """
    Здесь вы должны писать собственный обработчик
    
    Каждый code - это отдельный сервис ПКБ и каждый из них должен обрабатываться отдельно или высылаться в другую 
    программу
    
    if code == 'MON':  # Банковский мониторинг
        mon_handler(content)
    if code == 'BCO':  # Бэкофис ПКБ
        bco_handler(content)
    
    и т.д.
    """
    logger.info("Сообщение обработано. Код: {}; Контент: {}".format(code, content))
    pass


def create_message_hash(content):
    """
    Этот фрагмент кода предназначен для калькуляции хэш суммы
    content является byte-ом
    """
    return hashlib.sha256(content).hexdigest()


@app.route('/endpoint', methods=["POST"])
def endpoint():
    r = request.json
    code = r['code']
    proxy_url = r['proxy_url']
    filename = r['filename']
    checksum = r['checksum']

    logger.info(
        "Получено сообщение. Код {}; CDN Сервер: {}; Название файла: {}; Заголовок: {}".format(code, proxy_url,
                                                                                               filename, checksum)
    )

    # Чтение контента файла
    content = file_read(proxy_url, code, filename)

    if content is not None:
        # Hash сумма контента файла
        sha256_hash = create_message_hash(content)

        if checksum != sha256_hash:
            logger.error("Вероятно произошло ошибка в чтении файла или неправильно вычислен хэш сумма файла")
            return {
                       "Code": "FAIL",
                       "Status": "Контент не соответствует контрольной сумме"
                   }, HTTPStatus.NOT_ACCEPTABLE

        logger.info("Хэш значения сообщения: {}".format(sha256_hash))
        # Проверка подписи
        # Требуется SDK от НУЦ РК

        try:
            # Лучше создать асинхронный процесс для обработки
            # Время Timeout-а запроса на стороне ПКБ 10s
            Process(target=handler, args=(code, content,)).start()
        except Exception as exc:
            logger.error(exc)

        # Запрос отработан успешно
        # Возвращаем http статус либо OK - 200, либо, если вы используете асинхронную обработку, ACCEPTED - 202
        return {
                   "sha256": sha256_hash
               }, HTTPStatus.ACCEPTED
    else:
        return {
                   "Code": "FAIL",
                   "Status": "Content is None"
               }, HTTPStatus.INTERNAL_SERVER_ERROR


@app.route('/health', methods=["GET"])
def health():
    """

    :rtype: object
    """
    return {
               "Code": HTTPStatus.OK,
               "Status": "ok"
           }, HTTPStatus.OK


if __name__ == '__main__':
    auth = Auth(
           "/login/",
           "/refresh/",
           os.environ['AUTH_USERNAME'],
           os.environ['AUTH_PASSWORD']
    )
    authentication = Authentication(
        "https://notifier.1cb.kz/api/v1",
        auth
    )
    authentication.authorization()

    port = int(os.environ.get("PORT", 9090))
    app.run(host="0.0.0.0", port=port)
