from core.database import get_db1

#from core.database import admin_test
from core.database import get_db



def log_api_usage(
    user_id,
    api_key,
    ip_address,
    endpoint
):

    #conn = admin_test()
    conn=get_db1()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            INSERT INTO api_usage
            (
                user_id,
                api_key,
                ip_address,
                endpoint
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s
            )
            """,
            (
                user_id,
                api_key,
                ip_address,
                endpoint
            )
        )

        conn.commit()

    finally:

        cur.close()
        conn.close()


def log_download(
    user_id,
    email,
    format_name,
    ip_address
):

    #conn = admin_test()
    conn=get_db1()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            INSERT INTO download_logs
            (
                user_id,
                email,
                format_name,
                ip_address
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s
            )
            """,
            (
                user_id,
                email,
                format_name,
                ip_address
            )
        )

        conn.commit()

    finally:

        cur.close()
        conn.close()