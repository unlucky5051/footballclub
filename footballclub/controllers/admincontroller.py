# admincontroller.py
from models.user import User
from models.role import Role
from peewee import DoesNotExist

class AdminController:
    @staticmethod
    def create_user(username, password, email, role_id):
        """
        Создает нового пользователя.
        :param username: Имя пользователя
        :param password: Пароль
        :param email: Электронная почта
        :param role_id: ID роли пользователя
        :return: Созданный пользователь или None, если произошла ошибка
        """
        try:
            # Проверяем, существует ли роль с указанным ID
            role = Role.get(Role.role_id == role_id)
            user = User.create(username=username, password=password, email=email, role_id=role)
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
        :param user_id: ID пользователя
        :return: True, если пользователь удален, иначе False
        """
        try:
            user = User.get(User.user_id == user_id)
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
        :return: Список пользователей
        """
        try:
            users = User.select()
            return list(users)
        except Exception as e:
            print(f"Ошибка при получении списка пользователей: {e}")
            return []

    @staticmethod
    def update_user(user_id, username=None, password=None, email=None, role_id=None):
        """
        Обновляет данные пользователя.
        :param user_id: ID пользователя
        :param username: Новое имя пользователя (опционально)
        :param password: Новый пароль (опционально)
        :param email: Новая электронная почта (опционально)
        :param role_id: Новая роль (опционально)
        :return: Обновленный пользователь или None, если произошла ошибка
        """
        try:
            user = User.get(User.user_id == user_id)
            if username:
                user.username = username
            if password:
                user.password = password
            if email:
                user.email = email
            if role_id:
                role = Role.get(Role.role_id == role_id)
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

    @classmethod
    def deleteUserAdm(cls, id):
        try:
            user = User.get(User.user_id == id)
            user_name = user.name
            User.delete().where(User.user_id == id).execute()
            return True
        except User.DoesNotExist:
            return False

if __name__ == "__main__":
    print(AdminController.delete_user(1))