#Matt curran

import sys
import requests
import secrets
import sqlite3 as db
from typing import Tuple


def get_top_250_data() -> list[dict]:
    api_query = f"https://imdb-api.com/en/API/Top250TVs/{secrets.My_key}"
    response = requests.get(api_query)
    if response.status_code != 200:  # if we don't get an ok response we have trouble
        print(f"Failed to get data, response code:{response.status_code} and error message: {response.reason} ")
        sys.exit(-1)
    # jsonresponse is a kinda useless dictionary, but the items element has what we need
    jsonresponse = response.json()
    show_list = jsonresponse["items"]
    return show_list


def report_results(data_to_write: list[dict]):
    with open("Output.txt", mode='a') as outputFile:  # open the output file for appending
        for show in data_to_write:
            print(show, file=outputFile)  # write each data item to file
            print("\n", file=outputFile)
            print("===================================================================", file=outputFile)


def get_ratings(top_show_data: list[dict]) -> list[dict]:
    results = []
    api_queries = []
    base_query = f"https://imdb-api.com/en/API/UserRatings/{secrets.My_key}/"
    wheel_of_time_query = f"{base_query}tt7462410"
    api_queries.append(wheel_of_time_query)
    first_query = f"{base_query}{top_show_data[0]['id']}"
    api_queries.append(first_query)
    fifty_query = f"{base_query}{top_show_data[49]['id']}"
    api_queries.append(fifty_query)
    hundred_query = f"{base_query}{top_show_data[99]['id']}"
    api_queries.append(hundred_query)
    two_hundered = f"{base_query}{top_show_data[199]['id']}"
    api_queries.append(two_hundered)
    for query in api_queries:
        response = requests.get(query)
        if response.status_code != 200:  # if we don't get an ok response we have trouble, skip it
            print(f"Failed to get data, response code:{response.status_code} and error message: {response.reason} ")
            continue
        rating_data = response.json()
        results.append(rating_data)
    return results


def open_db(filename: str) -> Tuple[db.Connection, db.Cursor]:
    db_connection = db.connect("capstone.sqlite")
    cursor = db_connection.cursor()
    return db_connection, cursor


def setup_db(cursor: db.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS headline(
    show_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    full_title TEXT NOT NULL,
    show_year INTEGER,
    crew TEXT NOT NULL,
    rating INTEGER,
    rating_count INTEGER
    );''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS ratings(
    FOREIGN KEY(show_id) REFERENCES headline (show_id)
    ON DELETE CASCADE ON UPDATE NO ACTION,
    total_rating INTEGER,
    total_rating_votes INTEGER,
    ten_percent INTEGER,
    ten_rvotes INTEGER,
    nine_percent INTEGER,
    nine_rvotes INTEGER,
    eight_percent INTEGER,
    eight_rvotes INTEGER,
    seven_rvotes INTEGER,
    six_percent INTEGER,
    six_rvotes INTEGER,
    five_percent INTEGER,
    five_rvotes INTEGER,
    four_percent INTEGER,
    four_rvotes INTEGER,
    three_percent INTEGER,
    three_rvotes INTEGER,
    two_percent INTEGER,
    two_rvotes INTEGER,
    one_percent INTEGER,
    one_rvotes INTEGER );''')


def populate_tables(cursor: db.Cursor):
    try:
        datafile = open("Output.txt", "r")
    except:
        print("file not found.")

    data = datafile.read()
    data = data.split()

    for i in range(0, len(data), 6):
        show_id = data[i]
        title = data[i+2]
        full_title = data[i+1]
        year = data[i+1]
        crew = data[i+2]
        rating = data[+1]
        rating_count = data[+1]
        cursor.execute('''INSERT INTO HEADLINE(show_id, title, full_title, show_year, crew, rating, rating_count) 
        VALUES (?,?,?,?,?,?,?)''', (show_id, title, full_title, year, crew, rating, rating_count))


def close_db(conn: db.Connection):
    conn.commit()
    conn.close()


def main():
    conn, cursor = open_db("capstone.sqlite")
    print(type(conn))
    top_show_data = get_top_250_data()
    ratings_data = get_ratings(top_show_data)
    report_results(ratings_data)
    report_results(top_show_data)
    close_db(conn)


if __name__ == '__main__':
    main()


