# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re


class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        fields = adapter.field_names()
        
        for field in fields:
            value = adapter.get(field)
            adapter[field] = str(value).strip()

        values = {'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5}

        adapter['category'] = adapter.get('category').lower()
        adapter['rating'] = adapter.get('rating').lower()
        adapter['rating'] = values[adapter.get('rating')]

        adapter['price'] = float(adapter.get('price')[1:])
        item_stock = re.search(r'\d+', adapter.get('stock'))
        if item_stock:
            item_stock = item_stock.group()[0]
        else:
            item_stock = 0
        adapter['stock'] = int(item_stock)

        return item
    

import mysql.connector

class SaveToMySQLPipeline:
    
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='admin',
            database='books'
        )
        
        self.cur = self.conn.cursor()

        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255),
                price FLOAT,
                stock INT,
                rating INT,
                description TEXT,
                upc VARCHAR(255),
                category VARCHAR(255),
                url TEXT
            )
        """)

    def process_item(self, item, spider):
        self.cur.execute("""
            INSERT INTO books (title, price, stock, rating, description, upc, category, url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            item['title'],
            item['price'],
            item['stock'],
            item['rating'],
            item['description'],
            item['upc'],
            item['category'],
            item['url']
        ))
        
        self.conn.commit()
        return item
    
    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

    