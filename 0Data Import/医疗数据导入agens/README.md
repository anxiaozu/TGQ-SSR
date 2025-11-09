## 依赖要求
```
python3.6+ psycopg
```
## 前提条件
1. 数据库可以远程连接
2. 需要导入的数据（预处理完成的CSV文件）存放到了与数据库相同的服务器，且启动数据库的用户有权限访问这些文件
## 修改参数
1. 数据库的连接信息
2. CSV文件存放的目录
3. 日志输出文件
![Alt text](img/1716521269589.jpg)


create user liuyang password 'ZAQ1234@esz';
ALTER USER liuyang WITH SUPERUSER;
## 执行命令
```
python -u load_opengauss_age.py
```
* 导入sf0.1
```
python -u load_opengauss_age.py -u omm -p ZAQ1234@esz -H 127.0.0.1 -P 5432  -d postgres -D /home/liuyang/sf01/ -ldbc sf0_1
python -u load_agens_finbench.py -u omm -p ZAQ1234@esz -H 127.0.0.1 -P 5432  -d postgres -D /home/liuyang/openGauss_AGE/sf0.01/snapshot/ -ldbc sf0_1

python -u load_agens_yiliao.py -u omm -p ZAQ1234@esz -H 127.0.0.1 -P 5432  -d postgres -D /home/work/liuytest/大论文/0数据导入/医疗数据导入agens/import/ -ldbc sf0_1
```
* 导入sf1
```
python -u load_opengauss_age.py -u liuyang -p ZAQ1234@esz -H 10.8.8.151 -P 7432  -d postgres -D /home/age/agensldbcdata -ldbc sf1
```
* 导入sf10
```
python -u load_opengauss_age.py -u omm -p ZAQ1234@esz -H 10.8.8.151 -P 5432  -d postgres -D /home/liuyang/agetest/ldbcopgdata/sf10/ -ldbc sf10
```
## 导入校验
```
load 'age';
set search_path = ag_catalog;
select * from cypher('ldbc',$$match (n) return count(n)$$) as r(a agtype);
select * from cypher('ldbc',$$match (n)-[r]->(m) return count(*)$$) as r(a agtype);
```

* sf0.1 
![Alt text](img/1716457939456.jpg)
 