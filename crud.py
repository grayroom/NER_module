from database import Databases


class CRUD(Databases):
    def update_db(self, table, colum, value, targ, condition):
        sql = "UPDATE {table} SET {colum}='{value}' WHERE \
                {targ}='{condition}' ".format(table=table,
                                              colum=colum,
                                              value=value,
                                              targ=targ,
                                              condition=condition)
        try:
            self.cursor.execute(sql)
            self.commit()
        except Exception as e:
            print(" update DB err", e)
