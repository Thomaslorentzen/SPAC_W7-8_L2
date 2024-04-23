
from entities.DBforbindelse import DBforbindelse
from entities.items import Kategori, Transaktion , Vare, SøgEfterKategori, SøgEfterVare, SøgEfterTransaktion

class Menu:
    def __init__(self, session, cursor):
        self.session = session
        self.cursor = cursor
        self.vare_handler = VareHandler(session, cursor)
        self.kategori_handler = KategoriHandler(session, cursor)
        self.transaktions_handler = TransaktionsHandler(session, cursor)

    def vis_hovedmenu(self):
        print("Velkommen til hovedmenuen")
        print("Vælg mellem menuen for varer eller kategori")
        print("1. Varer")
        print("2. Kategori")
        print("3. Transaktion")
        print("4. Afslut")
    
    def kør_hovedmenu(self):
        while True:
            self.vis_hovedmenu()
            valg = input("Vælg en handling: ")

            if valg == "1":
                self.kør_vare_menu()
            elif valg == "2":
                self.kør_kategori_menu()
            elif valg == "3":
                self.kør_transaktions_menu()
            elif valg == "4":
                print("Afslutter program...")
                break
            else:
                print("Ugyldigt valg. Prøv igen.")

    def vis_vare_menu(self):
        print("Varehåndtering:")
        print("1. Tilføj vare")
        print("2. Opdater vare")
        print("3. Slet vare")
        print("4. Vis vare information")
        print("5. Søg efter vare")
        print("6. Tilbage til hovedmenu")

    def kør_vare_menu(self):
        while True:
            self.vis_vare_menu()
            valg = input("Vælg en handling: ")

            if valg == "1":
                self.vare_handler.tilføj_vare()
            elif valg == "2":
                self.vare_handler.opdater_vare()
            elif valg == "3":
                self.vare_handler.slet_vare()
            elif valg == "4":
                vare_ID = int(input("Indtast ID på varen, som skal vises: "))  # Prompt for vare_ID
                self.vare_handler.vis_vare_info(vare_ID)  # Pass vare_ID to the method

            elif valg == "5":
                self.vare_handler.søg_efter_vare(self.cursor)  
            elif valg == "6":
                print("Tilbage til hovedmenu...")
                break
            else:
                print("Ugyldigt valg. Prøv igen.")

    def vis_kategori_menu(self):
        print("Kategoriadministration:")
        print("1. Tilføj kategori")
        print("2. Opdater kategori")
        print("3. Slet kategori")
        print("4. Vis kategori information")
        print("5. Søg efter kategori") 
        print("6. Tilbage til hovedmenu")

    def kør_kategori_menu(self):
        while True:
            self.vis_kategori_menu()
            valg = input("Vælg en handling: ")

            if valg == "1":
                self.kategori_handler.tilføj_kategori()
            elif valg == "2":
                self.kategori_handler.opdater_kategori()
            elif valg == "3":
                self.kategori_handler.slet_kategori()
            elif valg == "4":
                self.kategori_handler.vis_kategori_info()
            elif valg == "5":
                self.kategori_handler.søg_efter_kategori(self.cursor)
            elif valg == "6":
                print("Tilbage til hovedmenu...")
                break
            else:
                print("Ugyldigt valg. Prøv igen.")

    def vis_transaktions_menu(self):
        print("Transaktionsadministration:")
        print("1. Opret transaktion")
        print("2. Registrer transaktion")
        print("3. Søg efter vare")
        print("4. Generer transaktionsrapport")  # Ny mulighed
        print("5. Tilbage til hovedmenu")

    def kør_transaktions_menu(self):
        while True:
            self.vis_transaktions_menu()
            valg = input("Vælg en handling: ")

            if valg == "1":
                self.transaktions_handler.opret_transaktion()
            elif valg == "2":
                self.transaktions_handler.registrer_transaktion()
            elif valg == "3":
                self.transaktions_handler.søg_efter_transaktion(self.cursor)  
            elif valg == "4":  # Ny case for at generere rapport
                self.generer_transaktionsrapport()
            elif valg == "5":
                print("Tilbage til hovedmenu...")
                break
            else:
                print("Ugyldigt valg. Prøv igen.")  
    
    def generer_transaktionsrapport(self):
        while True:
            try:
                vare_ID = int(input("Indtast ID på varen, du vil generere en rapport for: "))
                transaktioner = Transaktion.hent_transaktioner_for_vare(vare_ID, self.session)
                if transaktioner:
                    print("\nTransaktionsrapport for vare med ID {}:\n".format(vare_ID))
                    print("{:<15} {:<25} {:<20} {:<10}".format("Transaktion ID", "Dato og tid", "Transaktionstype", "Antal"))
                    print("-" * 70)
                    for transaktion in transaktioner:
                        transaktion_ID, dato_og_tid, _, _, antal, transaktionstype = transaktion
                        print("{:<15} {:<25} {:<20} {:<10}".format(transaktion_ID, dato_og_tid, transaktionstype, antal))
                    print("\n")
                    break  # Stop loopet hvis alt er i orden
                else:
                    print("Ingen transaktioner fundet for denne vare.")
                    return  # Gå tilbage til transaktionsmenuen
            except ValueError:
                print("Ugyldigt vare-ID. Prøv igen.")
                return  # Gå tilbage til transaktionsmenuen
            

