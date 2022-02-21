#Matt curran

import api_data
import database


def report_results(data_to_write: list):
    with open("Output.txt", mode='a') as outputFile:
        for show in data_to_write:
            print(show, file=outputFile)
            print("\n", file=outputFile)
            print("===================================================================", file=outputFile)


def main():
    connection, db_cursor = database.open_db("capstone.sqlite")
    database.create_top250_table(db_cursor)
    database.create_ratings_table(db_cursor)
    top_show_data = api_data.get_top_250_data()
    top_show_data_for_db = api_data.prepare_top_250_data(top_show_data)
    database.put_top_250_in_db(top_show_data_for_db, db_cursor)
    database.put_in_wheel_of_time(db_cursor)
    ratings_data = api_data.get_ratings(top_show_data)
    db_ready_ratings_data = api_data.prepare_ratings_for_db(ratings_data)
    database.put_ratings_into_db(db_ready_ratings_data, db_cursor)
    database.close_db(connection)


if __name__ == '__main__':
    main()


