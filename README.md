# wls_domain_creation

PLEASE INSTALL JAVA AND FMW before running below
   --> check repository "java_fmw_install" for details

Update "domain.properties" file as needed and run script as below

If using Windows:
D:\apps\wlshome\oracle_common\common\bin\wlst.cmd D:\wls_domain_creator.py

Incase of UNIX envs:
Please update the "wls_domain_creator.py" script as below for proper dir structure handling..
1. Search and replace "\" with "/"
2. Save and run
   /apps/wlshome/oracle_common/common/bin/wlst.cmd  script_dir/wls_domain_creator.py
Test
