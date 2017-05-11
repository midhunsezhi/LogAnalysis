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
               LIMIT 3")

    articles = c.fetchall()
    for article in articles:
        print(article[0] + " - " + str(article[1]) + " views")
    DB.close()


def popularAuthors():
    """Returns the popular authors of all time"""
    DB = connect()
    c = DB.cursor()

    c.execute("SELECT authors.name, count(*) AS frequency \
               FROM articles, authors, log \
               WHERE '/article/' || articles.slug = log.path \
               AND articles.author = authors.id \
               GROUP BY authors.name \
               ORDER BY frequency DESC")

    authors = c.fetchall()
    for author in authors:
        print(author[0] + " - " + str(author[1]) + " views")
    DB.close()


def highFailureDays():
    """Returns the days with more than 1% error rate"""
    DB = connect()
    c = DB.cursor()

    c.execute("WITH hitlog as \
                    (SELECT to_char(time, 'Month DD, YYYY') as day, \
                     COUNT(*) as pagehits \
                     FROM log \
                     GROUP BY day) \
               , failurelog as \
                    (SELECT day, COUNT(*) as failures \
                     FROM hitlog, log \
                     WHERE to_char(time, 'Month DD, YYYY') = day \
                     AND log.status != '200 OK' \
                     GROUP BY day) \
               SELECT hitlog.day, \
               (failures::decimal / pagehits::decimal) * 100 as errorrate \
               FROM hitlog, failurelog \
               WHERE hitlog.day = failurelog.day \
               AND (failures::decimal / pagehits::decimal) > 0.01 \
               ORDER BY errorrate")

    days = c.fetchall()
    for day in days:
        print(str(day[0]) + " - " + str(round(day[1], 2)) + "% errors")
    DB.close()


if __name__ == '__main__':
    print("\n" + ("*" * 75) + "\n")

    print("The most popular three articles of all time are as follows: \n")
    popularArticles()

    print("\n" + "Popularity of authors is as follows (Most popular first) " \
          + "\n")
    popularAuthors()

    print("\n" + "The days on which more than 1% of requests lead to errors \
          are as follows: " + "\n")
    highFailureDays()

    print("\n" + ("*" * 75) + "\n")
