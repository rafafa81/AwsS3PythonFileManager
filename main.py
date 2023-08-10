from MyLibraries.AwsS3 import AwsS3

obj=AwsS3()
obj.setPath('AwsS3Path/')
directories,files=obj.getFilesList()
obj.downloadFile("File_Name","Folder_User_Name")
print(files)







