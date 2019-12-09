# Directory where the software to be installed is located
$WLS_SOFTWARE_DIRECTORY="D:\download\webLogic"
$WLS_SOFTWARE_FILE="${WLS_SOFTWARE_DIRECTORY}\V886423-01_WebLogic_Server_12.2.1.3.0.zip"
$JAVA_SOFTWARE_FILE="D:\download\java\jdk-8u181-windows-x64.exe"

# Name of JVM file
$JVM_FILE_NAME="jdk-8u181-windows-x64.exe"

# Name of the WebLogic file
$WEBLOGIC_JAR_FILE_NAME="fmw_12.2.1.3.0_wls.jar"

# The scripts create files that are placed in this directory
$TEMPORARY_DIRECTORY="${WLS_SOFTWARE_DIRECTORY}\files"

# Base directory
$BASE_DIRECTORY="d:\apps"

# Directory that will used for the installation and configuration
$RUNTIME_HOME="${BASE_DIRECTORY}\wlshome"

# Directory where the JVM will be installed
$JAVA_HOME="${BASE_DIRECTORY}\java\jdk1.8.0_181"
$JRE_HOME="${BASE_DIRECTORY}\java\jre8"

# Directory that will be used as the middleware home (holds software binaries)
$MIDDLEWARE_HOME="${RUNTIME_HOME}"

# Name of the domain
$DOMAIN_NAME="p6api_domain"

# Directory where the configuration will be placed
$CONFIGURATION_HOME="${RUNTIME_HOME}\user_projects"

# Domain home (directory that contains the domain configuration files)
$DOMAIN_CONFIGURATION_HOME="${CONFIGURATION_HOME}\domains\${DOMAIN_NAME}"

# Domain application home (directory in which application related artifacts are placed)
$DOMAIN_APPLICATION_HOME="${CONFIGURATION_HOME}\applications\${DOMAIN_NAME}"

# Node manager home (directory that contains the node manager configuration files)
$NODE_MANAGER_HOME="${CONFIGURATION_HOME}\nodemanagers\${DOMAIN_NAME}"

# Default homes that are created when the software is installed
$COHERENCE_HOME="${MIDDLEWARE_HOME}\coherence"
$FUSION_MIDDLEWARE_HOME="${MIDDLEWARE_HOME}\oracle_common"
$WEBLOGIC_HOME="${MIDDLEWARE_HOME}\wlserver"