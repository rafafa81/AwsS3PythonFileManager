import boto3
import pytz
from .Credentials import *


class AwsS3:
    def __init__(self):
        self.__S3_NAT_CREDS = S3_NAT_CREDS
        self.__S3_NAT_BUCKET = S3_NAT_BUCKET
        self.__bucketName = self.__S3_NAT_BUCKET
        self.__path = ""
        self.__s3 = self.__credentials_nat_assigment_client()

    def __credentials_nat_assigment_resource(self):
        return boto3.resource(
            service_name=self.__S3_NAT_CREDS['service_name'],
            region_name=self.__S3_NAT_CREDS['region_name'],
            aws_access_key_id=self.__S3_NAT_CREDS['aws_access_key_id'],
            aws_secret_access_key=self.__S3_NAT_CREDS['aws_secret_access_key']
        )

    def __credentials_nat_assigment_client(self):
        return boto3.client(
            service_name=self.__S3_NAT_CREDS['service_name'],
            region_name=self.__S3_NAT_CREDS['region_name'],
            aws_access_key_id=self.__S3_NAT_CREDS['aws_access_key_id'],
            aws_secret_access_key=self.__S3_NAT_CREDS['aws_secret_access_key']
        )

    def setEnv(self, env):
        if env == "NAT":
            s3 = self.__credentials_nat_assigment_client()
            self.__bucketName = self.__S3_NAT_BUCKET
        else:
            return "Ambiente no identificado"
        self.__s3= s3

    def getEnv(self):
        return self.__bucketName

    def getFilesList(self):
        listFolderArray = []
        dictFiles = {}
        result = self.__s3.list_objects(Bucket=self.__bucketName, Prefix=self.__path, Delimiter='/')
        if (type(result.get('CommonPrefixes'))) is not type(None):
            for ele in result.get('CommonPrefixes'):
                listFolderArray.append(ele.get('Prefix').strip('\n'))
        if 'Contents' in result.keys():
            for ele in result['Contents']:
                dictFiles[ele['Key']] = ele['LastModified'].astimezone(pytz.timezone('Mexico/General')).strftime(
                    "%d/%m/%Y %I:%M:%S %p")
        return self.__transformFilesList(listFolderArray,dictFiles)

    def downloadFile(self, fileName,username):
        s3 = self.__credentials_nat_assigment_resource()
        bucket = s3.Bucket(self.__bucketName)
        if self.getPath().endswith("/"):
            fileConcatenation=self.getPath() + fileName
        else:
            fileConcatenation=self.getPath() + "/" + fileName
        downloadedFileName="./downloaded_files/"+username+"/"+fileName
        try:
            bucket.download_file(Key=fileConcatenation, Filename=downloadedFileName)
        except:
            return False
        return True

    def setPath(self, path):
        self.__path = path

    def getPath(self):
        return self.__path

    #This function translates the information gathered to display only the directories and files name, not every complete path
    def __transformFilesList(self,directoriesList,filesDict):
        tempList=[]
        tempDict={}
        for ele in directoriesList:
            tempFolderName=ele.split("/")[-2]
            tempList.append(tempFolderName.strip('\n') + "/")
        for fileName,date in filesDict.items():
            tempFileNameFormatted=fileName.split("/")[-1]
            if  tempFileNameFormatted!= "":
                tempDict[tempFileNameFormatted]=date
        return tempList,tempDict
