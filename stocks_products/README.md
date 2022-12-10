Создание образа, находясь в папке с проектом stocks_products:

docker build -t crud_test .

Запуск контейнера:

docker run -p 8000:8000 --name crud_test -d crud_test

После чего проект доступен на localhost:8000