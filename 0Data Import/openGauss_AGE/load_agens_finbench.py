#!/usr/bin/env python3
import time
import psycopg
import concurrent.futures
import logging
import argparse

logger = None
'''
使用python 多个线程同时导入数据
docker run --name ogg --privileged=true -d -e GS_PASSWORD=ZAQ1234@esz -v /home/liuy/opengaussdata:/var/lib/opengauss/data  -v /home/liuy/openGauss-load/sf1/:/data/  -p5432:5432 liruxru/ogg:0.2.0-addloadx
pip3 install psycopg-binary -i https://pypi.tuna.tsinghua.edu.cn/simple
'''
class PostgresDbLoader():

    def __init__(self,database,endpoint,port,user,password,datadir):
        self.database = database
        self.endpoint = endpoint
        self.port = port
        self.user = user
        self.password = password
        self.datadir = datadir
        print(self.datadir )
        logger.info(f"load param {database} {endpoint} {port} {user} {password} {datadir}")


    def vacuum(self):
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
            logger.info("Run vacuum")
            all = []
            with open("agesql/jinrong/analyse.sql", "r") as f:
                lines = f.readlines()
                for line in lines:
                    if line == '':
                        continue
                    future = executor.submit(self.execute_sql, line.replace('\n', ''))
                    all.append(future)
            concurrent.futures.wait(all)

    def create_schema(self):
        pg_con = psycopg.connect(
            dbname=self.database,
            host=self.endpoint,
            user=self.user,
            password=self.password,
            port=self.port)
     
        pg_con.autocommit=True
        cur = pg_con.cursor()

        logger.info("create graph")
        cur.execute(self.load_script("agesql/jinrong/schema.sql"))
        pg_con.close()
    def clear_dirty_data(self):
        pg_con = psycopg.connect(
            dbname=self.database,
            host=self.endpoint,
            user=self.user,
            password=self.password,
            port=self.port)
     
        pg_con.autocommit=True
        cur = pg_con.cursor()

        logger.info("clear_dirty_data")
        cur.execute(self.load_script("agesql/jinrong/clear_dirty_data.sql"))
        pg_con.close()        
    def create_index(self):
        # 创建线程池
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            # 提交任务
            logger.info("create index")
            all = []
            with open("agesql/jinrong/create_index.sql", "r") as f:
               lines = f.readlines()
               for line in lines:
                   if line == '':
                       continue
                   future = executor.submit(self.execute_sql, line.replace('\n', ''))
                   all.append(future)
            concurrent.futures.wait(all)  
    
    def load_node_edge(self):
        # 创建线程池
        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
            # 提交任务
            logger.info("load node")
            all = []
            with open("agesql/jinrong/load_node.sql", "r") as f:
               lines = f.readlines()
               for line in lines:
                   if line == '':
                       continue
                   future = executor.submit(self.execute_sql, line.replace('\n', ''))
                   all.append(future)
            logger.info("load edge")
            with open("agesql/jinrong/load_edge.sql", "r") as f:
               lines = f.readlines()
               for line in lines:
                   if line == '':
                       continue
                   future =executor.submit(self.execute_sql, line.replace('\n', ''))
                   all.append(future)
            concurrent.futures.wait(all)  


   
    def load_script(self, filename):
        with open(filename, "r") as f:
            return f.read()

    # 定义任务函数
    def execute_sql(self,sql):
        pg_con = psycopg.connect(
            dbname=self.database,
            host=self.endpoint,
            user=self.user,
            password=self.password,
            port=self.port)
     
        try:
            pg_con.autocommit=True
            # pg_con.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)    
            cur = pg_con.cursor()
            cur.execute("set graph_path = finbench")
            sql = sql.replace('/data/', self.datadir)
            cur.execute(sql)
            results = cur.fetchall()
            logger.info(f"执行sql:{sql}---result:{results}")
            pg_con.close()
        except Exception as err:
            pg_con.close()
            logger.info(f"执行sql:{sql}---err:{err}")
            
    def drop_graph(self):
        pg_con = psycopg.connect(
            dbname=self.database,
            host=self.endpoint,
            user=self.user,
            password=self.password,
            port=self.port)
     
        pg_con.autocommit=True
        cur = pg_con.cursor()
        try:
            cur.execute(self.load_script("agesql/jinrong/drop_graph.sql"))
        except Exception as err:
            logger.info(f"drop graph---err:{err},没事，一般不影响导入")
        pg_con.close()

    def main(self):
        logger.info(f'连接的数据库配置信息: {self.database},{self.endpoint},{self.user},{self.password},{self.port}')
        
        self.drop_graph()
        # 记录开始导入时间
        start = time.time()
        # 创建schema
        self.create_schema()
        logger.info(f"create in Postgres in {time.time()-start:.4f} seconds") 
           
        # 导入节点和边
        start = time.time()
        self.load_node_edge()
        logger.info(f"Loaded data in Postgres in {time.time()-start:.4f} seconds")  
          
        # 创建索引   注意 AGE 1.0.0 和openGauss-AGE 官方版本是不支持索引的
        start = time.time()
        self.create_index()
        logger.info(f"create index in Postgres in {time.time()-start:.4f} seconds")   
          
        # 清理
        start = time.time()
        self.vacuum()
        # 删除ldbc脏数据
        self.clear_dirty_data()
        logger.info(f"vacuum analyse Postgres in {time.time()-start:.4f} seconds")
