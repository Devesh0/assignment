import db_queries


def get_company_list():
    """Get the top 10 company list having call_status True. """
    sql_query = "SELECT company_id,client_number \
                FROM requests \
                WHERE call_status=%s LIMIT 10" % (True,)

    company_list = db_queries.query_fetchall(sql_query)
    return company_list


def get_server_list():
    """Returns the dictionary of servers allocated to the companies."""
    sql_query = "SELECT company_server.company_id,servers.server_name \
                FROM servers \
                JOIN company_server ON company_server.server_id = servers.server_id"

    servers = db_queries.query_fetchall(sql_query)
    server_list = {}
    for key, value in servers:
        server_list.setdefault(key, []).append(value)
    return server_list


def get_server_threshold():
    """Returns the server threshold that is maximum_call-call_running."""
    sql_query = "SELECT server_name,(max_call-call_running) as call_count \
                FROM servers"

    call_count = db_queries.query_fetchall(sql_query)
    call_count = dict(call_count)
    return call_count
