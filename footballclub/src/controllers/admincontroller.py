# admincontroller.py
from src.models.users import Users
from src.models.roles import Roles
from peewee import DoesNotExist

class AdminController:
    @staticmethod
    def create_user(username, password, email, role_id):
        """
        Создает нового пользователя с указанными данными.
        Возвращает созданного пользователя или None в случае ошибки.
        """
        try:
            role = Roles.get(Roles.role_id == role_id)
            user = Users.create(username=username, password=password, email=email, role_id=role)
            print(f"Пользователь {username} успешно создан.")
            return user
        except DoesNotExist:
            print(f"Роль с ID {role_id} не найдена.")
            return None
        except Exception as e:
            print(f"Ошибка при создании пользователя: {e}")
            return None

    @staticmethod
    def delete_user(user_id):
        """
        Удаляет пользователя по ID.
        Возвращает True, если удаление прошло успешно, иначе False.
        """
        try:
            user = Users.get(Users.user_id == user_id)
            user.delete_instance()
            print(f"Пользователь с ID {user_id} успешно удален.")
            return True
        except DoesNotExist:
            print(f"Пользователь с ID {user_id} не найден.")
            return False
        except Exception as e:
            print(f"Ошибка при удалении пользователя: {e}")
            return False

    @staticmethod
    def get_all_users():
        """
        Возвращает список всех пользователей.
        В случае ошибки возвращает пустой список.
        """
        try:
            users = Users.select()
            return list(users)
        except Exception as e:
            print(f"Ошибка при получении списка пользователей: {e}")
            return []

    @staticmethod
    def update_user(user_id, username=None, password=None, email=None, role_id=None):
        """
        Обновляет данные пользователя по ID.
        Возвращает обновленного пользователя или None в случае ошибки.
        """
        try:
            user = Users.get(Users.user_id == user_id)
            if username:
                user.username = username
            if password:
                user.password = password
            if email:
                user.email = email
            if role_id:
                role = Roles.get(Roles.role_id == role_id)
                user.role_id = role
            user.save()
            print(f"Данные пользователя с ID {user_id} успешно обновлены.")
            return user
        except DoesNotExist:
            print(f"Пользователь с ID {user_id} или роль с ID {role_id} не найдены.")
            return None
        except Exception as e:
            print(f"Ошибка при обновлении данных пользователя: {e}")
            return None

    @staticmethod
    def get_user_by_id(user_id):
        """
        Возвращает пользователя по ID.
        В случае ошибки возвращает None.
        """
        try:
            user = Users.get(Users.user_id == user_id)
            return user
        except DoesNotExist:
            print(f"Пользователь с ID {user_id} не найден.")
            return None
        except Exception as e:
            print(f"Ошибка при получении пользователя: {e}")
            return None

    @staticmethod
    def get_users_by_role(role_id):
        """
        Возвращает список пользователей по роли.
        В случае ошибки возвращает пустой список.
        """
        try:
            users = Users.select().where(Users.role_id == role_id)
            return list(users)
        except Exception as e:
            print(f"Ошибка при получении пользователей по роли: {e}")
            return []

if __name__ == "__main__":
    # Пример использования
    new_user = AdminController.create_user("test_user", "password123", "test@example.com", 1)
    users = AdminController.get_all_users()
    for user in users:
        print(user.username)