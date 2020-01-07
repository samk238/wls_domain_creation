#D:\apps\wlshome\oracle_common\common\bin\wlst.cmd D:\wls_domain_creator_win.py
import os
import sys
import time
import fileinput
import re
from os.path import exists
from sys import argv
from shutil import copyfile

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def parsefile():
    propfile = get_script_path()+'\domain.properties'
    if exists(propfile):
        global fo
        fo = open(propfile, 'r+')
        lines = fo.readlines()
        for line in lines:
            #print line.rstrip()
            if "=" in line:
                line = line.rstrip()
                key = line.split('=')[0]
                value = line.split('=')[1]
                _dict[key]=value

def printdomain():
    print '------------------------------'
    print "Properties Information"
    print '------------------------------'
    for key, val in _dict.iteritems():
        print key,"=>",val

def export_properties():
    global _dict
    global mwhome
    global wlshome
    global domainroot
    global approot
    global domainNameF
    global domain_username
    global domain_password
    global adminPort
    global adminAddress
    global adminPortSSL
    global adminMachine
    global machines
    global servers
    global clusters
    
    mwhome = _dict.get('mwhome')
    wlshome = _dict.get('wlshome')
    domainroot = _dict.get('domainroot')
    approot = _dict.get('approot')
    domainNameF = _dict.get('domain_name')
    domain_username = _dict.get('domain_username')
    domain_password = _dict.get('domain_password')

    adminPort = _dict.get("admin.port")
    adminAddress = _dict.get("admin.address")
    adminPortSSL = _dict.get("admin.port.ssl")
    #adminMachine = _dict.get("admin.machine")

    machines = _dict.get("machines").split(',')
    servers = _dict.get("managedservers").split(',')
    clusters = _dict.get("clusters").split(',')

def read_template():
    # Load the template. Versions < 12.2
    try:
        readTemplate(wlshome + "\\common\\templates\\wls\\wls.jar")
    except:
        print "Error Reading the Template",wlshome
        print "Dumpstack: \n -------------- \n",dumpStack()
        sys.exit(2)

def create_machine():
    try:
        cd('/')
        for machine in machines:
            print "Creating a New Machine with the following Configuration"
            mn = create(machine,'Machine')
            machine_name=_dict.get(machine+'.Name')
            machine_listenadd=_dict.get(machine+'.listenaddress')
            if (machine_name != ""):
                print "\tMachine Name",machine_name
                mn.setName(machine_name)
            else:
                print "No machine Name mentioned for",machine
    except:
        print "Creating Machine failed",machine
        print "Dumpstack: \n -------------- \n",dumpStack()
        sys.exit(2)

def create_admin():
    try:
        print "\nCreating AdminServer with the following Configuraiton"
        cd('/Security/base_domain/User/' + domain_username)
        cmo.setPassword(domain_password)
        cd('/Server/AdminServer')
        cmo.setName('AdminServer')
        cmo.setListenPort(int(adminPort))
        cmo.setListenAddress(adminAddress)
        print "\tAdminServer ListenPort:",adminPort
        print "\tAdminServer Listenaddress:",adminAddress
        print "\tAdminServer SSLListenPort:",adminPortSSL

        create('AdminServer','SSL')
        cd('SSL/AdminServer')
        set('Enabled', 'True')
        set('ListenPort', int(adminPortSSL))

    except:
        print "Error while creating AdminServer"
        print "Dumpstack: \n -------------- \n",dumpStack()

def create_managedserver():
    try:
        cd ('/')
        for server in servers:
            MSN = _dict.get(server+'.Name')
            MSP = _dict.get(server+'.port')
            MSA = _dict.get(server+'.address')
            MSM = _dict.get(server+'.machine')
            print "\nCreating A New Managed Server with following Configuration"
            print "\tServerName:",MSN
            print "\tServer ListenPort:",MSP
            print "\tServer ListenAddress:",MSA
            sobj = create(MSN,'Server')
            sobj.setName(MSN)
            sobj.setListenPort(int(MSP))
            sobj.setListenAddress(MSA)

            #sobj.setMachine(MSM)
    except:
        print "Error While Creating ManagedServer",server
        print "Dumpstack: \n -------------- \n",dumpStack()

