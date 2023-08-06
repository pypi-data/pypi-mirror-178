# di-di-napalm-ros
## Обзор
Пакет позволяющий взаимодействовать с оборудованием Mikrotik  
Библиотека загружена на pypi https://pypi.org/project/di-di-napalm-ros/

## Установка
```
pip install di-di-napalm-ros
```

## Функционал
Реализованные методы:  
-get_facts  
-get_environment  
-get_lldp_neighbors_detail  
-get_interfaces  
-get_config  

## Процесс обновления пакета с заливанием на pypi
Изменяем setup.py в корне и по необходимости __init__ внутри функциональной директории

Из корня проекта
Билдим:
```
python setup.py sdist
```
Отправляем на pypi
```
twine upload dist/*
```
