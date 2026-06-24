#from core.database import get_db1
#from core.database import 
'''from core.database import admin_test


def log_api_usage(
    user_id,
    endpoint
):
def log_api_usage(    #added to check user actions
        user_id,
        api_key,
        ip_address,
        endpoint
):

    #conn = get_db1()
    #conn = get_aoi_db()
    conn = admin_test()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            INSERT INTO api_usage_logs
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
                endpoint
            )
        )

        conn.commit()

    finally:
        cur.close()
        conn.close()


def log_download(
    user_id,
    format_name
):

    conn = get_db1()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            INSERT INTO download_logs
            (
                user_id,
                format_name
            )
            VALUES
            (
                %s,
                %s
            )
            """,
            (
                user_id,
                format_name
            )
        )

        conn.commit()

    finally:
        cur.close()
        conn.close()
from core.database import admin_test


def log_download(
    user_id,
    email,
    api_key,
    file_format,
    ip_address
):

    conn = admin_test()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            INSERT INTO download_logs
            (
                user_id,
                email,
                api_key,
                download_format,
                ip_address
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s
            )
            """,
            (
                user_id,
                email,
                api_key,
                file_format,
                ip_address
            )
        )

        conn.commit()

    finally:

        cur.close()
        conn.close()'''
from core.database import admin_test


def log_api_usage(
    user_id,
    api_key,
    ip_address,
    endpoint
):

    conn = admin_test()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            INSERT INTO api_usage_logs
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
    api_key,
    file_format,
    ip_address
):

    conn = admin_test()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            INSERT INTO download_logs
            (
                user_id,
                email,
                api_key,
                download_format,
                ip_address
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s
            )
            """,
            (
                user_id,
                email,
                api_key,
                file_format,
                ip_address
            )
        )

        conn.commit()

    finally:

        cur.close()
        conn.close()