def create_clusters():
    try:
        cd ('/')
        for cluster in clusters:
            CN = _dict.get(cluster+'.Name')
            cobj = create(CN,'Cluster')
            print "\nCreating a New Cluster with the following Configuration"
            print "\tClusterName",CN
    except:
        print "Error while Creating Cluster",cluster
        print "Dumpstack: \n -------------- \n",dumpStack()
        sys.exit(2)

def commit_writedomain():
    try:
        # If the domain already exists, overwrite the domain
        setOption('OverwriteDomain', 'true')

        setOption('ServerStartMode','prod')
        setOption('AppDir', approot + "\\" + domainNameF)

        writeDomain(domainroot + "\\" + domainNameF)
        closeTemplate()

    except:
        print "ERROR: commit_writedomain Failed"
        print "Dumpstack: \n -------------- \n",dumpStack()
        undo('false','y')
        stopEdit()
        exit()

def print_withformat(title):
    print "\n-----------------------------------------------------\n",title,"\n-----------------------------------------------------"

def print_somelines():
    print "-----------------------------------------------------"

def print_domainsummary():
    print "domainNameF:",domainNameF
    print "DomainUserName:",domain_username
    print "DomainPassword: ****************"
    print "DomainDirectory:",domainroot
    print "ApplicationRoot:",approot

def start_AdminServer():
    import time
    global startfalg
    startfalg = 1
    global managementurl
    managementurl = "t3://"+adminAddress+":"+adminPort
    global AdminServerDir
    AdminServerDir = domainroot+"\\"+domainNameF+"\\servers\\AdminServer"
    global AdminServerLogDir
    AdminServerLog = AdminServerDir+"\\logs\\AdminServer.log"
    global DomainDir
    DomainDir = domainroot+"\\"+domainNameF
    try:
        #connect('weblogic','weblogic1','t3://10.84.9.60:7001')
        connect(domain_username,domain_password,managementurl)
        startfalg = 0
        print "ADMIN SERVER is already running, using existing connection for WLST..."
    except:
        print "\n\t Unable to connect ADMIN SERVER using WLST CONNECT.."
        print "\t Proceeding with starting the ADMIN SERVER..\n"

    if startfalg != 0:
        try:
            print_somelines()
            print "\nStarting Server with following Params"
            print_somelines()
            print "DomainDir",DomainDir
            print "managementurl",managementurl
            print_somelines()
        
            print "\nRedirecting Startup Logs to",AdminServerLog
            startServer('AdminServer',domainNameF,managementurl,domain_username,domain_password,DomainDir,'true',300000,serverLog=AdminServerLog)
        
            print "AdminServer has been successfully Started"
        except:
            print "ERROR: Unable to Start AdminServer after 5 minutes, please check the ADMIN logs and make corrections..."
            print "Log location:", AdminServerLog
            print "Dumpstack: \n -------------- \n",dumpStack()

def connect_online():
    try:
        global managementurl
        managementurl = "t3://"+adminAddress+":"+adminPort
        print "\nConnecting to AdminServer with managementurl",managementurl
        connect(domain_username,domain_password,managementurl)
        print "\nSuccessfully Connected to AdminServer!!."
        
    except:
        print "ERROR: Unable to Connect to AdminServer"
        sys.exit(2)

def acquire_edit_session():
    edit()
    startEdit()

def save_activate_session():
    save()
    activate()

def Enable_wlst_log_redirection():
    #wlst output redirect to a logfile
    exelogfile = get_script_path()+'\wlst_execution.log'
    redirect(exelogfile,'false')

def Stop_wlst_log_redirection():
    stopRedirect()

