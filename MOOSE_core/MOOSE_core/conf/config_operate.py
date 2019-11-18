from configparser import ConfigParser


def get_dbconfig_uri():
    dbconf = ConfigParser()
    dbconf.read("db.cfg")  # 获取配置信息
    '''
    host = dbconf.get('mysql_db', ' host')
    user = dbconf.get('mysql_db', 'user')
    passwd = dbconf.get('mysql_db', 'passwd')
    db = dbconf.get('mysql_db', ' database')
    port = dbconf.get('mysql_db', 'port')
    
    return r'mysql://'+user+':' + passwd+' @ ' + host + '/' + db+'?charset = utf8'
    '''
    return r'mysql://XXXXX:XXXXX@XXXXXXXXX/MOOSE?charset=utf8'
