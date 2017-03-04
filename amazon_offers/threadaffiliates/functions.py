from config import THREADAFFILIATES_FB_DETAILS
import helpers
import pymysql


def get_db_connection():
    db = pymysql.connect(THREADAFFILIATES_FB_DETAILS["host"],
                         THREADAFFILIATES_FB_DETAILS["user"],
                         THREADAFFILIATES_FB_DETAILS["pass"],
                         THREADAFFILIATES_FB_DETAILS["name"])
    return db


def execute_query(sql, db=get_db_connection()):
    cursor = db.cursor()
    cursor.execute(sql)
    results = helpers.dictfetchall(cursor)
    cursor.close()
    return results


def get_post_message_list():
    message_list = [
        "Threadcrafts Store. Products exclusively handpicked for you.",
        "Exclusive range of products available only at Threadcrafts Store",
        "Amazing offers only on Threadcrafts Store",
        "Grab 'em before they are gone. Visit now.",
    ]
    return message_list


def fetch_products(limit="0,5"):
    sql = "SELECT * FROM products WHERE product_status = 1 ORDER BY rand() LIMIT " + str(
        limit)
    data = execute_query(sql)
    output_list = list()
    if len(data) > 0:
        for tmpdata in data:
            post_data_dict = {
                "name": tmpdata["product_title"].encode("utf-8"),
                "description": "Starts at Rs. " + str(
                    int(tmpdata["product_price_min"])),
                "picture": tmpdata["product_image_url"],
                "link": tmpdata["product_url_short"],
            }
            output_list.append(post_data_dict)
    return output_list
