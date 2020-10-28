"""Endpoint controller module"""
# Created by Жасулан Бердибеков <zhasulan87@gmail.com> at 10/28/20 9:15 PM
import hashlib
from http import HTTPStatus
from multiprocessing import Process

from flask import request

from app import app, logger
from internal.handler.main import handler
from internal.handler.message import file_read


@app.route('/endpoint', methods=["POST"])
def endpoint():
    """

    :return:
    """
    req = request.json
    code = req['code']
    proxy_url = req['proxy_url']
    filename = req['filename']
    checksum = req['checksum']

    logger.info(
        "Получено сообщение. Код %s; CDN Сервер: %s; Название файла: %s; Заголовок: %s", code, proxy_url, filename,
        checksum
    )

    # Чтение контента файла
    content = file_read(proxy_url, code, filename)

    if content is not None:
        # Hash сумма контента файла
        sha256_hash = hashlib.sha256(content).hexdigest()

        if checksum != sha256_hash:
            logger.error("Вероятно произошло ошибка в чтении файла или неправильно вычислен хэш сумма файла")
            return {"Code": "FAIL", "Status": "Контент не соответствует контрольной сумме"}, HTTPStatus.NOT_ACCEPTABLE

        logger.info("Хэш значения сообщения: %s", sha256_hash)
        # Проверка подписи
        # Требуется SDK от НУЦ РК

        try:
            # Лучше создать асинхронный процесс для обработки
            # Время Timeout-а запроса на стороне ПКБ 10s
            Process(target=handler, args=(code, content,)).start()
        except Exception as exc:  # pylint: disable=broad-except
            logger.error(exc)

        # Запрос отработан успешно
        # Возвращаем http статус либо OK - 200, либо, если вы используете асинхронную обработку, ACCEPTED - 202
        return {
                   "sha256": sha256_hash
               }, HTTPStatus.ACCEPTED
    return {"Code": "FAIL", "Status": "Content is None"}, HTTPStatus.INTERNAL_SERVER_ERROR