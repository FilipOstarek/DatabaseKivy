from sqlalchemy import create_engine, Column, ForeignKey, UniqueConstraint, desc
from sqlalchemy.types import Float, String, Integer, TIMESTAMP, Enum, Text, BLOB, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Global Variables

SQLITE = 'sqlite'
MYSQL = 'mysql'

Base = declarative_base()


class Popis(Base):
    __tablename__ = 'popis'

    id = Column(Integer, primary_key=True)
    jmeno = Column(String(50), nullable=True)
    vek = Column(String(50), nullable=True)
    vaha = Column(String(50), nullable=True)
    samotny_popis = Column(Text)
    #fotka = relationship('Fotka', backref='popis')
    fotka_id = Column(Integer, ForeignKey('fotka.id'))
    druh = Column(String(60), ForeignKey('druh.jmeno_druhu'))


class Fotka(Base):
    __tablename__ = 'fotka'

    id = Column(Integer, primary_key=True)
    url = Column(String(150), unique=True, nullable=False)
    nazev_fotky = Column(String(length=100))
    #druh = relationship('Druh', backref='popis')
    popis = relationship('Popis', backref='popis')

class Druh(Base):
    __tablename__ = 'druh'

    id = Column(Integer, primary_key=True)
    jmeno_druhu = Column(String(60), unique=True, nullable=False)

class Database:
    DB_ENGINE = {
        SQLITE: 'sqlite:///{DB}',
        MYSQL: 'mysql+mysqlconnector://{USERNAME}:{PASSWORD}@localhost/{DB}'
    }

    def __init__(self, dbtype='sqlite', username='', password='', dbname='data.db'):
        dbtype = dbtype.lower()

        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname, USERNAME=username, PASSWORD=password)
            self.engine = create_engine(engine_url, echo=False)
        else:
            print('DBType is not found in DB_ENGINE')

        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def create_popis(self, popis):
        try:
            self.session.add(popis)
            self.session.commit()
            return True
        except:
            return False

    def create_fotka(self, fotka):
        try:
            self.session.add(fotka)
            self.session.commit()
            return True
        except:
            return False

    def create_druh(self, druh):
        try:
            self.session.add(druh)
            self.session.commit()
            return True
        except:
            return False

    def read_popisy(self, order=Popis.jmeno):
        try:
            result = self.session.query(Popis).order_by(order).all()
            print(result)
            return result
        except:
            return False

    def read_popisy_by_id(self, id):
        try:
            result = self.session.query(Popis).get(id)
            return result
        except:
            return False

    def read_fotky(self, order=Fotka.id):
        try:
            result = self.session.query(Fotka).order_by(order).all()
            return result
        except:
            return False

    def read_fotka_by_id(self, id):
        try:
            result = self.session.query(Fotka).get(id)
            return result
        except:
            return False

    #def read_druhy(self, order=Druh.id):
    def read_druhy(self):
        try:
            #result = self.session.query(Druh).order_by(order).all()
            result = self.session.query(Druh).all()
            return result
        except:
            return False

    def read_druhy_by_id(self, id):
        try:
            result = self.session.query(Druh).get(id)
            return result
        except:
            return False

    def update(self):
        try:
            self.session.commit()
            return True
        except:
            return False

    def delete_druh(self, id):
        try:
            pokus = self.read_druhy_by_id(id)
            self.session.delete(pokus)
            self.session.commit()
            return True
        except:
            return False

    def delete_fotka(self, id):
        try:
            pokus = self.read_fotka_by_id(id)
            self.session.delete(pokus)
            self.session.commit()
            return True
        except:
            return False

    def delete_popis(self, id):
        try:
            pokus = self.read_popisy_by_id(id)
            self.session.delete(pokus)
            self.session.commit()
            return True
        except:
            return False
