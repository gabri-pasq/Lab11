from database.DB_connect import DBConnect
from model.products import Prodotto


class DAO():
    @staticmethod
    def getcolor():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct gp.Product_color 
                    from go_sales.go_products gp"""

        cursor.execute(query)

        for row in cursor:
            result.append(row['Product_color'])

        cursor.close()
        conn.close()
        return sorted(result)

    @staticmethod
    def getarchi(anno, colore):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select t1.Product_number as p1,t2.Product_number as p2, count(distinct t1.Date) as peso
                    from (select *
                          from go_sales.go_daily_sales gds 
                          where gds.Product_number in (select gp.Product_number from go_sales.go_products gp where gp.Product_color =%s) and year(gds.`Date`)=%s)as t1,
                          (select *          
                          from go_sales.go_daily_sales gds 
                          where gds.Product_number in (select gp.Product_number from go_sales.go_products gp where gp.Product_color =%s) and year(gds.`Date`)=%s)as t2
                    where t1.Product_number!=t2.Product_number and t1.Retailer_code=t2.Retailer_code and t1.Date = t2.Date
                    group by p1,p2   """

        cursor.execute(query, (colore, anno, colore, anno,))
        for row in cursor:
            result.append((row['p1'], row['p2'], row['peso']))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getnodi(c):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * 
            from go_sales.go_products gp 
            where gp.Product_color =%s
            order by Product_number asc  """

        cursor.execute(query, (c,))

        for row in cursor:
            result.append(Prodotto(**row))

        cursor.close()
        conn.close()
        return result