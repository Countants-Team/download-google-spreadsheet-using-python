"""Hello Analytics Reporting API V4."""
import sys
import csv
import os
import ast
import ConfigParser


from shutil import copyfile

from apiclient.discovery import build

from oauth2client.service_account import ServiceAccountCredentials

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']



config_file = sys.argv[1]
config = ConfigParser.ConfigParser()
config.read(config_file)

csvFileName = config.get("gaVarList", "csvFileName")

keyFileLocation = config.get("gaVarList", "keyFileLocation")
viewId = config.get("gaVarList", "viewId")

startDate = config.get("gaVarList", "startDate")
endDate = config.get("gaVarList", "endDate")
metrics = config.get("gaVarList", "metrics")
dimensions = config.get("gaVarList", "dimensions")
filtersField = config.get("gaVarList", "filtersField")
sortField = config.get("gaVarList", "sortField")
sortOrder = config.get("gaVarList", "sortOrder")
maxResults = config.get("gaVarList", "maxResults")


tempfolder = config.get("gaVarList", "tempfolder")
jobname = config.get("gaVarList", "jobname")


orderBy=[]

if(filtersField==""):
    filtersField = ''

if(sortField =="" and sortOrder==""):
    orderBy = []
else:
    orderBy = [{'fieldName': sortField, 'orderType': 'VALUE', 'sortOrder': sortOrder}]



dim = [x for (x) in dimensions.split(',') if x]
mat = [x for (x) in metrics.split(',') if x]

dimvar = []
dimData =[]

matVar = []
matData =[]

dimvar =["{'name': "+"'"+s+"'"+'}' for s in dim]
matVar = ["{'expression': "+"'"+s+"'"+'}' for s in mat]

dimData = [ast.literal_eval(x) for x in dimvar]
matData = [ast.literal_eval(x) for x in matVar]

date_ranges = [(startDate,endDate)]

#if path not exist create path
if not os.path.exists(tempfolder+jobname):
        os.makedirs(tempfolder+jobname)
    


def initialize_analyticsreporting():
    """Initializes an Analytics Reporting API V4 service object.

    Returns:
      An authorized Analytics Reporting API V4 service object.
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        keyFileLocation, SCOPES)

    # Build the service object.
    analytics = build('analytics', 'v4', credentials=credentials)

    return analytics


def get_report(pag_index,analytics):
    """Queries the Analytics Reporting API V4.

    Args:
      analytics: An authorized Analytics Reporting API V4 service object.
    Returns:
      The Analytics Reporting API V4 response.
    """
    return analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': viewId,
                    'dateRanges': [{'startDate': startDate, 'endDate': endDate}],
                    'metrics': matData,
                    'dimensions': dimData,
                    'filtersExpression':filtersField,
                    'orderBys':orderBy,
                    'pageToken': str(pag_index),
                    'pageSize':str(pag_index+10000)
                }]
        }
    ).execute()


def print_response(response):
    """Parses and prints the Analytics Reporting API V4 response.

    Args:
      response: An Analytics Reporting API V4 response.
    """
    for report in response.get('reports', []):
        columnHeader = report.get('columnHeader', {})
        dimensionHeaders = columnHeader.get('dimensions', [])
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

        for row in report.get('data', {}).get('rows', []):
            dimensions = row.get('dimensions', [])
            dateRangeValues = row.get('metrics', [])

            for header, dimension in zip(dimensionHeaders, dimensions):
                print header + ': ' + dimension

            for i, values in enumerate(dateRangeValues):
                # print 'Date range: ' + str(i)
                for metricHeader, value in zip(metricHeaders, values.get('values')):
                    print metricHeader.get('name') + ': ' + value


def save_report_data(response, outfile, type, count):
    for report in response.get('reports', []):
        print count
        if count == 0:
            create_header = True
            count += 1
        else:
            create_header = False

	reload(sys)
        sys.setdefaultencoding('utf8')


        f = open(outfile, type)
        writer = csv.writer(f, lineterminator='\n')

        columnHeader = report.get('columnHeader', {})
        dimensionHeaders = columnHeader.get('dimensions', [])
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
        rows = report.get('data', {}).get('rows', [])

        header_row = []
        temp_header_row = []
        header_row.extend(dimensionHeaders)
        header_row.extend([mh['name'] for mh in metricHeaders])
        temp_header_row.extend(header_row)

        if create_header:
            writer.writerow(temp_header_row)

        for row in rows:
            dimensions_data = row.get('dimensions', [])
            metrics_data = [m['values'] for m in row.get('metrics', [])][0]

            data_row = []
            temp_data_row = []
            data_row.extend(dimensions_data)
            data_row.extend(metrics_data)

            temp_data_row.extend(data_row)
            writer.writerow(temp_data_row)

        # Close the file.
        f.close()


def main():
    if os.path.isfile(iniBakup):
        os.remove(iniBakup)
    copyfile(iniPath, iniBakup)
    response = ''
    analytics = initialize_analyticsreporting()
    outfile = tempfolder+jobname + csvFileName
    count = 0
    for start_date, end_date in date_ranges:
        limit = get_report(0,analytics)
        rowCount = limit['reports'][0]['data']['rowCount']
        for pag_index in xrange(0, rowCount, int(maxResults)):
            response = get_report(pag_index,analytics)
            if count == 0:
                save_report_data(response, outfile,'wt',count)
                count += 1
            else:
                save_report_data(response, outfile, 'a',count)
    

if __name__ == '__main__':
    main()
