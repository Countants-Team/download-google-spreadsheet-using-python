
# Download spreadsheet using sheets api in python

This component is use for download spreadsheet using sheets api in python. This is an end to end process of downloading spreadsheet in any format,Steps are given below. 

	
1. Run Below command one by one <br />
	(i)   sudo apt-get update <br />
    	(ii)  sudo apt-get -y install python-pip <br />
     	(iii) pip install --upgrade google-api-python-client
	
2. Now go to the below link - <br />
	https://console.developers.google.com/apis/library/sheets.googleapis.com <br />
	
3.  If project already created select project else create new project
4.  Click on ENABLE API
5.  Now search for Google Sheets API, click on Google Sheets API.
6.  Check Google Sheets API & Drive API are ENABLE or DISABLE if ENABLE then click on label.In below    screenshot API is already enabled
      
7.  Then Go to credentials. (In top left)
8.  At the top of the page, select the OAuth consent screen tab. Select an Email address, enter a Product name if not already set, and click the Save button.  

9.  Select the Credentials tab, click the Create credentials button and select OAuth client ID.
10. Select the application type Other, enter the name , and click the Create button.
11. Click OK to dismiss the resulting dialog. 
12. Click the download icon (Download JSON) button to the right of the client ID.
	
13.  Move this file to your working directory and rename it client_secret.json.
14.  Give access permission to the folder in which you want to download the file using below command<br />
	 sudo chmod 777 -R dirpath
15.  Fill the credential in ini file , And run below command.
16.  python fileDownloadfromGdrive.py 'fileDownloadfromGdrive.ini'

17. Ini file parameter description are below.<br />
    (i) clientsecretkeypath = your dir path/client_secret.json<br />
    (ii) spreadsheetid = your spreadsheet id<br />
    (iii) filename = file name you want to save<br />
    (iv) filepath = file path where you want to save<br />
    (v) mimetype = application/vnd.openxmlformats-officedocument.spreadsheetml.sheet

18. Mime list is below:	<br />	
    (i) MS Excel = application/vnd.openxmlformats-officedocument.spreadsheetml.sheet <br />
    (ii) Open Office sheet = application/x-vnd.oasis.opendocument.spreadsheet <br />
    (iii) PDF = application/pdf<br /> 
    (iv) CSV (first sheet only) = text/csv <br />
    (v) TSV (first sheet only)  = text/tab-separated-values <br />
    (vi) HTML (zipped) = application/zip
