import pandas as pd
import sqlite3 as sql


def get_view_overview_result(city, big_lab):
    conn = sql.connect("travel.db")
    # df_query = pd.read_sql_query(querytable, conn, params=(city, tmp))

    placeholders = ','.join(['?'] * len(big_lab))
    querytable = f"SELECT * FROM view_overview WHERE rw_city like ? AND big_lab IN ({placeholders})"
    df_query = pd.read_sql_query(querytable, conn, params=(city, *big_lab))
    conn.close()  
    return df_query


def get_view_overview_result_2(city, big_lab):
    conn = sql.connect("travel.db")
    # df_query = pd.read_sql_query(querytable, conn, params=(city, tmp))

    placeholders = ','.join(['?'] * len(big_lab))
    querytable = f"SELECT * FROM view_overview WHERE rw_city like ? AND big_lab NOT IN ({placeholders})"
    df_query = pd.read_sql_query(querytable, conn, params=(city, *big_lab))
    conn.close()  
    return df_query



# # Test
# city="桃園市"
# category=["旅遊景點"]
# df = get_view_overview_result(city, category)
# print(df.head(2))
# print(len(df))
def get_result_by_name(names):
    conn = sql.connect("travel.db")
    placeholders = ','.join(['?'] * len(names))
    querytable = f"SELECT * FROM view_overview WHERE name IN ({placeholders})"
    df_query = pd.read_sql_query(querytable, conn, params=(*names,))
    conn.close()
    return df_query

def get_result_by_city(city):
    conn = sql.connect("travel.db")

    querytable = "SELECT * FROM view_overview WHERE rw_city like (?)"
    df_query = pd.read_sql_query(querytable, conn, params=(city,))
    conn.close()
    return df_query

def get_result_by_all_city():
    conn = sql.connect("travel.db")
    querytable = "SELECT * FROM view_overview"
    df_query = pd.read_sql_query(querytable, conn)
    conn.close()
    return df_query


# print(get_view_overview_result('宜蘭%','公園'))