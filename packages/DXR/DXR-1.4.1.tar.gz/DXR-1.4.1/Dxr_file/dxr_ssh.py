import pexpect
password_key = '.*assword.*'
# 获取列表下所有文件以及文件夹，并且获取这些文件的大小以及更新时间, 自动输入密码
def ssh_get_file_list(remote_path, ip, user_name, password):
    ssh = pexpect.spawn('ssh %s@%s ls -l %s' % (user_name, ip, remote_path))
    try:
        i = ssh.expect([password_key, pexpect.EOF, pexpect.TIMEOUT], timeout=60)
        if i == 0:
            ssh.sendline(password)
            ssh.expect(pexpect.EOF)
        file_list_str = ssh.before.decode('utf-8')
        if 'No such file or directory' in file_list_str:
            return None
        file_list = file_list_str.split('\r\n')
        file_list = file_list[1:-1]
        # 对列表进行处理成一个字典的列表，键分别为权限，文件个数，所有者，所属组，大小，更新时间，文件名
        file_list_dict = []
        for f in file_list:
            file_dict = {}
            f = f.split()
            if len(f) != 9:
                continue
            file_dict['permissions'] = f[0]
            file_dict['number'] = f[1]
            file_dict['owner'] = f[2]
            file_dict['group'] = f[3]
            file_dict['size'] = f[4]
            file_dict['time'] = f[5] + ' ' + f[6] + ' ' + f[7]
            file_dict['name'] = f[8]
            file_list_dict.append(file_dict)
        return file_list_dict
    except pexpect.EOF:
        print('EOF')
        ssh.close()
        return None
    except pexpect.TIMEOUT:
        print('TIMEOUT')
        ssh.close()
        return None
   
def ssh_download_file(remote_path, local_path, ip, user_name, password):
    cmd = 'scp %s@%s:%s %s' % (user_name, ip, remote_path, local_path)
    ssh = pexpect.spawn(cmd)
    # 不设置超时时间，因为下载文件的时间不确定
    try:
        i = ssh.expect([password_key, pexpect.EOF, pexpect.TIMEOUT])
        if i == 0:
            ssh.sendline(password)
            ssh.expect(pexpect.EOF)
        return True
    except pexpect.EOF:
        print('EOF')
        ssh.close()
        return False
    
def ssh_upload_file(local_path, remote_path, ip, user_name, password):
    cmd = 'scp %s %s@%s:%s' % (local_path, user_name, ip, remote_path)
    ssh = pexpect.spawn(cmd)
    # 不设置超时时间，因为下载文件的时间不确定
    try:
        i = ssh.expect([password_key, pexpect.EOF, pexpect.TIMEOUT])
        if i == 0:
            ssh.sendline(password)
            ssh.expect(pexpect.EOF)
        return True
    except pexpect.EOF:
        print('EOF')
        ssh.close()
        return False
    
def ssh_rename_file(old_path, new_path, ip, user_name, password):
    cmd = 'ssh %s@%s mv %s %s' % (user_name, ip, old_path, new_path)
    ssh = pexpect.spawn(cmd)
    try:
        i = ssh.expect([password_key, pexpect.EOF, pexpect.TIMEOUT], timeout=60)
        if i == 0:
            ssh.sendline(password)
            ssh.expect(pexpect.EOF)
        return True
    except pexpect.EOF:
        print('EOF')
        ssh.close()
        return False
    except pexpect.TIMEOUT:
        print('TIMEOUT')
        ssh.close()
        return False
    
def ssh_delete_file(path, ip, user_name, password):
    cmd = 'ssh %s@%s rm -rf %s' % (user_name, ip, path)
    ssh = pexpect.spawn(cmd)
    try:
        i = ssh.expect([password_key, pexpect.EOF, pexpect.TIMEOUT], timeout=60)
        if i == 0:
            ssh.sendline(password)
            ssh.expect(pexpect.EOF)
        return True
    except pexpect.EOF:
        print('EOF')
        ssh.close()
        return False
    except pexpect.TIMEOUT:
        print('TIMEOUT')
        ssh.close()
        return False
    
def ssh_create_file(path, ip, user_name, password):
    cmd = 'ssh %s@%s touch %s' % (user_name, ip, path)
    ssh = pexpect.spawn(cmd)
    try:
        i = ssh.expect([password_key, pexpect.EOF, pexpect.TIMEOUT], timeout=60)
        if i == 0:
            ssh.sendline(password)
            ssh.expect(pexpect.EOF)
        return True
    except pexpect.EOF:
        print('EOF')
        ssh.close()
        return False
    except pexpect.TIMEOUT:
        print('TIMEOUT')
        ssh.close()
        return False
    
def ssh_create_dir(path, ip, user_name, password):
    cmd = 'ssh %s@%s mkdir %s' % (user_name, ip, path)
    ssh = pexpect.spawn(cmd)
    try:
        i = ssh.expect([password_key, pexpect.EOF, pexpect.TIMEOUT], timeout=60)
        if i == 0:
            ssh.sendline(password)
            ssh.expect(pexpect.EOF)
        return True
    except pexpect.EOF:
        print('EOF')
        ssh.close()
        return False
    except pexpect.TIMEOUT:
        print('TIMEOUT')
        ssh.close()
        return False
    
def ssh_get_file_size(path, ip, user_name, password):
    cmd = 'ssh %s@%s du -sh %s' % (user_name, ip, path)
    ssh = pexpect.spawn(cmd)
    try:
        i = ssh.expect([password_key, pexpect.EOF, pexpect.TIMEOUT], timeout=60)
        if i == 0:
            ssh.sendline(password)
            ssh.expect(pexpect.EOF)
            file_size = ssh.before.decode('utf-8').split('\r\n')[1].split()[0]
            return file_size
        else:
            return None
    except pexpect.EOF:
        print('EOF')
        ssh.close()
        return None
    except pexpect.TIMEOUT:
        print('TIMEOUT')
        ssh.close()
        return None