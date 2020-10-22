import hashlib
import json
import os
from datetime import datetime
from http import HTTPStatus
from multiprocessing import Process
from time import sleep
import urllib.request as url_req

from flask import Flask, request

app = Flask(__name__)


def log(message, severity="info"):
    _log = {
        "message": message,
        "timestamp": datetime.now().timestamp(),
        "severity": severity
    }
    print(json.dumps(_log, ensure_ascii=False))
    pass


def file_read(file_url):
    with url_req.urlopen(file_url) as f:
        content = f.read().decode('utf-8')

        return content
    pass


def handler(code, content, checksum):
    sleep(10)  # Ваша зона действии
    log("Сообщение обработано. Код: {}; Контрольная сумма: {}".format(code, checksum))
    pass


def create_message_hash(message):
    return hashlib.sha256(json.dumps(message, ensure_ascii=False).encode('utf-8')).hexdigest()


@app.route('/endpoint', methods=["POST"])
def endpoint():
    r = request.json
    code = r['code']
    file_url = r['file_url']
    checksum = r['checksum']

    log("Получено сообщение. Код {}; Ссылка на файл: {}; Заголовок: {}".format(code, file_url, checksum))

    # Чтение контента файла
    content = file_read(file_url)
    # Hash сумма контента файла
    sha256_hash = create_message_hash(content)

    if checksum != sha256_hash:
        log("Вероятно произошло ошибка в чтении файла или неправильно посчитало хэш сумму файла")
        return {
            "Code": "FAIL",
            "Status": "Контент не соответствует контрольной сумме"
        }, HTTPStatus.NOT_ACCEPTABLE

    log("Хэш значения сообщения: {}".format(sha256_hash))
    # Проверка подписи
    # Требуется SDK от НУЦ РК

    try:
        # Лучше создать асинхронный процесс для обработки
        # Время Timeout-а запроса на стороне ПКБ 10s
        Process(target=handler, args=(code, content, checksum,)).start()
        pass
    except Exception as e:
        log(e, "error")
        pass

    # Запрос отработан успешно
    # Возвращаем http статус либо OK - 200, либо, если вы используете асинхронную обработку, ACCEPTED - 202
    return {
        "sha256": sha256_hash
    }, HTTPStatus.ACCEPTED


@app.route('/health', methods=["GET"])
def hello():
    return {
        "Status": "ok"
    }, HTTPStatus.OK


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 9090))
    app.run(host="0.0.0.0", port=port)
