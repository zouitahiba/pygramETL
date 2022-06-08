from pygrametl.datasources import CSVSource

accident_file_handle = open('accidentsdelaroute.csv', 'r', 16384)
AccidentSource = CSVSource(accident_file_handle, delimiter=';')

def transformerDate(row):
    """Splits a timestamp containing a date into its three parts"""
    # Splitting of the timestamp into parts
    date = row['DateDebutInfraction']
    # Assignment of each part to the dictionary
    date_split = date.split('/')
    # Récupérer chaque élément à part et le rajouter dans le dictionnaire
    row['anneeTempsD'] = date_split[2]
    print('annee :' + row['anneeTempsD'])
    row['moisTempsD'] = date_split[1]
    print('mois :' + row['moisTempsD'])


for row in AccidentSource:
    print(transformerDate(row))