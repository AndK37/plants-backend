from sqlalchemy.orm import Session
from database import engine
import models
from datetime import date
import os


models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

with Session(bind=engine) as session:
    try:
        os.mkdir('img')
    except:
        pass

    r1 = models.Role(name='admin')
    r2 = models.Role(name='moderator')
    r3 = models.Role(name='customer')
    r4 = models.Role(name='seller')

    u1 = models.User(surname='Иванов', 
                     name='Иван', 
                     email='ivan.ivanov@mail.ru', 
                     login='ivanych', 
                     password='$2b$12$Z9fp6m2PDDOxEtiHem0Y5.1PX87a0hisEsTQ3Qrre2TTmtyifyMmm', 
                     role_id=1)
    u2 = models.User(surname='Петров', 
                     name='Сергей', 
                     email='sergei.petrov@gmail.com', 
                     login='spetr', 
                     password='$2b$12$Z9fp6m2PDDOxEtiHem0Y5.1PX87a0hisEsTQ3Qrre2TTmtyifyMmm', 
                     role_id=2)
    u3 = models.User(surname='Смирнова', 
                     name='Ольга', 
                     email='olga.smirnova@yahoo.com', 
                     login='osmirnov', 
                     password='$2b$12$Z9fp6m2PDDOxEtiHem0Y5.1PX87a0hisEsTQ3Qrre2TTmtyifyMmm', 
                     role_id=3)
    u4 = models.User(surname='Васильев', 
                     name='Дмитрий', 
                     email='vasilyev.dmitry@yandex.r', 
                     login='dmvasiliev', 
                     password='$2b$12$Z9fp6m2PDDOxEtiHem0Y5.1PX87a0hisEsTQ3Qrre2TTmtyifyMmm', 
                     role_id=3)
    u5 = models.User(surname='Попова', 
                     name='Елена', 
                     email='elena.popova@hotmail.com', 
                     login='Green Shop', 
                     password='$2b$12$Z9fp6m2PDDOxEtiHem0Y5.1PX87a0hisEsTQ3Qrre2TTmtyifyMmm', 
                     role_id=4)

    c1 = models.Category(name='vegetables')
    c2 = models.Category(name='fruits')
    c3 = models.Category(name='flowers')

    p1 = models.Plant(name='Помидор', 
                         desc='Красный овощ, богатый витаминами и антиоксидантами.', 
                         price=80.0, 
                         packing=1, 
                         category_id=1,
                         seller_id=5,
                         image='./img/plants/17472072770195327.jpeg')
    p2 = models.Plant(name='Огурец', 
                         desc='Свежий зеленый овощ, популярный ингредиент салатов.', 
                         price=70.0, 
                         packing=1, 
                         category_id=1,
                         seller_id=5,
                         image='./img/plants/17472072960632319.jpeg')
    p3 = models.Plant(name='Роза', 
                         desc='Классический цветок, символ любви и красоты.', 
                         price=150.0, 
                         packing=1, 
                         category_id=3,
                         seller_id=5,
                         image='./img/plants/17472073070402499.jpeg')
    p4 = models.Plant(name='Картофель', 
                         desc='Корнеплод, основа многих блюд русской кухни.', 
                         price=50.0, 
                         packing=1, 
                         category_id=1,
                         seller_id=5,
                         image='./img/plants/17472075390502365.jpeg')
    p5 = models.Plant(name='Клубника', 
                         desc='Красная ароматная ягода, любимое лакомство летом.', 
                         price=200.0, 
                         packing=1, 
                         category_id=2,
                         seller_id=5,
                         image='./img/plants/17472073470197747.jpeg')
    p6 = models.Plant(name='Ромашка', 
                         desc='Простой и нежный цветок, часто используется в народной медицине.', 
                         price=50.0, 
                         packing=1, 
                         category_id=3,
                         seller_id=5,
                         image='./img/plants/17472073580200932.jpeg')
    p7 = models.Plant(name='Морковь', 
                         desc='Оранжевый корнеплод, полезный источник витамина А.', 
                         price=60.0, 
                         packing=1, 
                         category_id=1,
                         seller_id=5,
                         image='./img/plants/17472072770195327.jpeg')
    p8 = models.Plant(name='Груша', 
                         desc='Сочный фрукт с приятным ароматом и вкусом.', 
                         price=120.0, 
                         packing=1, 
                         category_id=2,
                         seller_id=5,
                         image='./img/plants/17472073640628441.jpeg')
    p9 = models.Plant(name='Капуста белокочанная', 
                         desc='Крепкий овощ, незаменимый компонент борща и квашеной капусты.', 
                         price=40.0, 
                         packing=1, 
                         category_id=1,
                         seller_id=5,
                         image='./img/plants/17472075560042722.jpeg')
    p10 = models.Plant(name='Азалия', 
                         desc='Цветок с яркими цветами, популярен среди цветоводов.', 
                         price=250.0, 
                         packing=1, 
                         category_id=3,
                         seller_id=5,
                         image='./img/plants/17472073890088047.jpeg')
                         
    pr1 = models.PlantRating(user_id=3, plant_id=1, rating=5)
    pr2 = models.PlantRating(user_id=4, plant_id=1, rating=2)

    session.add(r1)
    session.add(r2)
    session.add(r3)
    session.add(r4)

    session.add(u1)
    session.add(u2)
    session.add(u3)
    session.add(u4)
    session.add(u5)

    session.add(c1)
    session.add(c2)
    session.add(c3)

    session.add(p1)
    session.add(p2)
    session.add(p3)
    session.add(p4)
    session.add(p5)
    session.add(p6)
    session.add(p7)
    session.add(p8)
    session.add(p9)
    session.add(p10)

    session.add(pr1)
    session.add(pr2)

    session.commit()