# http-hash-server
Тестовый сервер хранения файлов на Flask
## Описание
Сервер позволяет хранить, скачивать и удалять файлы. Обращение к файлам
осуществляется по http через их MD5 контрольную ссумму.
Для запуска сервера нужно указать папку хранения, IP адресс запуска и порт.  Для этого создать .env файл
с переменной или добавить в окружение:
```bash
UPLOAD_FOLDER = "/store/"
HOST = "0.0.0.0"
PORT= "5000"
```
### Загрузка файлов
Загрузка файла осуществляется методом POST, пример curl запроса:
```bash
curl -v -H 'Content-Type: application/octet-stream' -X POST --data-binary @/file/to/load  localhost:5000
```
В ответ сервер выдаёт хэш сумму файла, в заголовке ответа, по которой к нему в дальнейшем можно обращаться
```bash
Hash_of_file: a90928395006652f7d08202b2535898e
```
### Скачивание файлов
Запрос для скачивания файла отправляется методом GET, где в качестве
аргумента выступает контрольная сумма полученная ранее. Пример curl запроса:

```bash
curl -v -O  localhost:5000/db1d860731f285487ec459c53924ab95
```

### Удаление файлов
Запрос на удаление аналогичен запросу на скачивание только передаётся через 
метод DELETE
```bash
curl -v -X 'DELETE' localhost:5000/db1d860731f285487ec459c53924ab93
```

## Сборка Docker контейнера и его запуск
Для упрощения развёртывания может быть удобно собрать отдельный Docker контейнер 
с приложением и запускать его в "изолированном" режиме.
Для этого необходимо наличие установленного Docker 
и выполнение команд ниже из корневого каталого репозитория.

```bash
docker build --tag http-server-docker .
```
После окончания сборки образа запустите контейнер заменив /home/user/store/
на путь к папке на вашем ПК

```bash
docker run -v /home/user/store/:/store/ -d -p 5000:5000 http-server-docker
```


