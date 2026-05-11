from database.DB_connect import DBConnect
from model.fermata import Fermata
from model.connessione import Connessione

class DAO():

    @staticmethod
    def getAllFermate():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM fermata"
        cursor.execute(query)

        for row in cursor:
            result.append(Fermata(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def haconnessione(u : Fermata, v : Fermata):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * from fermata;
                 select * from connessione c where c.id_stazP = %s and c.id_stazA = %s"""
        cursor.execute(query, (u.id_fermata, v.id_fermata))
        #query che compara attirbuto di due oggetti stesso tipo
        for row in cursor:
            result.append(row)
        cursor.close()
        conn.close()
        return len(result) > 0 #return true if > 0

    @staticmethod
    def getvicini(u: Fermata):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * from fermata;
                    select * from connessione c where c.id_stazP = %s"""
        cursor.execute(query, (u.id_fermata,))
        # creo data classa apposita che gestisca l uscita di questa tabella
        for row in cursor:
            result.append(row)
        cursor.close()
        conn.close()
        return len(result) > 0  # return true if > 0

    @staticmethod
    def getAllEdges():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * from connessione c"""
        cursor.execute(query)
        #mi da tutte le 1500 connessioni direttamente
        for row in cursor:
            result.append(Connessione(**row))
        cursor.close()
        conn.close()
        return result  # return true if > 0ù

    @staticmethod
    def getAllEdgesVeloc():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select c.id_stazP , c.id_stazA , max(l.velocita) as v
            from connessione c, linea l
            where l.id_linea = c.id_linea 
            group by c.id_stazP , c.id_stazA 
            order by v asc"""
        cursor.execute(query)
        #mi da tutte le 1500 connessioni direttamente
        for row in cursor:
            result.append((row['id_stazP'], row['id_stazA'], row['v']))
        cursor.close()
        conn.close()
        return result  # return true if > 0

