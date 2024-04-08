import duckdb
from palmerpenguins import penguins

con = duckdb.connect('my-db.duckdb')
df = penguins.load_penguins()
con.execute('CREATE TABLE penguins AS SELECT * FROM df')
con.close()