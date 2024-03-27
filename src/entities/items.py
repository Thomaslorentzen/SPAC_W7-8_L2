from sqlalchemy import VARCHAR, DateTime, text, create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime  
from sqlalchemy.ext.declarative import declarative_base
import csv

Base = declarative_base()

class Kategori(Base):
    __tablename__ = 'kategori'

    kategori_ID = Column(Integer, primary_key=True)
    kategori_navn = Column(String(255))
    beskrivelse = Column(String(255))

    vare = relationship("Vare", back_populates="kategori")

    def __init__(self, kategori_navn, beskrivelse):
        self.kategori_navn = kategori_navn
        self.beskrivelse = beskrivelse

    @staticmethod
    def tilføj_kategori(kategori_navn, beskrivelse, session):
        statement = text("CALL TilføjKategori(:kategori_navn, :beskrivelse)")
        session.execute(statement, {"kategori_navn": kategori_navn, "beskrivelse": beskrivelse})
        session.commit()

    @staticmethod
    def opdater_kategori(kategori_ID, kategori_navn, beskrivelse, session):
        statement = text("CALL OpdaterKategori(:kategori_ID, :kategori_navn, :beskrivelse)")
        session.execute(statement, {"kategori_ID": kategori_ID, "kategori_navn": kategori_navn, "beskrivelse": beskrivelse})
        session.commit()

    @staticmethod
    def slet_kategori(kategori_ID, session):
        statement = text("CALL FjernKategori(:kategori_ID)")
        session.execute(statement, {"kategori_ID": kategori_ID})
        session.commit()

    @staticmethod
    def vis_kategori_info(kategori_ID, session):
        statement = text("CALL HentKategoriInfo(:kategori_ID)")
        result = session.execute(statement, {"kategori_ID": kategori_ID})
        return result.fetchone()

class Vare(Base):
    __tablename__ = 'vare'

    vare_ID = Column(Integer, primary_key=True)
    name = Column(String)
    beskrivelse = Column(String)
    kategori_ID = Column(Integer, ForeignKey('kategori.kategori_ID'))
    pris = Column(Integer)
    lager_antal = Column(Integer)
    transaktion = relationship("Transaktion", back_populates="vare")

    # Define relationship with Kategori
    kategori = relationship("Kategori", back_populates="vare")


    def __init__(self, name, beskrivelse, kategori_ID, pris, lager_antal):
        self.name = name
        self.beskrivelse = beskrivelse
        self.kategori_ID = kategori_ID
        self.pris = pris
        self.lager_antal = lager_antal

    @staticmethod
    def tilføj_vare(name, beskrivelse, kategori_ID, pris, lager_antal, session):
        statement = text("CALL TilføjVare(:name, :beskrivelse, :kategori_ID, :pris, :lager_antal)")
        session.execute(statement, {"name": name, "beskrivelse": beskrivelse, "kategori_ID": kategori_ID,
                                    "pris": pris, "lager_antal": lager_antal})
        session.commit()

    @staticmethod
    def opdater_vare(vare_ID, name, beskrivelse, kategori_ID, pris, lager_antal, session):
        statement = text("CALL OpdaterVare(:vare_ID, :name, :beskrivelse, :kategori_ID, :pris, :lager_antal)")
        session.execute(statement, {"vare_ID": vare_ID, "name": name, "beskrivelse": beskrivelse,
                                    "kategori_ID": kategori_ID, "pris": pris, "lager_antal": lager_antal})
        session.commit()

    @staticmethod
    def slet_vare(vare_ID, session):
        statement = text("CALL FjernVare(:vare_ID)")
        session.execute(statement, {"vare_ID": vare_ID})
        session.commit()

    @staticmethod
    def vis_vare_info(vare_ID, session):
        statement = text("CALL HentVareInfo(:vare_ID)")
        result = session.execute(statement, {"vare_ID": vare_ID})
        return result.fetchone()

    @staticmethod
    def opret_vare_rapport(session, filename):
        try:
            items = session.execute("CALL OpretVareRapport()")
            items = [item for item in items]
            if not items:
                print("Ingen varer fundet.")
                return
            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Navn", "Beskrivelse", "Pris", "Lager Antal"])  # Write header
                writer.writerows(items)
            print(f"Rapporten er gemt som '{filename}'.")
        except Exception as ex:
            print(f"En ukendt fejl opstod: {ex}")


class Transaktion(Base):
    __tablename__ = 'transaktioner'
    
    transaktion_ID = Column(Integer, primary_key=True)
    vare_id = Column(Integer, ForeignKey('vare.vare_ID'))
    dato_og_tid = Column(DateTime)
    antal = Column(Integer)
    transaktionstype = Column(VARCHAR(50))

    vare = relationship("Vare", back_populates="transaktion")

    def opret_transaktion(self, session):
        try:
            vare_id = int(input("Indtast ID på varen for transaktionen: "))
            dato_og_tid = input("Indtast dato og tid for transaktionen (YYYY-MM-DD HH:MM:SS): ")
            transaktionstype = input("Indtast transaktionstype: ")
            antal = int(input("Indtast antal: "))
            
            # Ensure correct format for datetime using datetime.strptime
            try:
                parsed_date = datetime.strptime(dato_og_tid, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                raise ValueError("Invalid datetime format. Use YYYY-MM-DD HH:MM:SS format.")
            
            statement = text("CALL OpretTransaktion(:vare_id, :p_dato_og_tid, :transaktionstype, :antal)")
            session.execute(statement, {"vare_id": vare_id, "p_dato_og_tid": parsed_date,
                                        "transaktionstype": transaktionstype, "antal": antal})
            session.commit()
            print("Transaktionen er oprettet.")
        except Exception as ex:
            print(f"Fejl ved oprettelse af transaktion: {ex}")

class Søgestrategi:
    def søg(self, parameter, cursor):
        pass

# Konkrete strategier
class SøgEfterID(Søgestrategi):
    def søg(self, vare_id, cursor):
        cursor.callproc('SøgEfterID', (vare_id,))
        result = cursor.fetchone()
        return result

class SøgEfterKategori(Søgestrategi):
    def søg(self, kategori_ID, cursor):
        cursor.callproc('SøgEfterKategori', (kategori_ID,))
        result = cursor.fetchall()
        return result

class SøgEfterTransaktion(Søgestrategi):
    def søg(self, transaktion_id, cursor):
        cursor.callproc('SøgEfterTransaktion', (transaktion_id,))
        result = cursor.fetchone()
        return result

class SøgEfterVare(Søgestrategi):
    def søg(self, vare_id, cursor):
        cursor.callproc('SøgEfterVare', (vare_id,))
        result = cursor.fetchone()
        return result

    engine = create_engine('mysql+mysqlconnector://root:Kom12345@localhost/lagerstyring')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)    


    