import unittest
import json
from app import app, db
from models import User


class UserTestCase(unittest.TestCase):

  def setUp(self):
    self.app = app.test_client()
    self.app.testing = True

    # Очищаем базу данных перед тестами
    with app.app_context():
      db.create_all()

  def tearDown(self):
    # Удаляем данные после тестов
    with app.app_context():
      db.session.remove()
      db.drop_all()

  def test_register_success(self):
    """Test creating a new user successfully."""
    user_data = {
      "username": "Artem",
      "email": "artem@mail.ru",
      "password": "12345"
    }

    response = self.app.post('/api/register',
                             data=json.dumps(user_data),
                             content_type='application/json')

    # Логируем ответ для отладки
    print("Response data (success):", response.data.decode())

    # Проверяем статус ответа
    self.assertEqual(response.status_code, 201)

    # Декодируем JSON-ответ
    data = json.loads(response.data.decode())

    # Проверяем наличие access_token и user_id
    self.assertIn('access_token', data)
    self.assertIn('user_id', data)

  def test_register_invalid_email(self):
    """Test creating a user with an invalid email format."""
    user_data = {
      "username": "InvalidEmailUser",
      "email": "invalidemail",  # Некорректный email
      "password": "12345"
    }

    response = self.app.post('/api/register',
                             data=json.dumps(user_data),
                             content_type='application/json')

    # Логируем ответ для отладки
    print("Response data (invalid email):", response.data.decode())

    # Проверяем статус ответа (ожидаем 400)
    self.assertEqual(response.status_code, 400)

    # Проверяем сообщение об ошибке
    data = json.loads(response.data.decode())
    self.assertIn('message', data)
    self.assertIn('Invalid email address', data['message'])

  def test_login_success(self):
    """Test user login with valid credentials."""
    # Сначала создадим пользователя
    user_data = {
      "username": "Artem",
      "email": "artem@mail.ru",
      "password": "12345"
    }
    self.app.post('/api/register',
                  data=json.dumps(user_data),
                  content_type='application/json')

    # Затем попробуем залогиниться
    login_data = {
      "username": "Artem",
      "password": "12345"
    }

    response = self.app.post('/api/login',
                             data=json.dumps(login_data),
                             content_type='application/json')

    # Логируем ответ для отладки
    print("Response data (login success):", response.data.decode())

    # Проверяем статус ответа
    self.assertEqual(response.status_code, 200)

    # Проверяем наличие access_token
    data = json.loads(response.data.decode())
    self.assertIn('access_token', data)

  def test_login_invalid_credentials(self):
    """Test login with invalid credentials."""
    login_data = {
      "username": "NonExistentUser",
      "password": "wrongpassword"
    }

    response = self.app.post('/api/login',
                             data=json.dumps(login_data),
                             content_type='application/json')

    # Логируем ответ для отладки
    print("Response data (invalid login):", response.data.decode())

    # Проверяем статус ответа (ожидаем 401)
    self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
  unittest.main()
