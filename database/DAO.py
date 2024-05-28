from database.DB_connect import DBConnect
from model.retailers import Retailer


class DAO():
    @staticmethod
    def getNazioni():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct (gr.Country )
                    from go_retailers gr """
        cursor.execute(query)
        for row in cursor:
            result.append(row['Country'])
        cursor.close()
        conn.close()
        return sorted(result)

    @staticmethod
    def getarchi(anno,i):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select t1.Retailer_code as r1,t2.Retailer_code as r2, count(distinct t1.Product_number)as peso 
                    from (select gds.Retailer_code ,gds.Product_number 
		                    from go_daily_sales gds 
		                    where gds.Product_number in (select distinct  gds.Product_number 
										                    from go_daily_sales gds 
										                    where year(gds.`Date`)=%s) and gds.Retailer_code =%s) as t1,
	(select gds.Retailer_code ,gds.Product_number 
		from go_daily_sales gds 
		where gds.Product_number in (select distinct  gds.Product_number 
										from go_daily_sales gds 
										where year(gds.`Date`)=%s) and gds.Retailer_code in (select gr.Retailer_code
                from go_retailers gr 
                where gr.Country =%s )) as t2
where t1.Retailer_code != t2.Retailer_code and t1.Product_number=t2.Product_number
group by r1,r2 """

        cursor.execute(query,(anno,i.Retailer_code,anno,i.Country))
        for row in cursor:
            result.append((row['r1'], row['r2'], row['peso']))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getnodi(nazione):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                from go_retailers gr 
                where gr.Country =%s  """

        cursor.execute(query, (nazione,))

        for row in cursor:
            result.append(Retailer(**row))

        cursor.close()
        conn.close()
        return result