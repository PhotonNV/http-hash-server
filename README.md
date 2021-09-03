# http-hash-server
Тестовый сервер хранения файлов на Flask

Зпарос на удаление 
curl -v -X 'DELETE' 127.0.0.1:5000/db1d860731f285487ec459c53924ab93

curl -v -H 'Content-Type: application/octet-stream' -X PUT --data-binary @/home/aramzaev/test1/foto  127.0.0.1:5000

curl -v -O  127.0.0.1:5000/db1d860731f285487ec459c53924ab95


