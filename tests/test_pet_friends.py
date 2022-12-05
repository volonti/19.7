from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os
pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем,что запрос api ключа возвращает статус 200 и результат содержит слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_correct_key(filter=''):
    """ Проверяем, что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api-ключ и сохраняем в переменную auth_key. Далее, используя этот ключ,
    запрашиваем список всех питомцев и проверяем, что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/cat.jpg'):
    """Проверяем, что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/8055.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_information_about_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

#Тест для ДЗ №1
def test_get_api_key_for_invalid_login(email=invalid_email, password=valid_password):
        """ Проверяем,что запрос api ключа возвращает статус 403 при вводе невалидного логина"""

        # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
        status, result = pf.get_api_key(email, password)

        # Сверяем полученные данные с нашими ожиданиями
        assert status == 403

#Тест для ДЗ №2
def test_get_api_key_for_invalid_password(email=valid_email, password=invalid_password):
        """ Проверяем,что запрос api ключа возвращает статус 403 при вводе невалидного пароля"""

        # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
        status, result = pf.get_api_key(email, password)

        # Сверяем полученные данные с нашими ожиданиями
        assert status == 403

#Тест для ДЗ №3
def test_add_new_pet_without_photo_with_valid_data(name='Котик', animal_type='Дворняжка',
                                     age='5'):
    """Проверяем, что можно добавить питомца без фото"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

#Тест для ДЗ №4
def test_add_photo_to_pet_with_valid_data(pet_photo='images/cat.jpg'):
    """Проверяем, что можно добавить фото питомцу по его ID"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем добавить питомцу фото
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_to_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Проверяем что статус ответа = 200
        assert status == 200
        assert result['pet_photo'] != ''
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

# Тест для ДЗ №5
def test_add_new_pet_with_empty_name(name='', animal_type='дворняжка',
                                         age='4', pet_photo='images/8055.jpg'):
    """Проверяем, что нельзя добавить питомца без имени"""
    # баг - питомца можно добавить без имени

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400

# Тест для ДЗ №6
def test_add_new_pet_with_empty_animal_type(name='Пёсик', animal_type='',
                                         age='5', pet_photo='images/8055.jpg'):
    """Проверяем, что нельзя добавить питомца без указания породы"""
    # баг - питомца можно добавить без ввода породы

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400

# Тест для ДЗ №7
def test_add_new_pet_with_invalid_age(name='Пёсик', animal_type='',
                                         age='-5', pet_photo='images/8055.jpg'):
    """Проверяем, что нельзя добавить питомца c отрицательным возрастом"""
    # баг - питомца можно добавить, указав отрицательное число

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400

# Тест для ДЗ №8
def test_add_new_pet_with_invalid_auth_key(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/8055.jpg'):
    """Проверяем, что нельзя добавить питомца c при вводе некорректного api ключа"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Указываем некорректный api ключ
    auth_key = {"key": '8a417540fe39eae66f0bcdbafd453e1fadfc2ba1b50cbc0d634b1fa2'}

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403

# Тест для ДЗ №9
def test_delete_pet_without_petID():
    """Проверяем невозможность удаления питомца без указания его ID"""

    # Получаем ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Пытаемся удалить питомца без указания ID
    pet_id = ''
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Проверяем что статус ответа равен 404, т.к. питомец не найден
    assert status == 404

# Тест для ДЗ №10
def test_add_new_pet_with_too_long_name(name='PPPPPPPPPPPPPPPPPPPPPPPPP'
                                             'PPPPPPPPPPPPPPPPPPPPPPPPPP'
                                             'PPPPPPPPPPPPPPPPPPPPPPPPPP'
                                             'PPPPPPPPPPPPPPPPPPPPPPPPPP'
                                             'PPPPPPPPPPPPPPPPPPPPPPPPPP', animal_type='двортерьер',
                                     age='4', pet_photo='images/cat.jpg'):
    """Проверяем, что нельзя добавить питомца с слишком длинным именем"""
    #баг

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
