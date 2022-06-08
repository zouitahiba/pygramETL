import psycopg2
import pygrametl
from pygrametl.datasources import CSVSource
from pygrametl.tables import Dimension, FactTable

pgconn = psycopg2.connect(dbname='SecuriteRoutiere', user='postgres', password='chabou19')
connection = pygrametl.ConnectionWrapper(pgconn)
connection.setasdefault()
#"set search_path to" - Add Folder Paths to the Windows Path Variable for Easy Access
connection.execute('set search_path to "SecuriteRoutiere"')
print('connection établie')

accident_file_handle = open('accidentsdelaroute.csv', 'r', 16384)
AccidentSource = CSVSource(accident_file_handle, delimiter=';')
print('lecture du fichier réussie')

# Creation of dimension and fact table abstractions for use in the ETL flow
TempsDebutEv_dimension = Dimension(
    name='TempsDebutEv',
    key='id_TempsD',
    attributes=['moisTempsD', 'anneeTempsD'])

Location_dimension = Dimension(
    name='LocationA',
    key='id_Location',
    attributes=['Rue', 'Codemunicipal'])

Evenement_dimension = Dimension(
    name='Evenement',
    key='id_Evenement',
    attributes=['nombrePersonneEv']
)

Accident_Fact = FactTable(
    name='Accident',
    keyrefs=['id_Location', 'id_Evenement', 'id_TempsD'],
    measures=['montantDommage'])


# Python function needed to split the date into its three parts
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


for row in AccidentSource:
    print(row)
    row['id_TempsD'] = row['DateDebutInfraction']
    #
    transformerDate(row)
    row['id_TempsD'] = TempsDebutEv_dimension.ensure(row)
    row['id_Evenement'] = row['Numerodevenement']
    row['nombrePersonneEv'] = pygrametl.getint(row['Nombredepersonnesaudossier'])
    row['id_Evenement'] = Evenement_dimension.ensure(row)

    #ke thebb thezz contenu mtaa fichier lel db direct
    # for row in esm_fichier:
    #      esmtable.ensure(row)

    row['id_Location'] = row['Rue'] + row['Codemunicipal']
    Location_dimension.ensure(row)
    #row['id_Location'] = Location_dimension.ensure(row)
    ##
    row['montantDommage'] = pygrametl.getint(row['montantDommage'])
    ##    # The row can then be inserted into the fact table
    Accident_Fact.ensure(row)

# The datawarehouse connection is then ordered to commit and close
connection.commit()
connection.close()

# Finally the connection to the database is closed
pgconn.close()
