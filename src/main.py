from entities.DBforbindelse import DBforbindelse
from menu import Menu

def main():
    # Establish database connection
    db_connection = DBforbindelse()
    session = db_connection.get_session()

    # Create a cursor for executing SQL statements
    cursor = session.connection().connection.cursor()

    # Create a menu instance with the session and cursor
    menu = Menu(session, cursor)

    # Run the main menu
    menu.kør_hovedmenu()

    # Close the session after menu execution
    session.close()

if __name__ == "__main__":
    main()