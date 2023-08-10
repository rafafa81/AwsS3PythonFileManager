# AwsS3PythonFileManager
Hi everyone, this is my first ever module created for an easier files and directories management of AWS S3 using python, hope it helps you all whenever you needed

The Python modules needed are:
boto3
pytz

As an example i'm adding the main.py, it is needed to create the instance and set the path to start working with the module, the S3 configurations are initializated at the creation of the object taking the information from the Credentials.py variables

Methods:

Used jus in case of adding more than one environment to AwsS3 code
setEnv(String environment):void
getEnv():String

Returns directories and files for current path
getFilesList():String,String

You must have created the subfolder "downloaded_files/<username>/" on your basedirectory
downloadFile(String fileName,String username):boolean

Path interactors to move between s3 directories
setPath(String path):void
getPath():String
