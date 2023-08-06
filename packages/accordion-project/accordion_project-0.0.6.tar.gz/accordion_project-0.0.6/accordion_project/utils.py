import requests
import os


'''
Select the correct key field from an operation or event message
 * message is a dictionary whose content depends on the operation
'''
def get_correct_key(message):

    # {"operation":"deploy", "componentInfo":"acc-orbkhdrw-0-0-3-q123e-gameserver", "minicloudId":"minicloud3", 
    # "timestamp":123456789, "token":"jks8o23rfo2i4"}

    key = None
    if "componentInfo" in message:
        key = string['componentInfo']
    elif "appInfo" in message:
        key = string['appInfo']
    elif "runningComponentInfo" in message:
        key = string['runningComponentInfo']

    return key

'''
Parses an ACCORDION id and returns an object with all namespace segments
'''
def parse(data):

    # acc-OVR-0-0-1-q123e-LSPart-345gr-min1
    delimiter = '-'
  
    def find_all(a_str, sub):
        start = 0
        while True:
            start = a_str.find(sub, start)
            if start == -1: return
            yield start
            start += len(sub) # use start += 1 to find overlapping matches
    
    occurences = list(find_all(data, '-'))
    index = 0
    segments = []
    count = 0
    for i in range(len(data)):
        if data[i] == delimiter:
            if count == 2 or count == 3:
                count = count + 1
                continue
            segments.append(data[index:i])
            index = i + 1
            count = count + 1
        if i == len(data)-1:
            segments.append(data[index:i+1])

    print(segments)
    # dataList = list(data)
    # dataList[occurences[2]] = '.'
    # dataList[occurences[3]] = '.'
    # data = ''.join(dataList)

    # segments = data.split('-')
    if len(segments)<3:
        raise Exception('Wrong syntax. At least the path segments: root, application name and application version are required.');

    if len(segments)>7:
        raise Exception('Wrong syntax. At most 7 path segments are expected.');

    root = segments[0]
    if root != 'acc':
        raise Exception('non ACCORDION namespace')
    
    appName = segments[1]
    appVersion = segments[2]

    if appName == None or appVersion == None:
        raise Exception('Application name and version are compulsory fields.')

    appInstanceId = segments[3] if len(segments)>3 else None
    componentName = segments[4] if len(segments)>4 else None
    runningInstanceId = segments[5] if len(segments)>5 else None
    minicloudId = segments[6] if len(segments)>6 else None

    appInfo = delimiter.join([root,appName,appVersion])
    appInstanceInfo = delimiter.join([appInfo,appInstanceId]) if appInstanceId is not None else None
    componentInfo = delimiter.join([appInstanceInfo,componentName]) if appInstanceInfo is not None and componentName is not None else None
    runningComponentInfo = delimiter.join([componentInfo,runningInstanceId,minicloudId]) if componentInfo is not None and runningInstanceId is not None and minicloudId is not None else None

    return {'root':root, 'appName':appName, 'appVersion':appVersion, 'appInstanceId':appInstanceId, 'componentName':componentName, 'runningInstanceId':runningInstanceId, 'minicloudId':minicloudId, 'appInfo':appInfo, 'appInstanceInfo':appInstanceInfo, 'componentInfo':componentInfo, 'runningComponentInfo':runningComponentInfo}

'''
Fetch the intermediate model from the application bucket
'''
# 'http://app.accordion-project.eu:31724/application?name=29-09-22-testig-ri&isLatest=true&version=0.0.1'
def fetch_intermediate_model(application_name, application_version = None):

    APPLICATION_BUCKET_URL = os.getenv('APPLICATION_BUCKET_URL')
    if APPLICATION_BUCKET_URL == None:
        APPLICATION_BUCKET_URL = "http://app.accordion-project.eu:31724"
    print('Application bucket is at: '+APPLICATION_BUCKET_URL)

    application_version = application_version.replace("-", ".")

    print ("Fetching the application model for: ", application_name, application_version, flush=True)

    params = {
        'name' : application_name
        }
    if application_version is None:
        params['isLatest'] = True
    else:
        params['version'] = application_version
        params['isLatest'] = True # <-- We do this as a workaround for the bug in the Application bucket
    

    headers = {
        'Authorization' : "Basic Z3VpX2JhY2tlbmQ6M1EvMF46aGVqODlzczgsb1leWTpzTG1nK15lL2NMMCxLa21sTVg="
    }

    r = requests.get(APPLICATION_BUCKET_URL+"/application", headers = headers, params = params)

    return r