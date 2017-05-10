#!/usr/bin/env python3

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=news")

def popularArticles():
    """Returns the top 3 popular articles."""
    DB = connect()
    c = DB.cursor()

    c.execute("SELECT articles.title as title, count(*) AS frequency \
               FROM articles, log \
               WHERE '/article/' || articles.slug = log.path \
               GROUP BY title \
               ORDER BY frequency DESC \
               LIMIT 3 \
              ")
    articles = c.fetchall()
    for article in articles:
        print(article[0] + " - " + str(article[1]) + " views")
    DB.close()

if __name__ == '__main__':
    print("The most popular three articles of all time are as follows: \n")
    popularArticles()