'''
ldbc 生成的数据有脏数据  最好执行一下 DELETE  from ldbc.hasmoderator where end_id not in (select id from ldbc.person))
'''
def set_log(load_data_info):
    global logger
    logging.basicConfig(level=logging.INFO #设置日志输出格式
                        ,filename=f"load_opengauss_age_{load_data_info}.log" #log日志输出的文件位置和文件名
                        # ,filemode="w" #文件的写入格式，w为重新写入文件，默认是追加
                        ,encoding='utf-8'
                        ,format="%(asctime)s - %(name)s - %(levelname)-9s - %(filename)-8s : %(lineno)s line - %(message)s" #日志输出的格式
                        # -8表示占位符，让输出左对齐，输出长度都为8位
                        ,datefmt="%Y-%m-%d %H:%M:%S" #时间输出的格式
                        )
    logger = logging.getLogger()  # 不加名称设置root logger

    # 使用StreamHandler输出到屏幕
    ch = logging.StreamHandler()
    # 添加两个Handler
    logger.addHandler(ch)

## nohup python3 -u load.py > loadldbc100.log &        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()    
    parser.add_argument('-ldbc','--TEST_DATASET',  help="TEST_DATASET: 测试数据集 可选 [sf0_1,sf1,sf10]",      type=str,        required=True   )
    parser.add_argument('-d','--POSTGRES_DB',     help="POSTGRES_DB: 连接的数据库 如 gsql -d postgres",        type=str,          required=True    )
    parser.add_argument( '-H', '--POSTGRES_HOST',        help="POSTGRES_HOST: 数据库ip地址",        type=str,        default='10.8.8.151',       required=True    )    
    parser.add_argument('-P','--POSTGRES_PORT',        help="POSTGRES_PORT: 数据库端口地址",        type=int,        default='5432',        required=True    )
    parser.add_argument('-u','--POSTGRES_USER',        help="POSTGRES_USER: 数据库用户名",        type=str,        default='omm',        required=True    )          
    parser.add_argument('-p',     '--POSTGRES_PASSWORD',        help="POSTGRES_PASSWORD: 数据库密码",        type=str,        required=True    )  
    parser.add_argument('-D',   '--CSV_LDBC_DIR',        help="CSV_LDBC_DIR: 要导入的数据存放目录",        type=str,        required=True    )  

    args = parser.parse_args()
    query_dir = args.TEST_DATASET
    set_log(query_dir)
    
    PGLoader = PostgresDbLoader(args.POSTGRES_DB,args.POSTGRES_HOST,args.POSTGRES_PORT,args.POSTGRES_USER,args.POSTGRES_PASSWORD,args.CSV_LDBC_DIR)
    start = time.time()
    PGLoader.main()
    end = time.time()
    duration = end - start
    logger.info(f"Loaded total in Postgres in {duration:.4f} seconds")
