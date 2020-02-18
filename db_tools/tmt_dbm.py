from db_tools import MyDBM
import datetime
table_base = 'news_{}_tmt'
create_news_table = '''create table {}(
id int primary key auto_increment,
url varchar(100),
title varchar(200),
publish_time VARCHAR(5),
likes int
);
'''
insert_news = '''insert {}
(url, title, publish_time, likes)
values ({})
'''


class TmtDBM(MyDBM):
    def dump_news(self, record):
        handler = self.database.cursor()
        cur_date = datetime.date.today().strftime('%Y_%m_%d')
        table = table_base.format(cur_date)
        if not self.is_exits_table(table):
            handler.execute(create_news_table.format(table))
        handler.execute(insert_news.format(table, str(record)[1:-1]))
        self.database.commit()

# a = TmtDBM()
# a.dump_news(['1','1','11:11','1'])