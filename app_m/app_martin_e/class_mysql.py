import aiomysql

class Database:
    def __init__(self, host, user, password, database):
        self.config = {'host':host,
                       'user':user,
                       'password':password,
                       'db':database,
                     }
    
    async def execute(self, query):
        async with aiomysql.connect(**self.config) as conn:
        # Crear un cursor asincrónico
            async with conn.cursor() as cursor:
                
                await cursor.execute(query)
                await conn.commit()
                resultados = await cursor.fetchall()
                
                return resultados
  



        
        