# импортируем библиотеку sqlalchemy и некоторые функции из нее 
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text
import datetime 


# константа, указывающая способ соединения с базой данных
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
# базовый класс моделей таблиц
Base = declarative_base()

class User(Base):
    __tablename__ = 'athelete'
    id = sa.Column(sa.Integer, primary_key=True)
    age = sa.Column(sa.Integer)
    birthdate = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.Float)
    name = sa.Column(sa.Text)
    weight = sa.Column(sa.Integer)
    gold_medals = sa.Column(sa.Integer)
    silver_medals = sa.Column(sa.Integer)
    bronze_medals = sa.Column(sa.Integer)
    total_medals = sa.Column(sa.Integer)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)
    def __str__(self):
        return "%s %s %s %s %s %s %s" % (self.id, self.age, self.birthdate, self.gender , self.height , self.name ,self.weight )
    
    def find(self,ufilter, session):
        #ufilter = 'athelete.'+ufilter
        query = session.query(User).filter(text(ufilter))
        user = User(
            id = [user.id for user in query.all()],
            age = [user.age for user in query.all()],
            birthdate = [user.birthdate for user in query.all()],
            gender = [user.gender for user in query.all()],
            height = [user.height for user in query.all()],
            name = [user.name for user in query.all()],
            weight = [user.weight for user in query.all()],
            gold_medals = [user.gold_medals for user in query.all()],
            silver_medals = [user.silver_medals for user in query.all()],
            bronze_medals = [user.bronze_medals for user in query.all()],
            total_medals = [user.total_medals for user in query.all()],
            sport = [user.sport for user in query.all()],
            country = [user.country for user in query.all()]
        )
        if user.id:
            return user
        else:
            print("Такой атлет не найдет.")

    def print(self):
        if self.id:
            for user_id in range(len(self.id)):
                # выводим на экран идентификатор - время_последней_активности
                print("id: {}  имя: {}  дата р.:{} рост:{}".format(self.id[user_id], self.name[user_id] , self.birthdate[user_id], self.height[user_id] ))
        else:
            # если список оказался пустым, выводим сообщение об этом
            print("Такой атлет не найдет.")
    
    


def connect_db():
    #Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    # создаем описанные таблицы
    Base.metadata.create_all(engine)
    # создаем фабрику сессию
    session = sessionmaker(engine)
    # возвращаем сессию
    return session()



def get_nearest_value(iterable, value):
    return min(iterable, key=lambda x: abs(x - value))


def convert_str_to_date(date_str):
    date_str = str(date_str)
    parts = date_str.split("-")
    date_parts = map(int, parts)
    date = datetime.date(*date_parts)
    return date


def nearest_by_bd(user, session):
    athletes_list = session.query(User).all()
    athlete_id_bd = {}
    for athlete in athletes_list:
        bd = convert_str_to_date(athlete.birthdate)
        athlete_id_bd[athlete.id] = bd

    user_bd = convert_str_to_date(user.birthdate[0])
    min_dist = None
    athlete_id = None

    for id_, bd in athlete_id_bd.items():
        dist = abs(user_bd - bd)
        if not min_dist or dist < min_dist:
            min_dist = dist
            athlete_id = id_
    return athlete_id




def main():
    session = connect_db()
    userid = input("Введи ID пользователя для поиска: ")
    user = User()

    user = user.find('athelete.id == '+ str(userid), session)
    if user != None:
        print('найден атлет')
        user.print()

        print('найден  c похожим ростом')
        user1 = User()
        user1 = user1.find('athelete.height == '+ str(user.height[0]) + ' AND athelete.id !=' + str(user.id[0]), session)
        numb =get_nearest_value(user1.id, 1)
        user1 = user1.find('athelete.id == '+ str(numb), session)
        user1.print()

        print('найден  c похожей датой рождения')
        user2 = User()
        athlete_id = nearest_by_bd(user, session)
        user2 = user2.find('athelete.id == '+ str(athlete_id), session)
        user2.print()


if __name__ == "__main__":
    main()

