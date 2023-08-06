def query(table_name, column_names, where_clause):

    sql_str = (
        "select "
        + ",".join(column_names)
        + f" from `{table_name}` "
        + "where 1=1 "
        + where_clause
    )

    return sql_str


def get_model_data(conn, table_name, column_names, where_clause: str = ""):
    sql_str = query(table_name, column_names, where_clause)
    feature_df = conn.execute_query(sql_str)

    return feature_df
