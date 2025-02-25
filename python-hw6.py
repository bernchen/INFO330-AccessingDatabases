import sqlite3  # This is the package for all sqlite3 access in Python
import sys      # This helps with command-line parameters

# Connect to pokemon database
conn = sqlite3.connect("pokemon.db")
c = conn.cursor()

# All the "against" column suffixes:
types = ["bug","dark","dragon","electric","fairy","fight",
    "fire","flying","ghost","grass","ground","ice","normal",
    "poison","psychic","rock","steel","water"]

# Take six parameters on the command-line
if len(sys.argv) < 6:
    print("You must give me six Pokemon to analyze!")
    sys.exit()

team = []
for i, arg in enumerate(sys.argv):
    if i == 0:
        continue

    # Get the Pokemon's name, type(s), and "against_" columns from the pokemon database table
    c.execute(f"""SELECT *
        FROM imported_pokemon_data
        WHERE pokedex_number = {arg}""")
    row = c.fetchone()
    if row is None:
        print(f"Could not find a Pokemon with pokedex number {arg}")
        sys.exit()
    name = row[29]
    type1 = row[35]
    type2 = row[36]
    against = [float(row[i]) for i in range(1,19)]

    # You will need to write the SQL, extract the results, and compare
    # Remember to look at those "against_NNN" column values; greater than 1
    # means the Pokemon is strong against that type, and less than 1 means
    # the Pokemon is weak against that type

    # Analyze strong vs weak Pokemon based on types
    strong = []
    weak = []

#    for t in types:
#        if against[t] > 1:
#            strong.append(str(t))
#        elif against[t] < 1:
#            weak.append(str(t))

    for j, factor in enumerate(against):
        if factor > 1:
            strong.append(types[j])
        elif factor < 1:
            weak.append(types[j])
    
    # Print analysis results
    print(f"Analyzing {arg}")
    print(f"{name} ({type1}{' ' + str(type2) if type2 else ''}) is strong against {strong} but weak against {weak}")
    
# Ask the user if they want to save the team
answer = input("Would you like to save this team? (Y)es or (N)o: ")
if answer.upper() == "Y" or answer.upper() == "YES":
    teamName = input("Enter the team name: ")

    # Add Pokemon to team list
    team.append(name)

    # Insert and write the pokemon team to the "teams" table
    print("Saving " + teamName + " ...")
else:
    print("Bye for now!")

# Close the database connection
c.close()