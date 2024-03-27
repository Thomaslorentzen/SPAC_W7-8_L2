# Interface for søgestrategi
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
    def søg(self, kategori, cursor):
        cursor.callproc('SøgEfterKategori', (kategori,))
        result = cursor.fetchall()
        return result

# Kontekstklassen, der anvender søgestrategien
class Søgning:
    def __init__(self, strategi):
        self.strategi = strategi

    def udfør_søgning(self, parameter, cursor):
        return self.strategi.søg(parameter, cursor)
