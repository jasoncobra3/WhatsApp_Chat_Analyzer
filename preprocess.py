import re
import pandas as pd
def preprocess(data):
    pattern = '\d{1,2}\/\d{1,2}\/\d{2,4}, \d{1,2}:\d{1,2}\s[ap]m\s- '

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_messages': messages, 'message_dates': dates})
    df['message_dates'] = pd.to_datetime(df['message_dates'].str.strip(), format='%d/%m/%y, %I:%M %p -',
                                         errors='coerce')
    # separate users and messages
    users = []
    messages = []
    for message in df['user_messages']:
        entry = re.split('([\w\w]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[0])
            messages.append(entry[2])
        else:
            users.append('group notification')
            messages.append(entry[0])

    df['users'] = users
    df['messages'] = messages
    df.drop(columns=['user_messages'], inplace=True)

    df['date'] = df['message_dates'].dt.date
    df['year'] = df['message_dates'].dt.year
    df['month_num'] = df['message_dates'].dt.month
    df['month'] = df['message_dates'].dt.month_name()
    df['day'] = df['message_dates'].dt.day
    df['day_name'] = df['message_dates'].dt.day_name()
    df['hour'] = df['message_dates'].dt.hour
    df['minute'] = df['message_dates'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str("00"))
        elif hour == 0:
            period.append(str("00") + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period']=period
    return df
