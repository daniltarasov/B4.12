# импортируем библиотеку sqlalchemy и некоторые функции из нее 
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# константа, указывающая способ соединения с базой данных
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
# базовый класс моделей таблиц
Base = declarative_base()

# Структура таблицы пользователи
#CREATE TABLE user(
# "id" integer primary key autoincrement,
#  "first_name" text, 
# "last_name" text, 
# "gender" text,
#  "email" text,
# "birthdate" text, 
# "height" real);


class User(Base):
    __tablename__ = 'user'
    id = sa.Column(sa.Integer, primary_key=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender =  sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.Text)

def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    # создаем описанные таблицы
    #Base.metadata.create_all(engine)
    # создаем фабрику сессию
    session = sessionmaker(engine)
    # возвращаем сессию
    return session()

def request_data():
#    Запрашивает у пользователя данные и добавляет их в список users
    # выводим приветствие
    print("Привет! Я запишу твои данные!")
    # запрашиваем у пользователя данные
    first_name = input("Введи своё имя: ")
    last_name = input("А теперь фамилию: ")
    gender = input("А теперь пол: ")
    email = input("Мне еще понадобится адрес твоей электронной почты: ")
    birthdate= input("А теперь дату рождения: ")
    height= input("А теперь рост: ")

    # создаем нового пользователя
    user = User(
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        email=email,
        birthdate= birthdate,
        height = height
    )
    # возвращаем созданного пользователя
    return user


def main():
#    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    session = connect_db()
    # запрашиваем данные пользоватлея
    user = request_data()
    # добавляем нового пользователя в сессию
    session.add(user)
    # сохраняем все изменения, накопленные в сессии
    session.commit()
    print("Спасибо, данные сохранены!")
 

if __name__ == "__main__":
    main()


# SELECT * FROM user WHERE gender = "aaa";