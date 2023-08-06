Job command examples
====================

### Full list of all the available job commands

Print list of all the jobs:

    jcli job list

Print jobs which contain the string 'coreci' in their names:

    jcli job list coreci

Print the number of jobs on Jenkins server:

    jcli job count

Print the number of jobs on Jenkins server which contain the string 'core':

    jcli job count core

Delete job:
   
    jcli job delete <job_name>

Build parameterized job:

    jcli job build <job_name> -p '{"GERRIT_REFSPEC": "my_refspec", "GERRIT_BRANCH": "my_branch", "Cleanup_provisioned_resources":"true"}'

Build parameterized job by providing YAML file with parameters:

    vi /my/yaml/file
    "GERRIT_REFSPACE": "x"
    "GERRIT_BRANCH": "y"

    jcli job build <job_name> -y /path/to/yaml/file

Copy job:

    jcli job copy my_current_job my_new_awesome_job

Disable job:

    jcli job disable my_job

Enable job:

    jcli job enable his_job

Print information on last build of specific job:

    jcli job last_build super-mario-job