def map_machines():
    #try:
    acquire_edit_session()
    for machine in machines:
         print "Starting to map resources to the machine ",machine
         instances = _dict.get(machine+".instances")
         #print "INST",instances
         if len(instances) > 1:
             instances = instances.split(',')
             for instance in instances:
                if instance == "admin":
                    instname = "AdminServer"
                else:
                    instname = _dict.get(instance+".Name")
                    mtype = _dict.get(machine+'.Type')
                    mlistnadd = _dict.get(machine+'.Listenaddress')
                    mport = _dict.get(machine+'.Port')
                #print "What is the instname",instname
                cd ('/Servers/'+instname)
                #print "WHARE AM I",pwd()
                machine_name=_dict.get(machine+'.Name')
                mbean_name='/Machines/'+machine_name
                #print "What is Machine MBEAN",mbean_name
                cmo.setMachine(getMBean(mbean_name))
                cd(mbean_name+'/NodeManager/'+machine_name)
                cmo.setNMType(mtype)
                cmo.setListenAddress(mlistnadd)
                cmo.setListenPort(int(mport))
                cmo.setDebugEnabled(false)
         else:
                instname = _dict.get(instances+".Name")
                #print "What is the instname",instname
                cd ('/Servers/'+instname)
                #print "WHARE AM I",pwd()
                machine_name=_dict.get(machine+'.Name')
                mbean_name='/Machines/'+machine_name
                cmo.setMachine(getMBean(mbean_name))    
    save_activate_session()

def map_clusters():
    #try:
    acquire_edit_session()
    for cluster in clusters:
        print "\nStarting to map resources to the cluster ",cluster
        members = _dict.get(cluster+".members")
        clusterAddress = ""
        #print "members",members
        if len(members) > 1:
            members = members.split(',')
            for member in members:
                if member == "admin":
                    membername = "AdminServer"
                else:
                    membername = _dict.get(member+".Name")
                #print "What is the memberName",membername
                cd ('/Servers/'+membername)
                #print "WHARE AM I",pwd()
                cluster_name=_dict.get(cluster+'.Name')
                mbean_name='/Clusters/'+cluster_name
                #print "What is Cluster MBEAN",mbean_name
                cmo.setCluster(getMBean(mbean_name))
                clusterAddressip = _dict.get(member+'.address')
                clusterAddressport = _dict.get(member+'.port')
                clusterAddress = clusterAddress+","+clusterAddressip+":"+clusterAddressport
            cd ('/Clusters/'+cluster_name)
            cmo.setClusterAddress(clusterAddress[1:])
            cmo.setWeblogicPluginEnabled(true)
        else:
                membername = _dict.get(member+".Name")
                #print "What is the memberName",membername
                cd ('/Servers/'+membername)
                #print "WHARE AM I",pwd()
                cluster_name=_dict.get(cluster+'.Name')
                mbean_name='../../Clusters/'+cluster_name
                cmo.setCluster(getMBean(mbean_name))    
    save_activate_session()
    #except:
        #print "Machine Creation Failed"

def boot_props():
    BFileName = AdminServerDir + "\\security\\boot.properties"
    if os.path.isfile(BFileName):
        print("boot.prop file exists..")
    else:
        Sdir = AdminServerDir + "\\security"
        if not os.path.exists(Sdir):
            os.makedirs(Sdir)

        bp = open(BFileName,"w+")
        bp.write("username=%s\n" %(domain_username))
        bp.write("password=%s" %(domain_password))
        bp.close()

