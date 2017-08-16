

建立等效性连接:
    http://blog.csdn.net/dingqingsong/article/details/46894487 
    http://blog.chinaunix.net/uid-20329764-id-5086457.html
    http://www.cnblogs.com/yjmyzz/p/4481720.html
    
    想通过A机器(root用户) 访问 B机器(comodo@172.0.1.140)
    1.  A上执行: 
            ssh-keygen -t rsa -P '' 
            其中, -t表示key的类型，rsa表示key类型 -P表示密码，-P '' 就表示空密码，
            也可以不用-P参数，这样就要三车回车，用-P就一次回车。
            运行完之后在/home/root/.ssh目录下生成私钥id_rsa和公钥id_rsa.pub

    2.  将 A主机下的公钥 id_rsa.pub 复制到PC_B机下
        scp /home/root/.ssh/id_rsa.pub comodo@172.0.1.140:/xxxxx/id_rsa.pub

    3.  将PC_B主机上的公钥添加到/home/comodo/.ssh/authorzied_keys之中
        cat /xxxxxx/id_rsa.pub >>/home/comodo/.ssh/authorized_keys

    4.  最重要的修改B主机相应目录的权限:
        chmod 700 /home/comodo
        chmod 700 /hoem/comodo/.ssh
        chmod 600 /home/comodo/.ssh/authorized_keys

    3和4步骤 可以在A主机上 使用命令来建立:
        ssh-copy-id -i /home/root/.ssh/id_rsa.pub  comodo@172.0.1.140 


连接: 
    ssh -p 6022 yanfa@10.10.10.19


执行命令:
    ssh -p 6022 yanfa@10.10.10.19  "ls -1 > tmp.txt; scp tmp.txt root@10.10.10.151:/home/"



