from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Definir la base de datos
DATABASE_URL = "sqlite:///local_database.db"

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL, echo=True)

# Crear una clase base
Base = declarative_base()

# Definir un modelo
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

# Crear todas las tablas
Base.metadata.create_all(engine)

# Crear una sesión
Session = sessionmaker(bind=engine)
session = Session()

# Crear una nueva instancia de User
new_user = User(name='Juan', age=30)

# Agregar a la sesión
session.add(new_user)

# Confirmar los cambios
session.commit()

# Consultar todos los usuarios
users = session.query(User).all()
for user in users:
    print(user.name, user.age)

session.close()
