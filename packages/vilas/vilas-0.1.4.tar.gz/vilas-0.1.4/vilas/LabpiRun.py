# from pylab import *

from numpy import *
from prody import *
from os import listdir
import glob
import os
import sys
import Avogadro
import os.path
from subprocess import check_output
from subprocess import call
import subprocess

# import source
from parsePdb import Variable
from Utils import PdbFile
from Utils import DataController
from GromacsMD import GromacsMD


AminoAcid = ["ALA", "ARG", "ASN", "ASP", "CYS", "GLU", "GLN", "GLY", "HIS", "ILE", "LEU", "LYS", "MET", "PHE", "PRO", "SER", "THR", "TRP", "TYR", "VAL", "SEC", "PYL", "ASX", "GLX", "XLE", "XAA"]
ChainNames = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','P','Q','R','S','T','U','V','Y','Z']
ForceField = 'amber99sb'
GroLeft  = ''
GroRight = ''
GroOption = ''
GroVersion = ''
AvogadroAuto = ''
run_caver = ''
run_icst = ''
run_mode = ''
repeat_times = '0'
Method = '1'
main_path = ''
root_path = ''
ReceptorChain = ''
LigandChain = ''

ReceptorNumAtom = 0
ReceptorResidues = []
ReceptorCenter = []
ReceptorFile = []
LigandFile = []



