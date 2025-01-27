import mysql.connector
import getpass

import colorama
from colorama import Fore, Back, Style

colorama.init(autoreset=True)

"""
disease
    id INT UNSIGNED AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL
    PRIMARY KEY (id),
    targets TEXT
target
    id INT UNSIGNED AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL
    PRIMARY KEY (id),
    type VARCHAR(255) NOT NULL,
    diseases TEXT,
    pathway TEXT,
    sequence TEXT,
    description TEXT
drug
    id INT UNSIGNED AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    targets_P TEXT,
    targets_N TEXT,
    diseases TEXT,
    description TEXT
"""

host = "localhost"
user = "root"  # input("Enter your MySQL username: ")
password = "123456"  # getpass.getpass("Enter your MySQL password: ")
database = "test"  # input("Enter your database name: ")

db = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    charset="utf8mb4",
)

cursor = db.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS %s" % database)
cursor.execute("USE %s" % database)


# cursor.execute("DROP TABLE IF EXISTS disease")
# cursor.execute("DROP TABLE IF EXISTS target")
# cursor.execute("DROP TABLE IF EXISTS drug")


cursor.execute(
    "CREATE TABLE IF NOT EXISTS `disease` (`id` INT UNSIGNED AUTO_INCREMENT, `name` VARCHAR(255) NOT NULL, `targets_P` TEXT, `targets_N` TEXT, PRIMARY KEY(`id`))"
)
cursor.execute(
    "CREATE TABLE IF NOT EXISTS `target` (`id` INT UNSIGNED AUTO_INCREMENT, `name` VARCHAR(255) NOT NULL, `type` VARCHAR(255) NOT NULL, `diseases` TEXT, `pathway` TEXT, `sequence` TEXT, `description` TEXT, PRIMARY KEY(`id`))"
)
cursor.execute(
    "CREATE TABLE IF NOT EXISTS `drug` (`id` INT UNSIGNED AUTO_INCREMENT, `name` VARCHAR(255) NOT NULL, `targets_P` TEXT, `targets_N` TEXT, `structure` TEXT, `description` TEXT, PRIMARY KEY(`id`))"
)

db.commit()

print(
    """
Welcome to the drug target management system!
    Available commands:
    - insert disease <name>
    - insert target <name> <type>
    - insert drug <name>
    - delete disease/target/drug <name>
    - describe target/drug <name> <description>
    - give pathway <target_name> <pathway>
    - give sequence <target_name> <sequence>
    - give structure <drug_name> <structure>
    - list disease/target/drug
    - bind/unbind <target_name> <disease_name>
    - bind/unbind <target_name> <drug_name> <positive_or_negative>
    - search <name>
    - find bind <name>
    - find treatment <disease_name>
    - find effect <drug_name>
    - exit
"""
)

print(Fore.YELLOW + "Copyright (c) 2025 distjr_")


def error(message):
    print(Fore.RED + "[ERROR] " + message)