class VareHandler:
    def __init__(self, session, cursor):
        self.session = session
        self.cursor = cursor

    def tilføj_vare(self):
        name = input("Indtast navn på varen: ")
        beskrivelse = input("Indtast beskrivelse af varen: ")
        kategori_ID = int(input("Indtast kategori ID: "))
        pris = float(input("Indtast pris på varen: "))
        lager_antal = int(input("Indtast lagerantal på varen: "))

        # Call the static method from the Vare class and pass all the required arguments
        Vare.tilføj_vare(name, beskrivelse, kategori_ID, pris, lager_antal, self.session)
        print("Varen er tilføjet.")

    def opdater_vare(self):
        vare_ID = int(input("Indtast ID på varen, som skal opdateres: "))
        name = input("Indtast nyt navn på varen: ")
        beskrivelse = input("Indtast ny beskrivelse af varen: ")
        kategori_ID = int(input("Indtast ny kategori ID: "))
        pris = float(input("Indtast ny pris på varen: "))
        lager_antal = int(input("Indtast nyt lagerantal på varen: "))

        vare = Vare(name, beskrivelse, kategori_ID, pris, lager_antal)
        vare.vare_ID = vare_ID  # Set the vare_ID for updating
        vare.opdater_vare(vare_ID, name, beskrivelse, kategori_ID, pris, lager_antal, self.session)

        print("Varen er opdateret.")

    def slet_vare(self):
        vare_ID = int(input("Indtast ID på varen, som skal slettes: "))
        vare = Vare("", "", 0, 0, 0)  # Dummy object
        vare.slet_vare(vare_ID, self.session)  # Pass session parameter
        print("Varen er slettet.")


    def vis_vare_info(self, vare_ID):
        result = Vare.vis_vare_info(self.session, vare_ID)
        print(result)
    
    def søg_efter_vare(self, cursor):
        parameter = input("Indtast søgeparameter for vare: ")
        søgning = SøgEfterVare()
        result = søgning.søg(parameter, cursor)  # Pass the cursor here
        print(result)  # Display search results

class KategoriHandler:
    def __init__(self, session, cursor):
        self.session = session
        self.cursor = cursor

        

    def tilføj_kategori(self):
            navn = input("Indtast navn på kategorien: ")
            beskrivelse = input("Indtast beskrivelse af kategorien: ")

            try:
                print("Attempting to add category...")
                ny_kategori = Kategori(navn, beskrivelse)
                ny_kategori.tilføj_kategori(navn, beskrivelse, self.session)
                print("Kategorien er tilføjet.")
            except Exception as ex:
                print("An error occurred while adding category:", str(ex))

    def opdater_kategori(self):
        kategori_ID = int(input("Indtast ID på kategorien, som skal opdateres: "))
        navn = input("Indtast nyt navn på kategorien: ")
        beskrivelse = input("Indtast ny beskrivelse af kategorien: ")

        Kategori.opdater_kategori(kategori_ID, navn, beskrivelse, self.session)
        print("Kategorien er opdateret.")


    def søg_efter_kategori(self, cursor):
        parameter = input("Indtast søgeparameter for kategori: ")
        søgning = SøgEfterKategori()
        result = søgning.søg(parameter, cursor)  
        print(result)  

    def slet_kategori(self):
        kategori_ID = int(input("Indtast ID på kategorien, som skal slettes: "))
        kategori = Kategori("", "")  # Dummy object
        kategori.kategori_ID = kategori_ID
        kategori.slet_kategori(kategori_ID, self.session)
        print("Kategorien er slettet.")

    def vis_kategori_info(self, kategori_ID):
        kategori_ID = int(input("Indtast ID på kategorien, som skal vises: "))
        result = Kategori.vis_kategori_info(self.session, kategori_ID)
        print(result)

class TransaktionsHandler:
    def __init__(self, session, cursor):
        self.session = session
        self.cursor = cursor
    
    def opret_transaktion(self):
        try:
            transaktion = Transaktion()
            transaktion.opret_transaktion(self.session)
            print("Transaktionen er oprettet.")
        except Exception as ex:
            print(f"Fejl ved oprettelse af transaktion: {ex}")

    def registrer_transaktion(self):
        try:
            self.opret_transaktion()  # Call the method to create the transaction only once
            print("Transaktionen er registreret.")
        except Exception as ex:
            print(f"Fejl ved registrering af transaktion: {ex}")

    def søg_efter_transaktion(self, cursor):
        parameter = input("Indtast søgeparameter for transaktion: ")
        søgning = SøgEfterTransaktion()  
        result = søgning.søg(parameter, cursor)  
        print(result)  


