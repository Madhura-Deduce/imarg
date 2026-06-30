# core.database import get_db1
from core.database import get_db1
import uuid
from fastapi import HTTPException
#from core.database import admin_test
from core.config import PLAN_PRICES



def create_payment(
        user_id,
        email,
        #api_key,
        #ip_address,
        plan_name,
        duration_type
):

    #conn = admin_test()
    #conn = admin_test()
    conn=get_db1()
    #print(conn.get_dsn_parameters())
    cur = conn.cursor()

    try:

        
        # Check current subscription
    
        cur.execute(
            """
            SELECT subscription_type,full_name                
            FROM users
            WHERE id=%s
            """,
            (user_id,)
        )

        user = cur.fetchone()
        full_name=user["full_name"]

        if user and user["subscription_type"] == plan_name:

            raise HTTPException(
                status_code=400,
                detail=f"Already subscribed to {plan_name}"
            )

        
        # Check pending payment
        
        cur.execute(
            """
            SELECT id, order_id
            FROM payments
            WHERE
                user_id=%s
                AND plan_name=%s
                AND payment_status='CREATED'
            ORDER BY created_at DESC
            LIMIT 1
            """,
            (
                user_id,
                plan_name
            )
        )

        existing_payment = cur.fetchone()

        if existing_payment:

            return {
                "payment_id": existing_payment["id"],
                "order_id": existing_payment["order_id"],
                "payment_status": "CREATED",
                "message": "Pending payment already exists"
            }

        
        # Create new payment
    
        amount = PLAN_PRICES[plan_name][duration_type]

        order_id = f"ORD_{uuid.uuid4().hex[:12]}"
        #print("payment_id =", payment_id)

        cur.execute(
            """
            INSERT INTO payments
            (
                user_id, 
                email, 
                full_name, 
                order_id,
                plan_name, 
                duration_type, 
                amount, 
                payment_status, 
                payment_gateway
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
            RETURNING id
            """,
            (
                user_id,
                email,
                full_name,
                order_id,
                plan_name,
                duration_type,
                amount,
                "CREATED",
                "MANUAL"
            )
        )
        print("Inserted into subscription_history")

        payment = cur.fetchone()
        print("payment=",payment)

        conn.commit()

        return {
            "payment_id": payment["id"],
            "order_id": order_id,
            "amount": amount,
            "payment_status": "CREATED"
        }

    finally:

        cur.close()
        conn.close()


'''def verify_payment(
        order_id,
        transaction_id,
        gateway_name,
        payment_success
):
    """
    Called after payment gateway callback
    """

    conn = admin_test()
    cur = conn.cursor()

    try:

        if payment_success:

            status = "SUCCESS"

        else:

            status = "FAILED"

        cur.execute(
            """
            UPDATE payments
            SET
                payment_status=%s,
                transaction_id=%s,
                payment_gateway=%s
            WHERE order_id=%s
            RETURNING user_id, plan_name
            """,
            (
                status,
                transaction_id,
                gateway_name,
                order_id
            )
        )

        result = cur.fetchone()

        if result and status == "SUCCESS":

            cur.execute(
                """
                UPDATE users
                SET subscription=%s
                WHERE id=%s
                """,
                (
                    result["plan_name"],
                    result["user_id"]
                )
            )

        conn.commit()

        return {
            "order_id": order_id,
            "payment_status": status
        }

    finally:

        cur.close()
        conn.close()'''
def verify_payment(
        order_id,
        transaction_id,
        gateway_name,
        payment_success
):

    conn = get_db1()
    cur = conn.cursor()

    try:

        status = "SUCCESS" if payment_success else "FAILED"

        # Get payment details first
        cur.execute(
            """
            SELECT
                id,
                user_id,
                plan_name,
                duration_type
            FROM payments
            WHERE order_id=%s
            """,
            (order_id,)
        )

        payment = cur.fetchone()

        if not payment:
            raise Exception("Payment not found")

        payment_id = payment["id"]
        user_id = payment["user_id"]
        new_plan = payment["plan_name"]
        duration_type = payment["duration_type"]

        # Decide expiry interval
        if duration_type == "YEARLY":
            expiry_interval = "1 year"
        else:
            expiry_interval = "1 month"

        # Update payment record
        if payment_success:

            cur.execute(
                f"""
                UPDATE payments
                SET
                    payment_status=%s,
                    transaction_id=%s,
                    payment_gateway=%s,
                    expiry_date=NOW() + interval '{expiry_interval}'
                WHERE order_id=%s
                """,
                (
                    status,
                    transaction_id,
                    gateway_name,
                    order_id
                )
            )

        else:

            cur.execute(
                """
                UPDATE payments
                SET
                    payment_status=%s,
                    transaction_id=%s,
                    payment_gateway=%s
                WHERE order_id=%s
                """,
                (
                    status,
                    transaction_id,
                    gateway_name,
                    order_id
                )
            )

        # Update subscription only if payment succecded
        if payment_success:

            # Get old subscription
            cur.execute(
                """
                SELECT subscription_type
                FROM users
                WHERE id=%s
                """,
                (user_id,)
            )

            user_data = cur.fetchone()

            old_plan = (
                user_data["subscription_type"]
                if user_data else "FREE"
            )

            # Update user subscription
            if duration_type == "YEARLY":

                cur.execute(
                    """
                    UPDATE users
                    SET
                        subscription_type=%s,
                        subscription_expiry=NOW() + interval '1 year'
                    WHERE id=%s
                    """,
                    (
                        new_plan,
                        user_id
                    )
                )

            else:

                cur.execute(
                    """
                    UPDATE users
                    SET
                        subscription_type=%s,
                        subscription_expiry=NOW() + interval '1 month'
                    WHERE id=%s
                    """,
                    (
                        new_plan,
                        user_id
                    )
                )

            # Insert subscription history
            cur.execute(
                f"""
                INSERT INTO subscription_history
                (
                    user_id,
                    old_plan,
                    new_plan,
                    payment_id,
                    start_date,
                    expiry_date
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    NOW(),
                    NOW() + interval '{expiry_interval}'
                )
                """,
                (
                    user_id,
                    old_plan,
                    new_plan,
                    payment_id
                )
            )

        conn.commit()

        return {
            "success": True,
            "order_id": order_id,
            "payment_status": status
        }

    finally:

        cur.close()
        conn.close()
def get_payment_status(order_id):

    #conn = admin_test()
    conn=get_db1()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            SELECT
                id,
                order_id,
                amount,
                plan_name,
                duration_type,
                payment_status,
                transaction_id,
                payment_gateway,
                expiry_date,
                created_at
            FROM payments
            WHERE order_id=%s
            """,
            (order_id,)
        )

        result = cur.fetchone()

        return result

    finally:

        cur.close()
        conn.close()


def get_payment_history(user_id):

    #conn = admin_test()
    conn=get_db1()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            SELECT
                order_id,
                email,
                full_name,
                plan_name,
                duration_type,
                amount,
                payment_status,
                transaction_id,
                payment_gateway,
                expiry_date,
                created_at
            FROM payments
            WHERE user_id=%s
            ORDER BY created_at DESC
            """,
            (user_id,)
        )

        payments = cur.fetchall()

        return payments

    finally:

        cur.close()
        conn.close()