while True:
    command = input(">").split()
    try:
        if len(command) == 0:
            continue
        if command[0] == "exit":
            break
        elif command[0] == "insert":
            if command[1] == "disease":
                cursor.execute("INSERT INTO disease (name) VALUES (%s)", (command[2],))
                db.commit()
            elif command[1] == "target":
                cursor.execute(
                    "INSERT INTO target (name, type) VALUES (%s, %s)",
                    (command[2], command[3]),
                )
                db.commit()
            elif command[1] == "drug":
                cursor.execute("INSERT INTO drug (name) VALUES (%s)", (command[2],))
                db.commit()
            else:
                error(
                    "Invalid command. Use 'insert disease', 'insert target', or 'insert drug'."
                )
        elif command[0] == "delete":
            if command[1] == "disease":
                cursor.execute("DELETE FROM disease WHERE name=%s", (command[2],))
                db.commit()
            elif command[1] == "target":
                cursor.execute("DELETE FROM target WHERE name=%s", (command[2],))
                db.commit()
            elif command[1] == "drug":
                cursor.execute("DELETE FROM drug WHERE name=%s", (command[2],))
                db.commit()
            else:
                error(
                    "Invalid command. Use 'delete disease', 'delete target', or 'delete drug'."
                )
        elif command[0] == "give":
            if command[1] == "pathway":
                cursor.execute(
                    "UPDATE target SET pathway=%s WHERE name=%s",
                    (command[3], command[2]),
                )
                db.commit()
            elif command[1] == "sequence":
                cursor.execute(
                    "UPDATE target SET sequence=%s WHERE name=%s",
                    (command[3], command[2]),
                )
                db.commit()
            elif command[1] == "structure":
                cursor.execute(
                    "UPDATE drug SET structure=%s WHERE name=%s",
                    (command[3], command[2]),
                )
                db.commit()
            else:
                error(
                    "Invalid command. Use 'give pathway', 'give sequence', or 'give structure'."
                )
        elif command[0] == "list":
            if command[1] == "disease":
                cursor.execute("SELECT name FROM disease")
                result = cursor.fetchall()
                print("Diseases:")
                for disease in result:
                    print(disease[0])
            elif command[1] == "target":
                cursor.execute("SELECT name FROM target")
                result = cursor.fetchall()
                print("Targets:")
                for target in result:
                    print(target[0])
            elif command[1] == "drug":
                cursor.execute("SELECT name FROM drug")
                result = cursor.fetchall()
                print("Drugs:")
                for drug in result:
                    print(drug[0])
            else:
                error(
                    "Invalid command. Use 'list disease', 'list target', or 'list drug'."
                )
        elif command[0] == "search":
            cursor.execute(
                "SELECT * FROM disease WHERE name LIKE %s", ("%" + command[1] + "%",)
            )
            result = cursor.fetchall()
            print("Matching diseases:")
            print("-" * 55)
            print(
                "%-5s\t%-10s\t%-20s\t%-20s"
                % ("ID", "Name", "Target(Positive)", "Target(Negative)")
            )
            print("=" * 55)
            for disease in result:
                print(
                    "%-5s\t%-10s\t%-20s\t%-20s"
                    % (disease[0], disease[1], disease[2], disease[3])
                )
            print("*" * 55 + "\n")

            cursor.execute(
                "SELECT * FROM target WHERE name LIKE %s", ("%" + command[1] + "%",)
            )
            result = cursor.fetchall()
            print("Matching targets:")
            print("-" * 90)
            print(
                "%-5s\t%-10s\t%-5s\t%-10s\t%-20s\t%-20s\t%-20s"
                % (
                    "ID",
                    "Name",
                    "Type",
                    "Disease",
                    "Pathway",
                    "Sequence",
                    "Description",
                )
            )
            print("=" * 90)
            for target in result:
                print(
                    "%-5s\t%-10s\t%-5s\t%-10s\t%-20s\t%-20s\t%-20s"
                    % (
                        target[0],
                        target[1],
                        target[2],
                        target[3],
                        target[4],
                        target[5],
                        target[6],
                    )
                )
            print("*" * 90 + "\n")

            cursor.execute(
                "SELECT * FROM drug WHERE name LIKE %s", ("%" + command[1] + "%",)
            )
            result = cursor.fetchall()
            print("Matching drugs:")
            print("-" * 95)
            print(
                "%-5s\t%-10s\t%-20s\t%-20s\t%-20s\t%-20s"
                % (
                    "ID",
                    "Name",
                    "Target(Positive)",
                    "Target(Negative)",
                    "Structure",
                    "Description",
                )
            )
            print("=" * 95)
            for drug in result:
                print(
                    "%-5s\t%-10s\t%-20s\t%-20s\t%-20s\t%-20s"
                    % (drug[0], drug[1], drug[2], drug[3], drug[4], drug[5])
                )
            print("*" * 95 + "\n")

        else:
            error("Invalid command.")
    except Exception as e:
        error(str(e))
    # elif command[0] == "describe":
    #     if command[1] == "target":
    #         cursor.execute(
    #             "SELECT description FROM target WHERE name=%s", (command[2],)
    #         )
    #         result = cursor.fetchone()
    #         if result:
    #             print(result[0])
    #         else:
    #             print("Target not found.")
    #     elif command[1] == "drug":
    #         cursor.execute(
    #             "SELECT description FROM drug WHERE name=%s", (command[2],)
    #         )
    #         result = cursor.fetchone()
    #         if result:
    #             print(result[0])
    #         else:
    #             print("Drug not found.")
    #     else:
    #         print("Invalid command. Use 'describe target' or 'describe drug'.")


cursor.close()

db.close()

print(Fore.YELLOW + "Goodbye!")