class GromacsRun(object):
  global root_path
  root_path = os.path.dirname(__file__)
  dataController = DataController()

  #**********************************************************************#
  #***************************** Prepare Fuction ************************#
  #**********************************************************************#

  def ParsePDBInput(self):
    #Init variable
    global ReceptorCenter, ReceptorFile, ReceptorNumAtom, ReceptorResidues
    Receptors = Variable.parsepdb.Receptors

    ResidueNumber = 0
    lastResidueId = 0
    listCenter = [0,0,0]

    #Init root path
    global main_path
    main_path = self.dataController.getdata('path ')
    call('rm ' + main_path +'/input/receptor/*', shell=True)

    #Parse PDB and save to variable
    print len(Receptors)
    for receptor in Receptors:
      filename = os.path.basename(receptor.file_path)
      filename = os.path.splitext(filename)[0]
      for chain in receptor.chains:
        if chain.is_selected == False:
          continue

        if chain.chain_type == 'protein':
          protein = chain.chain_view

          fileName = main_path + '/input/receptor/receptor_' + filename + "_" + str(protein)
          writePDB( fileName.replace(" ", ""), protein)

          #If receptor is in group for pulling
          if chain.is_group == True:
            # split to seperate domain
            domains = chain.resindices.split(',')
            resBegin = protein.getResnums()[0]
            receptor_string = ''
            for domain in domains:
              # Check -1--2 or 1-2
              if len(domain.split('-')) == 2:
                ResidueStart = int(domain.split('-')[0])
                RedidueEnd = int(domain.split('-')[1])
              elif len(domain.split('-')) == 3 and domain.split('-')[0] == '':
                ResidueStart = (-1)*int(domain.split('-')[1])
                RedidueEnd = int(domain.split('-')[2])
              elif len(domain.split('-')) == 3 and domain.split('-')[0] != '':
                ResidueStart = int(domain.split('-')[0])
                RedidueEnd = (-1)*int(domain.split('-')[2])
              else:
                ResidueStart = int(domain.split('-')[1])
                RedidueEnd = (-1)*int(domain.split('-')[3])

              # Calc center and total atoms of each domain
              for resId in range(ResidueStart,RedidueEnd+1):
                listCenter += calcCenter(protein[resId])
                ReceptorNumAtom += protein[resId].numAtoms()

              # string resi ex: 123-424,560-818
              receptor_string += ','+str(ResidueStart-resBegin + lastResidueId)+'-'+str(RedidueEnd - resBegin + lastResidueId)

              # Calc number of residue
              ResidueNumber += RedidueEnd - ResidueStart + 1

            #format ReceptorResidues
            ReceptorResidues.append(receptor_string[1:])
            ReceptorFile.append(fileName.replace(" ", ""))

            lastResidueId += protein.numResidues()

            # ResidueStart = int(chain.resindices[0])
            # RedidueEnd = int(chain.resindices[1])
            # for resId in range(ResidueStart,RedidueEnd+1):
            #   listCenter += calcCenter(protein[resId])

            # ReceptorNumAtom += protein.numAtoms()
            # ResidueNumber += RedidueEnd - ResidueStart + 1

            # #format ReceptorResidues
            # resBegin = protein.getResnums()[0]
            # ReceptorResidues.append(str(ResidueStart-resBegin + lastResidueId)+':'+str(RedidueEnd - resBegin + lastResidueId))

            # lastResidueId += protein.numResidues()
            # ReceptorFile.append(fileName.replace(" ", ""))

        else:
          ligand = chain.chain_view
          fileName = main_path + '/input/receptor/ligand_' +  filename + "_" + str(ligand.getResnames()[0])

          # change resnum
          ligand.setResnums(1)

          # save ligand to file pdb
          writePDB(fileName.replace(" ", ""), ligand)

    ReceptorCenter = listCenter/ResidueNumber




  #Check version of gromacs
  #Check_out to read, call to call :))
  #Chon version gromacs tuong ung
  def setupOptions(self):
    # Get version of gromacs
    global GroLeft, GroRight, GroVersion
    gromacs_version = self.dataController.getdata('gromacs_version ')
    print gromacs_version
    version_array = gromacs_version.split(' VERSION ')[1].split('.')

    if int(version_array[0]) == 5:
      if int(version_array[1]) > 0:
        GroLeft = gromacs_version.split(' VERSION ')[0]
        GroRight = ''
      else:
        mdrun_array = gromacs_version.split(' VERSION ')[0].split('mdrun')
        GroLeft = 'gmx '
        GroRight = mdrun_array[1]
      GroVersion = 5
    else:
      mdrun_array = gromacs_version.split(' VERSION ')[0].split('mdrun')
      GroLeft = mdrun_array[0]
      GroRight = mdrun_array[1]
      GroVersion = 4

    # Set number of core or gpu
    global GroOption
    number_cores = self.dataController.getdata('maximum_cores ')
    if int(number_cores) > 0:
      GroOption = ' -nt '+number_cores
    else:
      GroOption = ''
    check_gpu = check_output(gromacs_version.split(' VERSION ')[0]+" -version", shell=True, executable='/bin/bash').splitlines()
    if( [s for s in check_gpu if "GPU support:" in s][0].split(":")[1].replace(' ','') == 'enable'):
      GroOption += ' -gpu_id 0'

    # Caver tools
    global run_caver
    if self.dataController.getdata('caver ') == 'True':
      run_caver = 'y'
      call('tar xfz '+root_path+'/caver.tar.gz -C '+self.dataController.getdata('path '), shell=True)
    else:
      run_caver = 'n'

    # ICST tools
    global run_icst
    if self.dataController.getdata('icst ') == 'True':
      run_icst = 'y'
    else:
      run_icst = 'n'

    #Repeat times
    global repeat_times
    repeat_times = int(self.dataController.getdata('repeat_times '))

    #Run nohup
    global run_mode
    if self.dataController.getdata('mode ') == 'nohup':
      run_mode = 'nohup'
    elif self.dataController.getdata('mode ') == 'config':
      run_mode = 'config'
    else:
      run_mode = 'normal'

    #Check add hydro by hand or auto
    global AvogadroAuto
    if self.dataController.getdata('ligand_auto ') == 'True':
      AvogadroAuto = 'true'
    else:
      AvogadroAuto = 'false'

  #**********************************************************************#
  #************************* Ligand Fuction *****************************#
  #**********************************************************************#
  def AddHydrogen(self, ligandFile, ligandName):
    ligand = Avogadro.MoleculeFile.readMolecule(ligandFile)
    if AvogadroAuto == 'true':
      ligand.removeHydrogens()
      ligand.addHydrogens()
      Avogadro.MoleculeFile.writeMolecule(ligand, ligandFile)
    elif AvogadroAuto == 'false':
      call('avogadro ' + ligandFile, shell=True)

    #Change name of residue
    call('antechamber -fi pdb -fo pdb -i ' +ligandFile+' -o ' +ligandFile+ ' -rn '+ligandName, shell=True, executable='/bin/bash')


  def CountCharge(self, ligandFile):
    ligand = Avogadro.MoleculeFile.readMolecule(ligandFile)
    sumCharge = 0
    for atom in ligand.atoms:
      sumCharge += atom.partialCharge

    return int(round(sumCharge, 0))

  def SetParameter(self, ligandNamePDB, charge, patchOutput):
    #check how to add net charge auto or by hand
    if AvogadroAuto == 'true':
      call('cp '+root_path+'/source/acpype.py '+ patchOutput +'; cd '+ patchOutput+ '; python2.7 acpype.py -i '+ ligandNamePDB +' -n '+ str(charge) +'; rm acpype.py', shell=True, executable='/bin/bash');
    elif AvogadroAuto == 'false':
      sys.stdin = open('/dev/tty')
      print "Enter net charge: "
      charge = raw_input("Enter net charge: ")
      call('cp '+root_path+'/source/acpype.py '+ patchOutput +'; cd '+ patchOutput+ '; python2.7 acpype.py -i '+ ligandNamePDB +' -n '+ str(charge) +'; rm acpype.py', shell=True, executable='/bin/bash');
  #**********************************************************************#
  #*************************** Prepare File *****************************#
  #**********************************************************************#

  def PrepareLigand(self):
    call('mkdir '+main_path+'/input/ligand/', shell=True)
    call('rm '+main_path+'/input/ligand/*', shell=True)
    # call('rm '+main_path+'/run/connection.txt', shell=True)

    ligands = Variable.parsepdb.Ligands
    index = 0
    for ligand in ligands:
      index+=1
      #Check name of ligands
      filename = os.path.basename(ligand.file_path)
      filename = filename.split('.pdb')[0]

      #Change NAME of ligand from input to output
      ligand_name = os.path.basename(ligand.file_path)
      if os.path.isfile(main_path+'/run/connection.txt') is False:
        if(len(filename)>3 or filename[0].isdigit() == True):
          # ligand_name = ligand.chain_view.getResnames()[0]
          if len(ligand.chains) > 0:
            ligand_name = ligand.chains[0].chain_view.getResnames()[0]
          else:
            ligand_name = ("A%02d" % (index))+'.pdb'
          # connection between ligand before and after rename
          self.addLine(filename + '\t' + ligand_name +'\n', main_path+'/run/connection.txt')
      else:
        linesearch = self.searchLine(filename, main_path+'/run/connection.txt')
        if len(linesearch.split('\t')) > 1:
          ligand_name = linesearch.split('\t')[1].split('\n')[0]
        elif(len(filename)>3 or filename[0].isdigit() == True):
          # ligand_name = ligand.chain_view.getResnames()[0]
          if len(ligand.chains) > 0:
            ligand_name = ligand.chains[0].chain_view.getResnames()[0]
          else:
            ligand_name = ("A%02d" % (index))+'.pdb'
          # connection between ligand before and after rename
          self.addLine(filename + '\t' + ligand_name +'\n', main_path+'/run/connection.txt')

      # Merge chains to 1 pdb file
      first_ligand = True
      for i in range (0, len(ligand.chains)):
        if ligand.chains[i].is_selected == False:
          continue
        if first_ligand == True:
         ligand_view = ligand.chains[i].chain_view
         first_ligand = False
        else:
         ligand_view += ligand.chains[i].chain_view

      # change resnum
      if len(ligand.chains) > 0:
        if ligand.chains[0].chain_type == 'ligand':
          ligand_view.setResnums(1)

      writePDB(main_path+'/input/ligand/'+ ligand_name, ligand_view)

      # parse pdb file
      lg = parsePDB(main_path+'/input/ligand/'+ ligand_name)

      #Check if this pdb is protein => add 'protein_' before this to identify
      if (not lg.select('protein') is None) or (not lg.select('resname A U G T C') is None):
        self.CallCommand(main_path+'/input/ligand', 'mv '+ligand_name+' protein_'+ligand_name)
        continue

      #Add hydrogen to ligand
      self.AddHydrogen(main_path+'/input/ligand/'+ligand_name, ligand_name.split('.')[0])

      #Count charge of ligand
      charge = self.CountCharge(main_path+'/input/ligand/'+ligand_name)

      #Set parameter (ff) for ligand
      self.SetParameter(main_path+'/input/ligand/'+ligand_name, charge, main_path+'/input/ligand')

  def PrepareLigandReceptor(self):
    ligands = ''
    try:
      ligands = check_output('cd '+main_path+'/input/receptor; ls ligand_*.pdb', shell = True).splitlines()
    except subprocess.CalledProcessError as e:

      for x in range(0,len(ligands)):
        #Add hydrogen to ligand
        AddHydrogen(main_path+'/input/receptor/'+ligands[x], ligands[x].split('_')[1].split('.')[0])

        #Count charge of ligand
        charge = self.CountCharge(main_path+'/input/receptor/'+ligands[x])

        #Set parameter (ff) for ligand
        self.SetParameter(ligands[x], charge, main_path+'/input/receptor')

  def PrepareCluster(self):
    global ReceptorChain
    global LigandChain
    call('cp '+root_path+'/source/top_pull.py '+main_path+'/analyse', shell = True)
    ligands = check_output('cd '+main_path+'/input/ligand; ls *.pdb', shell = True).splitlines()

    #cp file vo run
    for x in range(0,len(ligands)):
      ligandName = ligands[x].split('.')[0]
      isProtein = False
      if 'protein_' in ligandName:
        isProtein = True
        ligandName = ligandName.split('_')[1]
        call('mkdir '+main_path+'/run/run_' + ligandName, shell = True)
        call('mkdir '+main_path+'/run/run_' + ligandName+'/mdp', shell = True)
        call('cp '+main_path+'/input/ligand/'+ligands[x]+' '+main_path+'/run/run_' + ligandName+'/'+ligandName+'.pdb', shell = True)
        call('cp -r '+root_path+'/config/* '+main_path+'/run/run_'+ligandName+'/mdp', shell = True)
      else:
        if os.path.isfile(main_path+'/input/ligand/'+ligandName+'.acpype/'+ligandName+'_GMX.gro') is False:
          break
        call('mkdir '+main_path+'/run/run_' + ligandName, shell = True)
        call('mkdir '+main_path+'/run/run_' + ligandName+'/mdp', shell = True)
        call('cp -r '+main_path+'/input/ligand/'+ligandName+'.acpype '+main_path+'/run/run_'+ligandName, shell = True)
        call('cp -r '+root_path+'/config/* '+main_path+'/run/run_'+ligandName+'/mdp', shell = True)
        call('cp '+main_path+'/run/run_'+ligandName+'/'+ligandName+'.acpype/'+ligandName+'.pdb '+main_path+'/run/run_'+ligandName+'/'+ligandName+'.pdb', shell = True)

      # call('cp '+root_path+'/source/antechamber '+main_path+'/run/run_'+ligandName, shell=True)
      call('cp '+root_path+'/source/mathplot.py '+main_path+'/run/run_' + ligandName, shell = True)
      call('cp '+root_path+'/LabpiAnalyzer.py '+main_path+'/run/run_' + ligandName, shell = True)
      call('cp '+root_path+'/source/parse_pull.py '+main_path+'/run/run_'+ligandName, shell=True)
      call('cp '+root_path+'/source/pullana.py '+main_path+'/run/run_'+ligandName, shell=True)
      # call('cp '+root_path+'/source/MmPbSaStat.py '+main_path+'/run/run_'+ligandName, shell=True)
      call('cp -r '+main_path+'/input/receptor/*.acpype '+main_path+'/run/run_'+ligandName, shell = True)

      #Luu tung chain vao array de cong dong lai
      chains = []
      totalResidue = 0
      numberReceptor = 0
      numberLigand = 0
      print ReceptorFile
      for numR in range(0, len(ReceptorFile)):
        chains.append(parsePDB(ReceptorFile[numR]+'.pdb'))
        # change chain name A, B, C
        if ReceptorChain != '':
          ReceptorChain += ' or '
        ReceptorChain += 'chain '+ChainNames[numR]
        chainName = []
        for z in range(0, chains[numR].numAtoms()):
          chainName.append(ChainNames[numR])
        chains[numR].setChids(chainName)
        #Find total residue to know where is starting of ligand (type protein)
        totalResidue += chains[numR].numResidues()
        # count numberReceptor
        numberReceptor += 1

      #If ligand is protein => add it to pdb file
      if isProtein == True:
        chains.append(parsePDB(main_path+'/input/ligand/'+ligands[x]))
        # change chain name A, B, C
        chainName = []
        LigandChain = ChainNames[numR+1]
        for z in range(0, chains[numR+1].numAtoms()):
          chainName.append(ChainNames[numR+1])
        chains[numR+1].setChids(chainName)

        # count number Ligand
        numberLigand += 1

        file = open(main_path+'/run/run_' + ligandName+ '/ligand_residues.txt', 'w')
        file.close
        self.addLine(str(totalResidue)+'-'+str(totalResidue-1 + chains[numR+1].numResidues()),main_path+'/run/run_' + ligandName+ '/ligand_residues.txt')
      else:
        call('rm '+main_path+'/run/run_' + ligandName + '/ligand_residues.txt', shell=True)

      #Check if /receptor has other protein or not
      try:
        proteins = check_output('cd '+main_path+'/input/receptor; ls protein*', shell = True).splitlines()
        for y in range(len(chains), len(proteins)+len(chains)):
          chains.append(parsePDB(main_path+'/input/receptor/'+proteins[y-len(chains)]))
          chainName = []
          for z in range(0, chains[y].numAtoms()):
            chainName.append(ChainNames[y])
          chains[y].setChids(chainName)
      except subprocess.CalledProcessError as e:
        print 'ok'

      #Cong don protein lai thanh 1 file
      sumProtein = chains[0]
      sumReceptor = chains[0]
      for y in range(1, len(chains)):
        sumProtein += chains[y]
        # pdb file includes only receptor
        if y < numberReceptor or y >= numberReceptor + numberLigand:
          sumReceptor += chains[y]

      call('rm '+main_path+'/run/run_'+ligandName+'/protein.pdb', shell=True)
      call('rm '+main_path+'/run/run_'+ligandName+'/system.pdb', shell=True)
      writePDB(main_path+'/run/run_'+ligandName+'/protein.pdb',sumProtein)
      writePDB(main_path+'/run/run_'+ligandName+'/receptor.pdb',sumReceptor)

  def EditMdpFile(self):
    runfolders = check_output('ls '+main_path+'/run/', shell = True).splitlines()
    for x in range(0,len(runfolders)):
      if not os.path.isdir(main_path+'/run/'+runfolders[x]):
        continue

      mdpFolder = main_path+'/run/'+runfolders[x]+'/mdp'

      nsteps = int(int(self.dataController.getdata('nvt-nsteps '))/0.002)
      nstout = self.dataController.getdata('nvt-nst ')
      self.replaceLine('nsteps', 'nsteps     = '+str(nsteps)+'\n', mdpFolder+'/nvt.mdp')
      self.replaceLine('nstxout', 'nstxout     = '+str(nstout)+'\n', mdpFolder+'/nvt.mdp')
      self.replaceLine('nstvout', 'nstvout     = '+str(nstout)+'\n', mdpFolder+'/nvt.mdp')
      self.replaceLine('nstenergy', 'nstenergy     = '+str(nstout)+'\n', mdpFolder+'/nvt.mdp')
      self.replaceLine('nstlog', 'nstlog     = '+str(nstout)+'\n', mdpFolder+'/nvt.mdp')

      nsteps = int(int(self.dataController.getdata('npt-nsteps '))/0.002)
      nstout = self.dataController.getdata('npt-nst ')
      self.replaceLine('nsteps', 'nsteps     = '+str(nsteps)+'\n', mdpFolder+'/npt.mdp')
      self.replaceLine('nstxout', 'nstxout     = '+str(nstout)+'\n', mdpFolder+'/npt.mdp')
      self.replaceLine('nstvout', 'nstvout     = '+str(nstout)+'\n', mdpFolder+'/npt.mdp')
      self.replaceLine('nstenergy', 'nstenergy     = '+str(nstout)+'\n', mdpFolder+'/npt.mdp')
      self.replaceLine('nstlog', 'nstlog     = '+str(nstout)+'\n', mdpFolder+'/npt.mdp')

      nsteps = int(int(self.dataController.getdata('md-nsteps '))/0.002)
      nstout = self.dataController.getdata('md-nst ')
      self.replaceLine('nsteps', 'nsteps     = '+str(nsteps)+'\n', mdpFolder+'/md.mdp')
      self.replaceLine('nstxout', 'nstxout     = '+str(nstout)+'\n', mdpFolder+'/md.mdp')
      self.replaceLine('nstvout', 'nstvout     = '+str(nstout)+'\n', mdpFolder+'/md.mdp')
      self.replaceLine('nstxtcout', 'nstxtcout     = '+str(nstout)+'\n', mdpFolder+'/md.mdp')
      self.replaceLine('nstenergy', 'nstenergy     = '+str(nstout)+'\n', mdpFolder+'/md.mdp')
      self.replaceLine('nstlog', 'nstlog     = '+str(nstout)+'\n', mdpFolder+'/md.mdp')

      nsteps = int(int(self.dataController.getdata('smd-nsteps '))/0.002)
      nstout = self.dataController.getdata('smd-nst ')
      vel_pull = self.dataController.getdata('smd-vel ')
      k_pull = self.dataController.getdata('smd-k ')
      if(GroVersion >= 5):
        mdp_pull_file = '/md_pull_5.mdp'
        self.replaceLine('pull-coord1-rate', 'pull-coord1-rate      = '+str(vel_pull)+'\n', mdpFolder+mdp_pull_file)
        self.replaceLine('pull-coord1-k', 'pull-coord1-k         = '+str(k_pull)+'\n', mdpFolder+mdp_pull_file)
      else:
        mdp_pull_file = '/md_pull.mdp'
        self.replaceLine('pull_rate1', 'pull_rate1      = '+str(vel_pull)+'\n', mdpFolder+mdp_pull_file)
        self.replaceLine('pull_k1', 'pull_k1         = '+str(k_pull)+'\n', mdpFolder+mdp_pull_file)

      self.replaceLine('nsteps', 'nsteps     = '+str(nsteps)+'\n', mdpFolder+mdp_pull_file)
      self.replaceLine('nstxout', 'nstxout     = '+str(nstout)+'\n', mdpFolder+mdp_pull_file)
      self.replaceLine('nstvout', 'nstvout     = '+str(nstout)+'\n', mdpFolder+mdp_pull_file)
      self.replaceLine('nstxtcout', 'nstxtcout     = '+str(nstout)+'\n', mdpFolder+mdp_pull_file)
      self.replaceLine('nstenergy', 'nstenergy     = '+str(nstout)+'\n', mdpFolder+mdp_pull_file)
      self.replaceLine('nstlog', 'nstlog     = '+str(nstout)+'\n', mdpFolder+mdp_pull_file)


  #**********************************************************************#
  #************************** System Fuction ****************************#
  #**********************************************************************#

  def CallCommand(self, patch, command):
    call('cd '+patch+'; '+command, shell = True, executable='/bin/bash')

  def substring(self, mystr, mylist):
    return [i for i, val in enumerate(mylist) if mystr in val]

  def replaceLine(self, search, replace, myfile):
    f = open(myfile, "r")
    contents = f.readlines()
    f.close()

    contents[self.substring(search,contents)[0]] = replace

    f = open(myfile, "w")
    contents = "".join(contents)
    f.write(contents)
    f.close()

  def insertLine(self, search, position, insert, myfile):
    f = open(myfile, "r")
    contents = f.readlines()
    f.close()

    if len(self.substring(search,contents)) > 0:
      contents.insert(self.substring(search,contents)[0]+position, insert)
      f = open(myfile, "w")
      contents = "".join(contents)
      f.write(contents)
      f.close()
    else:
      self.addLine(insert, myfile)

  def searchLine(self, search, myfile):
    f = open(myfile, "r")
    contents = f.readlines()
    f.close()
    if len(self.substring(search,contents)) > 0:
      return contents[self.substring(search,contents)[0]]
    else:
      return ''

  def addLine(self, line, myfile):
    with open(myfile, "a") as mf:
      mf.write(line)

  def Log(self, tag, comment):
    self.addLine(tag+ ' ' +comment+'\n', 'log.txt')


  #**********************************************************************#
  #************************* Calc Fuction ****************************#
  #**********************************************************************#
  def RepresentsInt(self, s):
      try:
          int(s)
          return True
      except ValueError:
          return False

  def setbox(self, patch, inputfile,outputfile, nRR, distance,ratio,ligandZ):
    print patch
    print inputfile
    print outputfile
    print nRR
    print distance
    print ratio
    print ligandZ
    #Read file
    system = Avogadro.MoleculeFile.readMolecule(patch+inputfile)

    #Find max and min falue System
    max = [-1000000.0,-1000000.0,-1000000.0]
    min = [1000000.0,1000000.0,1000000.0]
    proteinMax = -1000000
    systemCenter = [0,0,0]
    for x in range(0, system.numAtoms):
        atom = system.atom(x)
        pos_x = float(atom.pos[0])
        pos_y = float(atom.pos[1])
        pos_z = float(atom.pos[2])
        systemCenter += atom.pos

        if pos_x>max[0]:
          max[0] = pos_x
        if pos_x<min[0]:
          min[0] = pos_x

        if pos_y>max[1]:
          max[1] = pos_y
        if pos_y<min[1]:
          min[1] = pos_y

        if pos_z>max[2]:
          max[2] = pos_z
          if atom.residueId < nRR:
            proteinMax = pos_z
        if pos_z<min[2]:
          min[2] = pos_z

    #Change distance
    distance *= 1.5

    #Check distance between ligand and maxZ protein
    dz = float(ligandZ) + float(distance) - float(proteinMax/10)
    if float(dz) < 0.0:
      distance = '0'
    else:
      distance = str(dz)

    self.Log('distance',str(distance))
    self.Log('ligandZ',str(ligandZ))
    self.Log('proteinMax',str(proteinMax/10))

    #distance between protein and box
    Oxyz = [min[0]-10,min[1]-10,min[2]-10]
    d_x = (max[0]-min[0])/10 + 2
    d_y = (max[1]-min[1])/10 + 2
    d_z = (max[2]-min[2])/10 + 2 + float(distance)
    systemCenter /= system.numAtoms
    systemCenter = (systemCenter - Oxyz)/10
    systemCenter[2] += (1/(float(ratio)+1))*float(distance)

    self.Log('dz',str(d_z))
    self.Log('systemCenter', str(systemCenter[2]))
    self.Log('ratio',str(ratio))

    call('cd '+patch+';'+GroLeft+'editconf'+GroRight+' -f '+inputfile+' -o '+outputfile +' -box '+str(d_x)+' '+str(d_y)+' '+str(d_z)+ ' -center '+str(systemCenter[0])+' '+str(systemCenter[1])+' '+str(systemCenter[2]), shell=True, executable='/bin/bash')


  def ParseIndex(self, indexFile):
    f = open(indexFile, "r")
    contents = f.readlines()
    f.close()

    groups = []
    for i in range(0, len(contents)):
      line = contents[i]
      if line[0:2] == '[ ':
        print line
        j = 0
        for k in range(0, len(groups)):
          if groups[j] == line.split('\n')[0]:
            contents[i] = '[ new_'+ contents[i][2:]
            break
          j+=1
        print str(len(groups)) + ' ' + str(j)
        if j >= len(groups):
          groups.append(line.split('\n')[0])
    print groups

    f = open(indexFile, "w")
    contents = "".join(contents)
    f.write(contents)
    f.close()

  def IndexHaveRNA(self, indexFile):
    if self.searchLine('RNA', indexFile) == '':
      return False
    else:
      return True

  def IndexHaveDNA(self, indexFile):
    if self.searchLine('DNA', indexFile) == '':
      return False
    else:
      return True

  def getMaxCoord(self, axe, obj, vectorPull):
    max = -1000000
    posAtom = 0
    for x in range(0,len(obj.getCoords())):
      if max < obj.getCoords()[x][axe]:
        max = self.rotatePoint(obj.getCoords()[x], vectorPull)[axe]
        posAtom = x

    return self.rotatePoint(obj.getCoords()[posAtom], vectorPull)

  def setupCaver(self, ligandCenter, filepdb):
    call('rm -r '+main_path+'/caver/input/*', shell=True)
    call('cp '+str(filepdb).replace(' ','\ ')+' '+main_path+'/caver/input', shell=True)
    coord_ligand = str(ligandCenter[0]) + ' ' + str(ligandCenter[1]) + ' ' + str(ligandCenter[2]) + '\n'
    self.replaceLine('starting_point_coordinates','starting_point_coordinates '+coord_ligand,main_path+'/caver/config.txt')
    call('cd '+main_path+'/caver; sh caver.sh', shell=True)

    outputFile = []
    try:
      outputFile = check_output('cd '+main_path+'/caver/out/data/clusters; ls *.pdb', shell = True).splitlines()
    except subprocess.CalledProcessError as e:
      return None
    tunel = parsePDB(main_path+'/caver/out/data/clusters/'+outputFile[0])
    tunelVector = tunel.getCoords()[tunel.numAtoms()-1] - tunel.getCoords()[tunel.numAtoms()-2]
    return tunelVector


  #**********************************************************************#
  #************************* Rotation Fuction ****************************#
  #**********************************************************************#
  def rotatePoint(self, point, pullvec):
    pullr = math.sqrt(float(pullvec[0])**2 + float(pullvec[1])**2 + float(pullvec[2])**2)
    pullphi = self.angle(float(pullvec[0]), float(pullvec[1]))
    pullxy = math.sqrt(float(pullvec[0])**2 + float(pullvec[1])**2)
    pulltheta = self.angle(float(pullvec[2]), float(pullxy) )
    self.rotateZ(point, pullphi)
    self.rotateY(point, pulltheta)
    return point

  #Fuction
  def angle(self, x, y):
    if x == 0.0:
      if y > 0.0:
        alpha = math.pi/2
      else:
        alpha = -math.pi/2
    elif x > 0.0:
      alpha = math.atan(y/x)
    else:
      if y > 0.0:
        alpha = math.pi + math.atan(y/x)
      else:
        alpha = -math.pi + math.atan(y/x)
    return alpha

  def rotateZ(self, point, phi):
    point_r_xy = math.sqrt(point[0]**2 + point[1]**2)
    point_phi = self.angle(point[0], point[1])

    point[0] = point_r_xy*math.cos(point_phi - phi)
    point[1] = point_r_xy*math.sin(point_phi - phi)
    return point

  def rotateY(self, point, theta):
    point_r_xz = math.sqrt(point[0]**2 + point[2]**2)
    point_theta = self.angle(point[2], point[0])

    point[0] = point_r_xz*math.sin(point_theta - theta)
    point[2] = point_r_xz*math.cos(point_theta - theta)
    return point
  #***********************************************************************************#


  #**********************************************************************#
  #************************* Gromacs Fuction ****************************#
  #**********************************************************************#
  def SetupSystem(self):
    global GroLeft, GroRight
    runfolders = check_output('ls '+main_path+'/run/', shell = True).splitlines()
    for x in range(0,len(runfolders)):
      if not os.path.isdir(main_path+'/run/'+runfolders[x]):
        continue

      run_path = main_path+'/run/'+runfolders[x]
      topolfile = main_path+'/run/'+runfolders[x]+'/topol.top'
      ligandCurrent = runfolders[x].split('_')[1] #A01

      # Check if file solv_ions.gro is exist
      # if os.path.isfile(run_path+'/solv_ions.gro') is True:
      #   continue

      try:
        ligandFolders = check_output('cd '+run_path+'; ls -d *.acpype', shell = True).splitlines()
      except subprocess.CalledProcessError as e:
        ligandFolders = []
      proteinfiles = check_output('cd '+run_path+'; ls protein*', shell = True).splitlines()

      #*****************************************************************************************************#
      #Add force field to protein
      #for y in range(0, len(proteinfiles)):
      #proteinname = proteinfiles[0].split(".")[0]
      self.CallCommand(run_path,GroLeft+'pdb2gmx'+GroRight+' -ff '+ForceField+' -f protein.pdb -o protein.gro -water spce -missing -ignh')

      #if ligand is protein
      # if os.path.isfile('run/'+runfolders[x]+'/'+ligandCurrent+'.pdb') is True:
      #   self.CallCommand('run/'+runfolders[x],GroLeft+'pdb2gmx'+GroRight+' -ff '+ForceField+' -f '+ligandCurrent+'.pdb -o '+ligandCurrent+'.gro -water spce')

      #*****************************************************************************************************#
      #Merge *.gro file
      #Read file protein.gro
      proteingro = open(run_path+'/protein.gro', 'r')
      proteinData = proteingro.readlines()
      proteingro.close()

      is_error = False
      for y in range(0, len(ligandFolders)):

        #Read file *.gro
        ligandName = ligandFolders[y].split('.')[0]
        if os.path.isfile(run_path+'/'+ligandFolders[y]+'/'+ligandName+'_GMX.gro') is True:
          gro = open(run_path+'/'+ligandFolders[y]+'/'+ligandName+'_GMX.gro', 'r')
        else:
          self.addLine(ligandName + ': paremeter of ligand is error or missing - hint: please sets it again by hand mode\n', main_path+'/run/log_error.txt')
          is_error = True
          continue

        ligandData = gro.readlines()
        gro.close()

        #Change number of atoms and add atoms to bottom of protein.gro
        proteinData[1] = str(int(proteinData[1]) + int(ligandData[1])) + '\n'
        for line in ligandData[2:len(ligandData)-1]:
          proteinData.insert(len(proteinData)-1, line)

      if is_error == True:
        continue

      #save to system.gro
      f = open(run_path+'/system.gro', "w")
      for item in proteinData:
        f.write(item)
      f.close()

      #*****************************************************************************************************#
      #Add atomtype and
      atomtypes = []
      for y in range(0, len(ligandFolders)):
        #Read file *.itp
        ligandName = ligandFolders[y].split('.')[0]
        itp = open(run_path+'/'+ligandFolders[y]+'/'+ligandName+'_GMX.itp', 'r')
        itpline = itp.readlines()
        atomtypes.extend( itpline[self.substring('[ atomtypes ]',itpline)[0]: self.substring('[ moleculetype ]',itpline)[0]] )

        #save other part to ligand_topology.itp
        atomtopologys = []
        atomtopologys = itpline[self.substring('[ moleculetype ]',itpline)[0]:]
        itp.close()

        f = open(run_path+'/'+ligandName+'.itp', "w")
        for item in atomtopologys:
          f.write(item)
        f.close()

        #add ligand_topology.itp to topol.top
        if y == 0: self.insertLine('; Include water topology', -1, '\n; Include ligand topology \n', topolfile)
        self.insertLine('; Include water topology', -1, '#include "'+ligandName+'.itp" \n', topolfile)

        #add molecular to bottom of topol.top
        self.addLine(ligandName+'                 1\n', topolfile)

      #save atomtypes to ligand_atomtypes.itp
      f = open(run_path+'/ligand_atomtypes.itp', "w")
      for item in atomtypes:
        f.write(item)
      f.close()

      #add ligand_atomtypes.itp to topol.top
      self.insertLine('; Include forcefield parameters', 2, '#include "ligand_atomtypes.itp" \n', topolfile)

      #*********************************************************************************
      #init analyzer
      cmd_analyse = 'python2.7 LabpiAnalyzer.py --pro '+run_path+'/protein.pdb --mdp '+run_path+'/mdp/md.mdp --rechain \'' +ReceptorChain+ '\' --root '+root_path+' --run '+run_path+ ' --ligand '+ligandCurrent
      if LigandChain != '':
        cmd_analyse += ' --lichain \'' + LigandChain +'\''
      if GroLeft.replace(' ','') != '':
        cmd_analyse += ' --gleft '+GroLeft
      if GroRight.replace(' ','') != '':
        cmd_analyse += ' --gright '+GroRight
      self.CallCommand(run_path, cmd_analyse +' -i True')
      print "check point analyzer"

      #*****************************************************************************************************#
      #setup Box
      if os.path.isfile(run_path+'/'+ligandCurrent+'.acpype/'+ligandCurrent+'.pdb') is True:
        ligand = parsePDB(run_path+'/'+ligandCurrent+'.acpype/'+ligandCurrent+'.pdb')
      elif os.path.isfile(run_path+'/'+ligandCurrent+'.pdb') is True:
        ligand = parsePDB(run_path+'/'+ligandCurrent+'.pdb')
      else:
        continue
      ligandCenter = calcCenter(ligand)

      #Check the vector for pulling
      vectorPull = []
      if run_caver == 'y':
        vectorPull = self.setupCaver(ligandCenter, run_path+'/protein.pdb')
        if vectorPull is None:
          vectorPull = ligandCenter - ReceptorCenter
      elif run_icst == 'y':
        if os.path.isfile(run_path+'/pull_direction.pdb') is False:
          print 'Detect pulling vector ...'
          call('cp '+root_path+'/source/icst '+run_path, shell=True)
          self.CallCommand(run_path, './icst -r receptor.pdb -l '+ligandCurrent+'.pdb -keep')
        pull_direction = parsePDB(run_path+'/pull_direction.pdb')
        vectorPull = pull_direction.getCoords()[1] - pull_direction.getCoords()[0]
      else:
        vectorPull = ligandCenter - ReceptorCenter

      # self.Log('ligandCenter',str(ligandCenter))
      # self.Log('ReceptorCenter',str(ReceptorCenter))

      call('cp '+root_path+'/source/rotate.py '+run_path+'/', shell = True)
      self.CallCommand(run_path+'/', 'python2.7 rotate.py -i system.gro -o rotate_system.gro -v '+str(vectorPull[0])+','+str(vectorPull[1])+','+str(vectorPull[2]))

      #*****************************************************************************************************#
      #set Boxsize
      #read distance
      pullspeed = float(self.searchLine('pull_rate1', run_path+'/mdp/md_pull.mdp').split("=")[1].split(';')[0])
      pulltime = float(self.searchLine('nsteps', run_path+'/mdp/md_pull.mdp').split("=")[1].split(';')[0])*float(self.searchLine('dt', main_path+'/run/'+runfolders[x]+'/mdp/md_pull.mdp').split("=")[1].split(';')[0])
      distance = pullspeed*pulltime

      #Calc ratio of receptor/ligand
      if os.path.isfile(run_path+'/'+ligandCurrent+'.acpype/'+ligandCurrent+'.pdb') is True:
        ligand = parsePDB(run_path+'/'+ligandCurrent+'.acpype/'+ligandCurrent+'.pdb')
      else:
        ligand = parsePDB(run_path+'/'+ligandCurrent+'.pdb')
      ligandNumAtom = ligand.numAtoms()

      self.Log('number atom', str(ReceptorNumAtom) + ' ' + str(ligandNumAtom))
      ratio = float(float(ReceptorNumAtom)/float(ligandNumAtom))
      ligandMax = self.getMaxCoord(2, ligand, vectorPull)
      receptor = Avogadro.MoleculeFile.readMolecule(run_path+'/protein.gro')
      self.setbox(run_path+'/', 'rotate_system.gro', 'newbox.gro', receptor.numResidues, distance, ratio, ligandMax[2]/10)


      #*******************************************************************************
      #Add solv
      # if os.path.isfile(run_path+'/solv.gro') is False:
      if GroVersion >=5:
        self.CallCommand(run_path, GroLeft+'solvate'+GroRight+' -cp newbox.gro -cs spc216.gro -p topol.top -o solv.gro')
      else:
        self.CallCommand(run_path, GroLeft+'genbox'+GroRight+' -cp newbox.gro -cs spc216.gro -p topol.top -o solv.gro')

      #Add ions to solv
      #self.CallCommand('run/'+runfolders[x], 'cp solv.gro solv_ions.gro')
      # if os.path.isfile(run_path+'/solv_ions.gro') is False:
      self.CallCommand(run_path, GroLeft+'grompp'+GroRight+' -maxwarn 10 -f mdp/ions.mdp -c solv.gro -p topol.top -o ions.tpr')
      self.CallCommand(run_path, 'echo -e \"SOL\"|' +GroLeft+'genion'+GroRight+' -s ions.tpr -o solv_ions.gro -p topol.top -pname NA -nname CL -neutral -conc 0.1')

      #Create index file for first time => check double name
      self.CallCommand(run_path, 'echo -e \"q\\n\" | '+ GroLeft+'make_ndx'+GroRight+' -f solv_ions.gro -o index.ndx')
      self.ParseIndex(run_path+'/index.ndx')

      #*****************************************************************************************************#
      #Chang file mdp
      try:
        ligandFolders = check_output('cd '+run_path+'; ls -d *.acpype', shell = True).splitlines()
      except subprocess.CalledProcessError as e:
        ligandFolders = []

      replace_1 = 'energygrps      = Protein'
      replace_2 = 'tc-grps         = Protein'
      replace_3 = 'tau_t           = 0.1 0.1'
      replace_4 = 'ref_t           = 300 300'
      for y in range(0, len(ligandFolders)):
        #Lay resname cua ligand, ex: FAD, A01
        ligandName = ligandFolders[y].split('.')[0]
        ligand = Avogadro.MoleculeFile.readMolecule(run_path+'/'+ligandFolders[y]+'/'+ligandName+'.pdb')
        resname = ligand.residues[0].name
        replace_1 += ' '+resname
        replace_2 += '_'+resname

      #Check index have RNA or not
      if self.IndexHaveRNA(run_path+'/index.ndx') == True:
        replace_1 += ' RNA'
        replace_2 += ' RNA'
        replace_3 += ' 0.1'
        replace_4 += ' 300'
      elif self.IndexHaveDNA(run_path+'/index.ndx') == True:
        replace_1 += ' DNA'
        replace_2 += ' DNA'
        replace_3 += ' 0.1'
        replace_4 += ' 300'

      replace_1 += '\n'
      replace_2 += ' Water_and_ions\n'
      replace_3 += '\n'
      replace_4 += '\n'

      self.replaceLine('energygrps', replace_1, run_path+'/mdp/minim.mdp')
      self.replaceLine('energygrps', replace_1, run_path+'/mdp/nvt.mdp')
      self.replaceLine('energygrps', replace_1, run_path+'/mdp/npt.mdp')
      self.replaceLine('energygrps', replace_1, run_path+'/mdp/md.mdp')
      self.replaceLine('energygrps', replace_1, run_path+'/mdp/md_pull.mdp')
      self.replaceLine('energygrps', replace_1, run_path+'/mdp/md_pull_5.mdp')
      self.replaceLine('energygrps', replace_1, run_path+'/mdp/md_md.mdp')

      self.replaceLine('tc-grps', replace_2, run_path+'/mdp/nvt.mdp')
      self.replaceLine('tc-grps', replace_2, run_path+'/mdp/npt.mdp')
      self.replaceLine('tc-grps', replace_2, run_path+'/mdp/md.mdp')
      self.replaceLine('tc-grps', replace_2, run_path+'/mdp/md_pull.mdp')
      self.replaceLine('tc-grps', replace_2, run_path+'/mdp/md_pull_5.mdp')
      self.replaceLine('tc-grps', replace_2, run_path+'/mdp/md_md.mdp')

      self.replaceLine('tau_t', replace_3, run_path+'/mdp/nvt.mdp')
      self.replaceLine('tau_t', replace_3, run_path+'/mdp/npt.mdp')
      self.replaceLine('tau_t', replace_3, run_path+'/mdp/md.mdp')
      self.replaceLine('tau_t', replace_3, run_path+'/mdp/md_pull.mdp')
      self.replaceLine('tau_t', replace_3, run_path+'/mdp/md_pull_5.mdp')
      self.replaceLine('tau_t', replace_3, run_path+'/mdp/md_md.mdp')

      self.replaceLine('ref_t', replace_4, run_path+'/mdp/nvt.mdp')
      self.replaceLine('ref_t', replace_4, run_path+'/mdp/npt.mdp')
      self.replaceLine('ref_t', replace_4, run_path+'/mdp/md.mdp')
      self.replaceLine('ref_t', replace_4, run_path+'/mdp/md_pull.mdp')
      self.replaceLine('ref_t', replace_4, run_path+'/mdp/md_pull_5.mdp')
      self.replaceLine('ref_t', replace_4, run_path+'/mdp/md_md.mdp')


      #Find group, merge group, create group to index file
      #*********************************************************************************
      #create group receptor
      mergeGroup = ''
      nameOfGroup = ''
      nameOfLigand = ''
      firstResidue = True
      if int(Method) == 1 or int(Method) == 2:
        system = Avogadro.MoleculeFile.readMolecule(run_path+'/newbox.gro')

        for y in range(0,len(ReceptorResidues)):
          receptorResidue = ReceptorResidues[y]
          print receptorResidue

          domains = receptorResidue.split(',')
          for domain in domains:
            ResStart = domain.split('-')[0]
            ResEnd = domain.split('-')[1]

            AtomStart = system.residues[int(ResStart)].atoms[0]+1
            AtomEnd = system.residues[int(ResEnd)].atoms[len(system.residues[int(ResEnd)].atoms)-1]+1
            if firstResidue == True:
              firstResidue = False
            else:
              mergeGroup += ' | '
              nameOfGroup += '_'
            mergeGroup += 'a '+str(AtomStart)+'-'+str(AtomEnd)
            nameOfGroup += 'a_'+str(AtomStart)+'-'+str(AtomEnd)

        mergeGroup += '\\n'

        #   ResStart = receptorResidue.split(':')[0]
        #   ResEnd = receptorResidue.split(':')[1]

        #   print receptorResidue

        #   AtomStart = system.residues[int(ResStart)].atoms[0]+1
        #   AtomEnd = system.residues[int(ResEnd)].atoms[len(system.residues[int(ResEnd)].atoms)-1]+1
        #   if(y != 0):
        #    mergeGroup += ' | '
        #    nameOfGroup += '_'
        #   mergeGroup += 'a '+str(AtomStart)+'-'+str(AtomEnd)
        #   nameOfGroup += 'a_'+str(AtomStart)+'-'+str(AtomEnd)
        # mergeGroup += '\\n'

        #Check if ligand is protein => add index
        if os.path.isfile(run_path+'/ligand_residues.txt') is True:
          f = open(run_path+'/ligand_residues.txt', "r")
          contents = f.readlines()
          f.close()
          print contents[0]
          print system.numResidues
          AtomStart = system.residues[int(contents[0].split('-')[0])].atoms[0]+1
          AtomEnd = system.residues[int(contents[0].split('-')[1])].atoms[len(system.residues[int(contents[0].split('-')[1])].atoms)-1]+1
          mergeGroup += 'a '+ str(AtomStart)+'-'+str(AtomEnd) +'\\n'
          nameOfLigand = 'a_'+ str(AtomStart)+'-'+str(AtomEnd)

      #Add group to index and Create posre
      topolfile = run_path+'/topol.top'
      indexfile = run_path+'/index.ndx'
      try:
        ligandFolders = check_output('cd '+run_path+'; ls -d *.acpype', shell = True).splitlines()
      except subprocess.CalledProcessError as e:
        ligandFolders = []

      #ex: Protein_A01_FDA group
      mergeGroup += '\\"protein\\"'
      for y in range(0, len(ligandFolders)):
        ligandName = ligandFolders[y].split('.')[0]
        ligand = Avogadro.MoleculeFile.readMolecule(run_path+'/'+ligandFolders[y]+'/'+ligandName+'.pdb')
        resname = ligand.residues[0].name
        self.CallCommand(run_path, 'echo -e \"'+resname+'\\n\" | '+GroLeft+'genrestr'+GroRight+' -f '+ligandName+'.acpype/'+ligandName+'_GMX.gro -o posre_'+ligandName+'.itp -fc 1000 1000 1000')
        self.insertLine(ligandName+'.itp', 1, '#ifdef POSRES \n#include "posre_'+ligandName+'.itp" \n#endif \n', topolfile)

        mergeGroup += ' | \\"' + resname +'\\"'
      self.CallCommand(run_path, 'echo -e \"'+mergeGroup +'\\nq\\n\" | '+ GroLeft+'make_ndx'+GroRight+' -f solv_ions.gro -n index.ndx')
      #Change water to water_and_ions in index.ndx
      #replaceLine('[ Water ]', '[ Water_and_ions ]\n', indexfile)

      #change name of group
      if int(Method) == 1 or int(Method) == 2:
        self.replaceLine(nameOfGroup, '[ Receptor ]\n', indexfile)
      if os.path.isfile(run_path+'/ligand_residues.txt') is True:
        self.replaceLine(nameOfLigand, '[ '+ligandCurrent+' ]\n', indexfile)

      #*********************************************************************************
      if(GroVersion >= 5):
        self.CallCommand(run_path, 'cp mdp/md_pull_5.mdp mdp/md_pull_repeat.mdp')
        self.replaceLine('gen_vel','gen_vel   = yes\ngen_temp = 300\ngen_seed = -1\n', run_path+'/mdp/md_pull_repeat.mdp')
        self.replaceLine('pull-group2-name', 'pull-group2-name     = '+ligandCurrent+'\n', run_path+'/mdp/md_pull_repeat.mdp')
        if (self.dataController.getdata('smd-direction ') == 'True'):
          self.addLine('pull-coord1-vec = 0 0 1', run_path+'/mdp/md_pull_repeat.mdp')
          self.replaceLine('pull-geometry', 'pull-geometry  = direction  \n', run_path+'/mdp/md_pull_repeat.mdp')

      else:
        self.CallCommand(run_path, 'cp mdp/md_pull.mdp mdp/md_pull_repeat.mdp')
        self.replaceLine('gen_vel','gen_vel   = yes\ngen_temp = 300\ngen_seed = -1\n', run_path+'/mdp/md_pull_repeat.mdp')
        self.replaceLine('pull_group1', 'pull_group1     = '+ligandCurrent+'\n', run_path+'/mdp/md_pull_repeat.mdp')
        if (self.dataController.getdata('smd-direction ') == 'True'):
          self.addLine('pull_vec1 = 0 0 1', run_path+'/mdp/md_pull_repeat.mdp')
          self.replaceLine('pull_geometry', 'pull_geometry  = direction  \n', run_path+'/mdp/md_pull_repeat.mdp')

      self.replaceLine('continuation', 'continuation  = no   ; Restarting after NPT\n', run_path+'/mdp/md_pull_repeat.mdp')


  #**********************************************************************#
  #****************************  QSub File  *****************************#
  #**********************************************************************#

  def createQsubFile(self):
    call('cp '+root_path+'/source/top_pull.py '+main_path+'/run', shell = True)
    topfile= open(main_path+'/run/qsub.sh','w')

    cmd = ''
    cmd += '#!/bin/bash\n'
    cmd += 'mkdir ../analyse\n'
    cmd += 'rm -r ../analyse/*\n'
    cmd += 'for x in `ls -d run_*`; do\n'
    cmd += '  mkdir ../analyse/${x#"run_"}\n'
    cmd += '  cd $x\n'
    cmd += '  mkdir em\n'
    cmd += '  if [ ! -f em.gro ]; then\n'
    cmd += '    '+GroLeft+'grompp'+GroRight+' -maxwarn 20 -f mdp/minim.mdp -c solv_ions.gro -p topol.top -o em/em.tpr\n'
    cmd += '    '+GroLeft+'mdrun'+GroRight+' -v -deffnm em/em -cpt 5\n'
    cmd += '  fi\n'
    cmd += '  mkdir nvt\n'
    cmd += '  if [ ! -f nvt.gro ]; then\n'
    cmd += '    '+GroLeft+'grompp'+GroRight+' -maxwarn 20 -f mdp/nvt.mdp -c em/em.gro -p topol.top -n index.ndx -o nvt/nvt.tpr\n'
    cmd += '    '+GroLeft+'mdrun'+GroRight+' -v -deffnm nvt/nvt -cpt 5\n'
    cmd += '  fi\n'
    cmd += '  mkdir npt\n'
    cmd += '  if [ ! -f npt.gro ]; then\n'
    cmd += '    '+GroLeft+'grompp'+GroRight+' -maxwarn 20 -f mdp/npt.mdp -c nvt/nvt.gro -p topol.top -n index.ndx -o npt/npt.tpr\n'
    cmd += '    '+GroLeft+'mdrun'+GroRight+' -v -deffnm npt/npt -cpt 5\n'
    cmd += '  fi\n'
    cmd += '  mkdir md\n'
    cmd += '  if [ ! -f md.gro ]; then\n'
    cmd += '    '+GroLeft+'grompp'+GroRight+' -maxwarn 20 -f mdp/md.mdp -c npt/npt.gro -p topol.top -n index.ndx -o md/md.tpr\n'
    cmd += '    '+GroLeft+'mdrun'+GroRight+' -v -deffnm md/md -cpt 5\n'
    cmd += '  fi\n'
    cmd += '  pullx_path=""\n'
    cmd += '  pullf_path=""\n'
    cmd += '  mkdir smd\n'
    cmd += '  for i in $(seq 1 3); do \n'
    cmd += '    if [ ! -f md_st_$i.gro ]; then\n'
    cmd += '      '+GroLeft+'grompp'+GroRight+' -maxwarn 20 -f mdp/md_pull_repeat.mdp -c md/md.gro -t md/md.cpt -p topol.top -n index.ndx -o smd/md_st_$i.tpr\n'
    cmd += '      '+GroLeft+'mdrun'+GroRight+' -px smd/pullx_$i.xvg -pf smd/pullf_$i.xvg -deffnm smd/md_st_$i -v -cpt 5\n'
    cmd += '    fi\n'
    cmd += '    python2.7 parse_pull.py -x pullx_$i.xvg -f pullf_$i.xvg -o pullfx_$i.xvg\n'
    cmd += '    pullx_path="$pullx_path smd/pullx_$i.xvg"\n'
    cmd += '    pullf_path="$pullf_path smd/pullf_$i.xvg"\n'
    cmd += '  done\n'
    cmd += '  python2.7 pullana.py -px $pullx_path -pf $pullf_path -plot ../../analyse/${x#"run_"}/pull_force_time.png ../../analyse/${x#"run_"}/pull_force_distance.xvg -log ../../analyse/${x#"run_"}/pull_data.png -v 0.004\n'
    cmd += '  echo -e \"System\"|' + self.GroLeft+'trjconv'+self.GroRight+' -s md/md.tpr -f md/md.xtc -o md/md_noPBC.xtc -pbc mol -ur compact\n'
    if(self.GroVersion >= 5):
      cmd += 'echo -e \"Backbone\\nBackbone\"|' + self.GroLeft+'rms'+self.GroRight+' -s md/md.tpr -f md/md_noPBC.xtc -o md/rmsd.xvg -tu ns\n'
    else:
      cmd += 'echo -e \"Backbone\\nBackbone\"|' + 'g_rms'+self.GroRight+' -s md/md.tpr -f md/md_noPBC.xtc -o md/rmsd.xvg -tu ns\n'
    cmd += '  cd ..\n'
    cmd += '  python2.7 mathplot.py -i md/rmsd.xvg -o ../../analyse/rmsd.png\n'
    cmd += 'done\n'
    cmd += 'mv top_pull.py ../analyse\n'
    cmd += 'cd ../analyse\n'
    cmd += 'python2.7 top_pull.py\n'
    cmd += 'rm top_pull.py\n'

    topfile.write(cmd)
    topfile.close()




  #**********************************************************************#
  #**************************** Main Fuction ****************************#
  #**********************************************************************#

  def main(self):
    self.ParsePDBInput()
    self.setupOptions()
    self.PrepareLigand()
    self.PrepareLigandReceptor()
    self.PrepareCluster()
    self.EditMdpFile()
    self.SetupSystem()

    gromacsMD = GromacsMD()
    if run_mode == 'nohup':
      call('nohup python2.7 '+root_path+'/GromacsMD.py &', shell = True, executable='/bin/bash')
    elif run_mode == 'config':
      self.dataController.setdata('status', 'finished')
      self.createQsubFile()
    else:
      gromacsMD.setupOptions()
      gromacsMD.mdrun()














