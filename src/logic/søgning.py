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
        cursor.callproc('SøfEfterVare', (vare_id,))
        result = cursor.fetchone()
        return result


    

