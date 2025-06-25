"""
Database management utility for the Museum API
Provides functions to update database schema safely
"""

import sys
from db.database import (
    create_tables,
    drop_tables,
    update_tables,
    add_column,
    drop_column,
    engine
)


def show_menu():
    """Display the main menu"""
    print("\n=== Database Management Tool ===")
    print("1. Create all tables")
    print("2. Drop all tables")
    print("3. Update tables (drop and recreate - WARNING: loses data)")
    print("4. Add column to table")
    print("5. Drop column from table")
    print("6. Show current table structure")
    print("7. Exit")
    print("================================")


def add_column_interactive():
    """Interactive function to add a column"""
    table_name = input("Enter table name: ")
    column_name = input("Enter column name: ")
    column_type = input("Enter column type (e.g., VARCHAR(255), INTEGER, BOOLEAN): ")

    nullable = input("Is column nullable? (y/n): ").lower() == 'n'
    default_value = input("Enter default value (or press Enter for none): ")

    kwargs = {'nullable': not nullable}
    if default_value:
        kwargs['default'] = default_value

    try:
        add_column(table_name, column_name, column_type, **kwargs)
        print(f"✅ Successfully added column '{column_name}' to table '{table_name}'")
    except Exception as e:
        print(f"❌ Error adding column: {e}")


def drop_column_interactive():
    """Interactive function to drop a column"""
    table_name = input("Enter table name: ")
    column_name = input("Enter column name: ")

    confirm = input(f"Are you sure you want to drop column '{column_name}' from table '{table_name}'? (y/n): ")
    if confirm.lower() != 'y':
        print("Operation cancelled.")
        return

    try:
        drop_column(table_name, column_name)
        print(f"✅ Successfully dropped column '{column_name}' from table '{table_name}'")
    except Exception as e:
        print(f"❌ Error dropping column: {e}")


def show_table_structure():
    """Show the current structure of all tables"""
    try:
        with engine.connect() as connection:
            # Get all table names using SQLAlchemy text()
            from sqlalchemy import text
            result = connection.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result]

            for table in tables:
                print(f"\n📋 Table: {table}")
                print("-" * 50)

                # Get table structure using SQLAlchemy text()
                result = connection.execute(text(f"DESCRIBE {table}"))
                columns = result.fetchall()

                for column in columns:
                    field, type_info, null, key, default, extra = column
                    print(f"  {field:<20} {type_info:<20} {null:<5} {key:<5} {default or 'NULL':<10}")

    except Exception as e:
        print(f"❌ Error showing table structure: {e}")


def main():
    """Main function"""
    while True:
        show_menu()
        choice = input("Enter your choice (1-7): ")

        try:
            if choice == '1':
                print("Creating all tables...")
                create_tables()
                print("✅ Tables created successfully!")

            elif choice == '2':
                confirm = input("Are you sure you want to drop all tables? This will delete all data! (y/n): ")
                if confirm.lower() == 'y':
                    print("Dropping all tables...")
                    drop_tables()
                    print("✅ Tables dropped successfully!")
                else:
                    print("Operation cancelled.")

            elif choice == '3':
                confirm = input("WARNING: This will drop and recreate all tables, losing all data! Continue? (y/n): ")
                if confirm.lower() == 'y':
                    print("Updating tables...")
                    update_tables()
                    print("✅ Tables updated successfully!")
                else:
                    print("Operation cancelled.")

            elif choice == '4':
                add_column_interactive()

            elif choice == '5':
                drop_column_interactive()

            elif choice == '6':
                show_table_structure()

            elif choice == '7':
                print("Goodbye!")
                sys.exit(0)

            else:
                print("❌ Invalid choice. Please enter a number between 1 and 7.")

        except Exception as e:
            print(f"❌ Error: {e}")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
