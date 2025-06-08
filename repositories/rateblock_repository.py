import psycopg2
from database.Database import DBConnector


class RateBlockRepository:
    def __init__(self):
        self.db_connector = DBConnector()

    def get_connection(self):
        return self.db_connector.get_connection()

    def get_rate_block(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM RATEBLOCK;")
        rateblock = cursor.fetchall()
        cursor.close()
        conn.close()
        return rateblock

    def insert_rate_block(self, is_minimum, min_con, max_con, rate, categ_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO RATEBLOCK (is_minimum, min_consumption, max_consumption, rate, categ_id)
            VALUES (%s, %s, %s, %s, %s);
        """, (is_minimum, min_con, max_con, rate, categ_id))
        conn.commit()
        cursor.close()
        conn.close()

    def get_rate_block_by_category(self, categ_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT block_id, is_minimum, min_consumption, max_consumption, rate, categ_id
            FROM RATEBLOCK
            WHERE categ_id = %s
            ORDER BY min_consumption;
        """, (categ_id,))
        blocks = cursor.fetchall()
        cursor.close()
        conn.close()
        return blocks

    def update_rate_block(self, block_id, is_minimum, min_con, max_con, rate):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE RATEBLOCK
            SET is_minimum = %s,
                min_consumption = %s,
                max_consumption = %s,
                rate = %s
            WHERE block_id = %s;
        """, (is_minimum, min_con, max_con, rate, block_id))
        conn.commit()
        cursor.close()
        conn.close()

    def delete_rate_block(self, block_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM RATEBLOCK WHERE block_id = %s;", (block_id,))
        conn.commit()
        cursor.close()
        conn.close()