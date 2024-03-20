import re
import pandas as pd

def preprocess(data):
    pattern='\d{2}/\d{2}/\d{2,4},\s\d{1,2}:\d{2}\s(?:[APMapm]{2}\s|)-\s'
    pattern2='\d{2}/\d{2}/\d{2,4},\s\d{2}:\d{2}\s[AaPp][Mm]\s-\s'

    messages = re.split(pattern,data)[1:]

    # if re.match(pattern2,data) is None:
    #     dates = re.findall(pattern,data)
    #     dates = [date.replace('\u202f', ' ') for date in dates]    
    # else:
    #     dates = re.findall(pattern,data)
    if re.search(pattern2,data):
        dates = re.findall(pattern,data)
        dates = [date.replace('\u202f', ' ') for date in dates]
    else:
        dates = re.findall(pattern,data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    #convert message_date type
    if re.search(pattern2,data):
        df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p - ')
    else:
        df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M - ')
   
    df.rename(columns={'message_date': 'date'},inplace=True)

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s',message)
        if entry[1:]:#username
            users.append(entry[1])
            messages.append(entry[2])
            
        else:
            users.append('Group_Notification')
            messages.append(entry[0]) 
            
    df['user']=users
    df['message']=messages
    df.drop(columns=['user_message'],inplace=True)
    df['year']= df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month']= df['date'].dt.month_name()
    df['day']= df['date'].dt.day
    df['hour']= df['date'].dt.hour
    df['minute']= df['date'].dt.minute
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()

    period = []

    for hour in df[['day_name','hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour+1))
        else:
            period.append(str(hour) + "-" + str(hour+1))

    df['period'] = period

    return df