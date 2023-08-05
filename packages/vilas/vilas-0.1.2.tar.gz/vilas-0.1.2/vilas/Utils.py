import os
import os.path
from subprocess import check_output
from subprocess import call
import distutils.spawn

class PdbFile(object):
    def __init__(self, file_path = '', chains = []):
        self.file_path = file_path
        self.chains = chains
   	pass

class Chain(object):
    def __init__(self, chain_id = 0, chain_type = '', chain_name = '', chain_view = '', is_selected = True, resindices = '', is_group = True):
        self.chain_id = chain_id
        self.chain_type = chain_type
        self.chain_name = chain_name
        self.chain_view = chain_view #Information about this chain in prody format
        self.is_selected = is_selected
        self.resindices = resindices
        self.is_group = is_group  #If this chain is a part of receptor group for pulling
    pass

class DataController(object):
    main_path = os.path.dirname(__file__)

    username = check_output('echo $USER',shell=True).split('\n')[0]
    root_path = '/home/'+username

    def __init__(self, *args, **kwargs):
        super(DataController, self).__init__(*args, **kwargs)
        setting_path = self.root_path + '/.vilas_setting.txt'
        if os.path.isfile(setting_path) == True:
            if self.getdata('config_auto ') == 'True':
                self.root_path = self.main_path + '/data'
        pass

    def getdata(self, name):
        f = open(self.root_path+'/.vilas_setting.txt', "r")
        contents = f.readlines()
        f.close()
        if len(self.substring(name,contents)) > 0:
            content = contents[self.substring(name,contents)[0]].split(' = ')[1].split('\n')[0]
            if content.replace(' ','') == '':
                if(name == 'path ' or name == 'path'):
                    return '/home/'+self.username + '/Documents/vilas-result';
            return content
        else: 
            self.initdata(name, '')
            return ''

    def setdata(self, name, value):
        if(name == 'config_auto ' or name == 'config_auto'):
            self.root_path = '/home/'+self.username

        print name + ' ' + value
        f = open(self.root_path+'/.vilas_setting.txt', "r")
        contents = f.readlines()
        f.close()

        if len(self.substring(name,contents)) > 0:
            print self.root_path+'/.vilas_setting.txt'
            contents[self.substring(name,contents)[0]] = name + ' = ' + value + '\n'
            f = open(self.root_path+'/.vilas_setting.txt', "w")
            contents = "".join(contents)
            f.write(contents)
            f.close()
        else:
            self.initdata(name, value)
        

    def initdata(self, name, value):
        f = open(self.root_path+'/.vilas_setting.txt', "r")
        contents = f.readlines()
        f.close()

        # If exist
        if len(self.substring(name,contents)) > 0:
            return

        contents.append(name + ' = ' + value + '\n')

        f = open(self.root_path+'/.vilas_setting.txt', "w")
        contents = "".join(contents)
        f.write(contents)
        f.close()

    def substring(self, mystr, mylist): 
        return [i for i, val in enumerate(mylist) if mystr in val]

    def checkExist(self):
        #Check root path
        setting_path = '/home/'+self.username + '/.vilas_setting.txt'
        if os.path.isfile(setting_path) == False:
            call('cp '+self.main_path+'/data/.vilas_setting.txt '+setting_path, shell=True)
            run_path = '/home/'+self.username + '/Documents/vilas-result'
            self.setdata('path ', run_path)

    # def checkAntechamber(self):
    #     # Check antechamber
    #     check_antechamber = distutils.spawn.find_executable('antechamber') is not None 
    #     if check_antechamber == False and self.searchLine('/home/'+self.username+'/.bashrc', 'AMBERHOME') == '':
    #         self.addLine('/home/'+self.username+'/.bashrc', '\n')
    #         self.addLine('/home/'+self.username+'/.bashrc', 'export AMBERHOME='+self.main_path+'\n')
    #         self.addLine('/home/'+self.username+'/.bashrc', 'export PATH=$AMBERHOME/bin:$PATH\n')
    #         self.addLine('/home/'+self.username+'/.bashrc', '\n')
    #         call('source /home/'+self.username+'/.bashrc', shell = True)

    # def addLine(self, myfile, line):
    #     with open(myfile, "a") as mf:
    #         mf.write(line)

    # def searchLine(self, myfile, search):
    #     f = open(myfile, "r")
    #     contents = f.readlines()
    #     f.close()
    #     if len(self.substring(search,contents)) > 0:
    #       return contents[self.substring(search,contents)[0]]
    #     else:
    #       return ''
                
class CheckPoint(object):
    point = ''
    step = ''
