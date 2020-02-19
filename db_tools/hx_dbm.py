from db_tools import MyDBM
import datetime

table_base = 'news_{}_hx'
create_news_table = '''create table {}(
id int primary key auto_increment,
url varchar(100),
title varchar(200),
description varchar(1000),
publish_time VARCHAR(20),
username varchar(20),
user_id int,
agree_number int,
favorite_number int,
video_url varchar(200),
comment_list varchar(500)
);'''
create_users_table = '''create table news_users_hx(
id int primary key auto_increment,
username varchar(20),
user_id int,
avatar varchar(200),
url varchar(100),
one_word varchar(400)
);'''
create_comment_table = '''create table news_comment_hx(
id int primary key auto_increment,
comment_id int,
username varchar(20),
user_id int,
content varchar(500),
publish_time varchar(20),
agree_number int,
disagree_number int
);'''
insert_news = '''insert {}
(url, title, description, publish_time, username, user_id, agree_number, favorite_number, video_url, comment_list)
values ({});'''
insert_users = '''insert news_users_hx
(username, user_id, avatar, url, one_word)
values ({});'''
insert_comment = '''insert news_comment_hx
(comment_id, username, user_id, content, publish_time, agree_number, disagree_number)
values ({});'''


class HxDBM(MyDBM):
    def dump_news(self, record):
        self.use_database()
        handler = self.database.cursor()
        cur_date = datetime.date.today().strftime('%Y_%m_%d')
        table = table_base.format(cur_date)
        if not self.is_exits_table(table):
            handler.execute(create_news_table.format(table))
        handler.execute(insert_news.format(table, str(record)[1:-1]))

        self.database.commit()

    def dump_users(self, record):
        self.use_database('news_users')
        handler = self.database.cursor()
        if not self.is_exits_table('news_users_hx'):
            handler.execute(create_users_table)
        is_exits = handler.execute(f'select user_id from news_users_hx where user_id = {record[1]};')
        if not is_exits:
            handler.execute(insert_users.format(str(record)[1:-1]))
            self.database.commit()

    def dump_comment(self, record):
        self.use_database('news_comment')
        handler = self.database.cursor()
        table = 'news_comment_hx'
        if not self.is_exits_table(table):
            handler.execute(create_comment_table)
        handler.execute(insert_comment.format(str(record)[1:-1]))
        self.database.commit()
