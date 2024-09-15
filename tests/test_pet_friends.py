from api import PetFriends
from settings import valid_email, valid_password
import os


pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Проверяем, что запрос API ключа возвращает статус 200 и в результате содержится слово key."""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result.
    status, result = pf.get_api_key(email, password)

    # Сверяем полученный ответ с ожидаемым результатом.
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """Проверяем, что запрос списка всех питомцев возвращает статус 200
    и в результате содержится не пустой массив питомцев. Доступное значение параметра filter - 'my_pets' либо ''."""

    # Получаем api ключ и сохраняем в переменную auth_key.
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    #  Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result.
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Сверяем полученный ответ с ожидаемым результатом.
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Deyk', animal_type='dog', age=3, pet_photo='images/Deyk.jpg'):
    """Проверяем, что запрос на создание питомца с фото с валидными данными возвращает статус 200
    и имя созданного питомца соответствует ожидаемому."""

    # Получаем полный путь до файла с фото питомца
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем api ключ и сохраняем в переменную auth_key.
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    #  Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result.
    status, result = pf.add_new_pet_with_photo(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом.
    assert status == 200
    assert result['name'] == name


def test_update_pet_info_with_valid_data(name='Deyk', animal_type='dog', age=5):
    """Проверяем, что запрос на обновление данных о своем последнем созданном питомце
    с валидными данными возвращает статус 200 и обновленные данные соответствуют ожидаемым."""

    # Получаем api ключ и сохраняем в переменную auth_key.
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Получаем список своих питомцев.
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Если список не пустой, обновляем данные о своем последнем созданном питомце.
    if len(my_pets['pets']) > 0:
        #  Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result.
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Сверяем полученный ответ с ожидаемым результатом.
        assert status == 200
        assert result['age'] == str(age)

    # Если список пустой, вызываем исключение с сообщением об отсутствии своих питомцев.
    else:
        raise Exception("There aren't my pets.")


def test_delete_pet_with_valid_data():
    """Проверяем, что запрос на удаление питомца с валидными данными возвращает статус 200
    и id удаленного питомца нет в списке питомцев."""

    # Получаем api ключ и сохраняем в переменную auth_key.
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Получаем список своих питомцев.
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Если список не пустой, удаляем питомца, созданного последним.
    if len(my_pets['pets']) > 0:
        # Берем id питомца, созданного последним.
        pet_id = my_pets['pets'][0]['id']

        # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status.
        status = pf.delete_pet(auth_key, pet_id)

        # Повторно запрашиваем список своих питомцев.
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

        # Сверяем полученный ответ с ожидаемым результатом.
        assert status == 200
        assert pet_id not in my_pets

    # Если список пустой, вызываем исключение с сообщением об отсутствии своих питомцев.
    else:
        raise Exception("There aren't my pets.")


def test_add_new_pet_without_photo_with_valid_data(name='Deyk', animal_type='dog', age=3):
    """Проверяем, что запрос на создание питомца без фото с валидными данными возвращает статус 200
    и имя созданного питомца соответствует ожидаемому."""

    # Получаем api ключ и сохраняем в переменную auth_key.
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    #  Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result.
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом.
    assert status == 200
    assert result['name'] == name


def test_add_pet_photo_with_valid_data(pet_photo='images/Deyk.jpg'):
    """Проверяем, что запрос на добавление фото питомца с валидными данными возвращает статус 200
    и id созданного питомца соответствует ожидаемому."""

    # Получаем полный путь до файла с фото питомца
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем api ключ и сохраняем в переменную auth_key.
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Получаем список своих питомцев.
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Если список не пустой, добавляем фото для своего последнего созданного питомца.
    if len(my_pets['pets']) > 0:
        #  Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result.
        status, result = pf.add_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Сверяем полученный ответ с ожидаемым результатом.
        assert status == 200
        assert result['id'] == my_pets['pets'][0]['id']

    # Если список пустой, вызываем исключение с сообщением об отсутствии своих питомцев.
    else:
        raise Exception("There aren't my pets.")


def test_unsuccessful_get_api_key_with_empty_email(
        email='',
        password=valid_password
):
    """Проверяем, что запрос API ключа с пустым значением email возвращает статус 403."""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status.
    status, _ = pf.get_api_key(email, password)

    # Сверяем полученный ответ с ожидаемым результатом.
    assert status == 403


def test_unsuccessful_get_api_key_with_empty_password(
        email=valid_email,
        password=''
):
    """Проверяем, что запрос API ключа с пустым значением пароля возвращает статус 403."""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status.
    status, _ = pf.get_api_key(email, password)

    # Сверяем полученный ответ с ожидаемым результатом.
    assert status == 403


def test_unsuccessful_get_api_key_with_empty_fields(
        email='',
        password=''
):
    """Проверяем, что запрос API ключа с пустыми полями возвращает статус 403."""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status.
    status, _ = pf.get_api_key(email, password)

    # Сверяем полученный ответ с ожидаемым результатом.
    assert status == 403


def test_unsuccessful_get_api_key_with_swap_fields(
        email=valid_email,
        password=valid_password
):
    """Проверяем, что запрос API ключа с валидным email в поле пароля
    и валидным паролем в поле email возвращает статус 403."""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status.
    status, _ = pf.get_api_key(password, email)

    # Сверяем полученный ответ с ожидаемым результатом.
    assert status == 403


def test_unsuccessful_get_api_key_with_incorrect_password(
        email=valid_email,
        password=valid_password + 'a'
):
    """Проверяем, что запрос API ключа с невалидным паролем возвращает статус 403."""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status.
    status, _ = pf.get_api_key(email, password)

    # Сверяем полученный ответ с ожидаемым результатом.
    assert status == 403


def test_unsuccessful_add_new_pet_with_gif_file(
        name='Deyk',
        animal_type='dog',
        age=3,
        pet_photo='images/Deyk.gif'
):
    """Проверяем, что запрос на создание питомца с файлом gif вместо фото возвращает статус 400.
    API запрос работает с ошибкой. При создании питомца с файлом gif вместо фото создается питомец без фото.
    Вместо кода 400 приходит код 200."""

    # Получаем полный путь до файла с фото питомца
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем api ключ и сохраняем в переменную auth_key.
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    #  Отправляем запрос и сохраняем полученный ответ с кодом статуса в status.
    status, _ = pf.add_new_pet_with_photo(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом.
    assert status == 400


def test_unsuccessful_add_new_pet_without_photo_with_str_age(name='Deyk', animal_type='dog', age='five'):
    """Проверяем, что запрос на создание питомца без фото со строковым значением возраста возвращает статус 400.
    API запрос работает с ошибкой. Питомец создается со строковым значением возраста.
    Вместо кода 400 приходит код 200."""

    # Получаем api ключ и сохраняем в переменную auth_key.
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    #  Отправляем запрос и сохраняем полученный ответ с кодом статуса в status.
    status, _ = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом.
    assert status == 400


def test_unsuccessful_add_new_pet_without_photo_with_empty_name(name='', animal_type='dog', age=5):
    """Проверяем, что запрос на создание питомца без фото с пустым значением имени возвращает статус 400.
    API запрос работает с ошибкой. Питомец создается без имени.
    Вместо кода 400 приходит код 200."""

    # Получаем api ключ и сохраняем в переменную auth_key.
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    #  Отправляем запрос и сохраняем полученный ответ с кодом статуса в status.
    status, _ = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом.
    assert status == 400
