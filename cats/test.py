from cats.database import *

db = Database(dbtype='sqlite', dbname='data.db')

druh = Druh()
druh.jmeno_druhu = 'NOVINKA - Britský netopýr s fešáckým knírem'
db.create_druh(druh)

foto = Fotka()
foto.nazev_fotky = 'Nalezení poblíž stříbrného jezera'
foto.url = 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.reddit.com%2Fr%2Fowo%2Fcomments%2Fi70d0i%2Fowo_cat%2F&psig=AOvVaw3rlTkI0vRdw8b0mJEcpwAg&ust=1618255856341000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCLjT__729u8CFQAAAAAdAAAAABAD'
db.create_fotka(foto)

popis = Popis()
popis.jmeno = 'Uwu'
popis.vek = 5
popis.vaha = 10
popis.samotny_popis = 'Hele pořádně ani nvm co tohle je za kočku - poznámka veterinářky Adély Pavlincové'
db.create_popis(popis)

