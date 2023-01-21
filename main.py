import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Shop, Stock, Sale

DNS = 'postgresql://postgres:postgres@localhost:5432/book_shops'
engine = sqlalchemy.create_engine(DNS)
create_tables(engine)

Session  = sessionmaker(bind=engine)
session = Session()

with open('test_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))

session.commit()

publisher_input = input('Введите имя или идентификатор издателя: ')

for c in session.query(
    Book.title, 
    Shop.name, 
    Sale.price, 
    Sale.date_sale).join(
        Publisher, Book.id_publisher == Publisher.id).join(
            Stock, Book.id == Stock.id_book).join(
                Shop, Shop.id == Stock.id_book).join(
                    Sale, Stock.id == Sale.id_stock).filter(
                        Publisher.name == publisher_input):
    print(c)

session.close()