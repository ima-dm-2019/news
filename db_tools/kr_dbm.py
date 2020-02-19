from db_tools import MyDBM
import datetime

table_base = 'news_{}_kr'
create_news_table = '''create table {}(
id int primary key auto_increment,
url varchar(100),
title varchar(200),
description varchar(1000),
publish_time VARCHAR(20),
username varchar(20)
);
'''
insert_news = '''insert {}
(url, title, description, publish_time, username)
values ({})
'''


class KrDBM(MyDBM):
    def dump_news(self, record):
        handler = self.database.cursor()
        cur_date = datetime.date.today().strftime('%Y_%m_%d')
        table = table_base.format(cur_date)
        if not self.is_exits_table(table):
            handler.execute(create_news_table.format(table))
        handler.execute(insert_news.format(table, str(record)[1:-1]))
        self.database.commit()
