import mysql.connector as mdb
import consts
import traceback


class DbWrapper():
    def __init__(self):
        self.open_connection()



    def open_connection(self):
        try:
            self.con = mdb.connect(user=consts.DB_USER, password=consts.DB_PASSWORD,
                                   host=consts.DB_HOSTNAME,
                                   database=consts.DB_NAME)
        except mdb.Error as err:
            if err.errno == mdb.errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == mdb.errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)


    def close_connection(self):
        self.con.close()


    def get_values_by_id(self, table_name, id_value):
        cursor = self.con.cursor()
        query = consts.SELECT_BY_ID.format(table_name,id_value)
        cursor.execute(query)
        tuples = cursor.fetchall()
        cursor.close()
        return tuples

    def get_values_by_field(self, table_name, field_name, field_value):
        '''
        convert field_value to a tuple
        :param table_name:
        :param field_name:str
        :param field_value:str
        :return: list of dict
        '''
        try:
            cursor = self.con.cursor()
            values_tup = (field_value,)
            query = consts.SELECT_BY_FIELD.format(table_name,field_name,'%s')
            cursor.execute(query,values_tup)
            columns = cursor.description
            result = [{columns[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
            cursor.close()
            return result
        except Exception as ex:
            print 'Error in selecting from db'
            print traceback.format_exc()

    def execute_generic_query(self, query):
        try:
            cursor = self.con.cursor()
            cursor.execute(query)
            columns = cursor.description
            result = [{columns[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
            cursor.close()
            return result
        except:
            print traceback.format_exc()

    def get_user_data_by_twitter_id(self,twitter_id):
        try:
            cursor = self.con.cursor()
            query = "select * from users where twitter_id = %s"
            twitter_id = (twitter_id,)
            cursor.execute(query, twitter_id)
            columns = cursor.description
            result = [{columns[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
            cursor.close()
            return result
        except:
            print traceback.format_exc()

    def get_num_of_rows(self, table_name):
        cursor = self.con.cursor()
        query = 'Select COUNT(*) from {0}'.format(table_name)
        cursor.execute(query)
        tuples = cursor.fetchall()
        cursor.close()
        return tuples

    def insert_to_table(self, table_name, fields,values):
        try:
            cursor = self.con.cursor()
            fileds_name = ''
            for field in fields:
                fileds_name+=field+','
            fileds_name = fileds_name[:-1]

            query = consts.INSERT_QUERY.format(table_name, fileds_name)
            values_tuple = tuple(values)
            query+='('
            for value in values:
                query+='%s,'

            query=query[:-1]
            query+=')'
            cursor.execute(query,values_tuple )
            self.con.commit()
            cursor.close()
        except:
            print 'problem in inserting to DB! ,qeury won\'t be executed, qeury:{0}'.format(query)
            print traceback.format_exc()


    def get_userid_screen_name_db(self):
        select_user_id = "select id,screen_name from users"
        outputs = self.execute_generic_query(select_user_id)
        return outputs

    def get_user_ids(self):
        select_user_id = "select id from users"
        outputs = self.execute_generic_query(select_user_id)
        return outputs

    def get_last_id_from_table(self, table_name):
        qeury = 'select max(id) from {0}'.format(table_name)
        outputs = self.execute_generic_query(qeury)
        return outputs

    def update_table(self, table_name, fields, values, condition_str):
        pass