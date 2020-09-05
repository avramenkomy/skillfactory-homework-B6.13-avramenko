#Стандартный блок импорта
from bottle import *
import album

#класс с пользовательским исключением
class NegativeNumberError(Exception):
	'''Ошибка, характеризующая число меньше 0'''
	pass

@route("/albums/<artist>")
def albums(artist):
    albums_list = album.find(artist) #Получаем список альбомов с заданным artist из модуля album.py
    if not albums_list:
    	#Если альбомов не нашлось
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(400, message)
    else:
    	#Если список альбомов не пуст, то генерируем список из названий полученных альбомов
        albums_names = [album.album for album in albums_list]
        #Формируем удобный вывод на страницу с переносом строк
        result = "Найдено <b>{}</b> альбомов {}: <br>".format(len(albums_names), artist) + "<br>".join(albums_names)
    return result

def conversion(value):
	'''Возбуждает пользовательское исключение если в запросе был передан отрицательный год'''
	if int(value) < 0:
		raise NegativeNumberError("Error: Value must be positive number")


@route("/albums", method="POST")
def album_data():
	'''Получает данные альбома, проверяет год, проверяет наличие данных об альбоме в БД и сохраняет данные альбома в БД'''

	#Получаем данные альбома
	album_data = {
		"year": request.forms.get("year"),
		"artist": request.forms.get("artist"),
		"genre": request.forms.get("genre"),
		"album": request.forms.get("album")
	}

	if album_data["year"]: #Если год был указан, то выполняем блок if
		try:
			#Попытка преобразовать в число
			year = conversion(album_data["year"])

		except ValueError:
			#Если в запросе год был указан как нечисловое значение, то ловим исключение ValueError
			message = "Error: Value must be integer"
			result = HTTPError(400, message)

		except NegativeNumberError:
			#Если в запросе год был указан как отрицательное число, то ловим кастомное исключение
			message = "Error: Year must be positive number"
			result = HTTPError(400, message)

		else: #Если исключений не возникло выполняем блок else
			if album.find_conflict(album_data): #Ищем конфликты, т.е. совпадающие альбомы по значениям album и artist
				album.save_album(album_data) #Сохраняем данные альбома
				result = "Data was successful saved" #Сообщение об успешном сохранении данных
			else:
				#Если возник конфликт, то для вывода готовим код ошибки и соответствующее сообщение
				message = "Album already exists"
				result = HTTPError(409, message)
	else: #Если год не был указан, то выводим ошибку
		message = "Error: year must be entered"
		result = HTTPError(400, message)
		
	return result 

if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)