def status_check():
    import time
    global statusflag
    statusflag = 1
    global managementurl
    managementurl = "t3://"+adminAddress+":"+adminPort
    try:
        #connect('weblogic','weblogic1','t3://10.84.9.60:7001')
        connect(domain_username,domain_password,managementurl)
        statusflag = 0
    except:
        print "\n\t Unable to connect ADMIN SERVER using WLST CONNECT.."
        print "\t Proceeding with domain build steps.. Assuming ADMIN is in SHUTDOWN STATE..\n"
        #time.sleep(15)
    
    if statusflag == 0:
        #connect('weblogic','weblogic1','t3://10.84.9.60:7001')
        connect(domain_username,domain_password,managementurl)
        servers=cmo.getServers()
        print "-------------------------------------------------------"
        print "\t"+cmo.getName()+" domain status"
        print "-------------------------------------------------------"
        
        domainRuntime();
        server_lifecycles = cmo.getServerLifeCycleRuntimes();
        for server_lifecycle in server_lifecycles:
            print " --> " + server_lifecycle.getName() + " is " + server_lifecycle.getState()
        
        print "-------------------------------------------------------"
        for server_lifecycle in server_lifecycles:
            if (server_lifecycle.getState() == 'RUNNING'):
                print ""
                print server_lifecycle.getName() + ' is in "RUNNING" mode, please "SHUTDOWN" and re-run the script.'
                print ""
                Stop_wlst_log_redirection()
                sys.exit(1)

def nm_modify():
    import os
    import sys
    import time
    import fileinput
    import re
    from os.path import exists
    from sys import argv
    from shutil import copyfile
    global NMProps
    global NMConfF
    NMProps = domainroot+"\\"+domainNameF+"\\nodemanager\\nodemanager.properties"
    NMConfF = domainroot+"\\"+domainNameF+"\\config\\nodemanager\\nm_password.properties"
    #NM Credentials
    copyfile (NMConfF, NMConfF+".ORG")
    open(NMConfF, 'w').close
    nm = open(NMConfF,"w+")
    nm.write("username=%s\n" %(domain_username))
    nm.write("password=%s" %(domain_password))
    nm.close()
    #NM Properties
    copyfile (NMProps, NMProps+".ORG")
    orig_stdout = sys.stdout
    nmfb = open(NMProps+".ORG")
    nmf = open(NMProps, 'w')
    sys.stdout = nmf
    lpattern = re.compile("ListenAddress=")
    Spattern = re.compile("SecureListener=")
    for line in nmfb:
        if lpattern.search(line):
            print(re.sub (r"ListenAddress=*", "ListenAddress=", "ListenAddress=%s") %(adminAddress))
        elif Spattern.search(line):
            print(re.sub (r"SecureListener=*", "SecureListener=", "SecureListener=false"))
        else:
            print(line).rstrip()
    sys.stdout = orig_stdout
    nmf.close()

if __name__ != "__main__":
    _dict={};
    Enable_wlst_log_redirection()
    print "--> Start of the script Execution >>"
    print "\n--> Parsing the properties file..."
    parsefile()
    print "\n--> Exporting the Properties to variables.."
    export_properties()
    print "\n--> Checking domain state.. before proceeding any further.."
    #status_check()
    print "\n--> Creating Domain from Domain Template..."
    read_template()
    print_withformat("Creating Machines")
    create_machine()
    print_somelines()
    print_withformat("Creating AdminServer")
    create_admin()
    print_somelines()
    print_withformat("Creating ManagedServers")
    create_managedserver()
    print_somelines()
    print_withformat("Creating Clusters")
    create_clusters()
    print_somelines()
    print "\n--> Commit and Saving the Domain"
    commit_writedomain()
    print_withformat("Domain Summary")
    print_domainsummary()
    print_somelines()
    print "\n--> Updating NM properties"
    nm_modify()
    print "\n--> Starting the AdminServer"
    start_AdminServer()
    connect_online()
    map_machines()
    map_clusters()
    print "\n--> Updating the boot.properties file"
    boot_props()
    print "\n--> End of Script Execution << \nGood Bye!"
    Stop_wlst_log_redirection()
    sys.exit(0)

if __name__ == "__main__":
    print "This script has to be executed with weblogic WLST"
    print "example:  D:\apps\wlshome\oracle_common\common\bin\wlst.cmd D:\wls_domain_creator.py"
