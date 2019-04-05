import json
import numpy as np
import datetime
import matplotlib.pylab as pylab
from matplotlib.patches import Rectangle
from itertools import compress

def plot_users_in_timeline(august_users, august_seconds, monthname='August'):
    morning = '6am-12am'
    afternoon = '12pm-16pm'
    evening = '16pm-20pm'
    night = '20pm-6pm'
    bins = [0, 6, 12, 16, 20, 24]
    august_users_binned = [np.sum(august_users[np.bitwise_and(august_seconds >= bins[i] * 3600,
                                                              august_seconds < bins[i + 1] * 3600)]) for i in
                           range(len(bins) - 1)]

    ##########  PLOT AUGUST USERS IN TIMELINE
    pylab.figure(figsize=(10,7))
    pylab.plot(np.asarray(august_seconds) / 3600, august_users, '.')
    pylab.xlabel('Time of the day (hours)')
    pylab.ylabel('Number of users')
    h = np.max(august_users) * 1.2
    pylab.ylim([0, h])
    c = [np.asarray([(255 - 100) / 255, (255 - 20) / 255, (255 - 40) / 255]),
         np.asarray([(255 - 20) / 255, (255 - 100) / 255, (255 - 40) / 255]),
         np.asarray([(255 - 40) / 255, (255 - 20) / 255, (255 - 100) / 255]),
         np.asarray([(255 - 40) / 255, (255 - 100) / 255, (255 - 100) / 255]),
         np.asarray([(255 - 100) / 255, (255 - 100) / 255, (255 - 40) / 255])]
    currentAxis = pylab.gca()

    currentAxis.add_patch(Rectangle([0, 0], 6 * 3600, h, facecolor=c[0]))
    currentAxis.text(0, h * 0.95, 'NIGHT', color='k')
    currentAxis.text(0, h * 0.90, '00am-6am', color='k')
    currentAxis.text(0, h * 0.85, str(int(august_users_binned[0])) + ' users', color='k')

    currentAxis.add_patch(Rectangle([6, 0], 6 * 3600, h, facecolor=c[1]))
    currentAxis.text(6, h * 0.95, 'MORNING', color='k')
    currentAxis.text(6, h * 0.90, '6am-12pm', color='k')
    currentAxis.text(6, h * 0.85, str(int(august_users_binned[1])) + ' users', color='k')

    currentAxis.add_patch(Rectangle([12, 0], 4 * 3600, h, facecolor=c[2]))
    currentAxis.text(12, h * 0.95, 'AFTERNOON', color='k')
    currentAxis.text(12, h * 0.90, '12pm-16pm', color='k')
    currentAxis.text(12, h * 0.85, str(int(august_users_binned[2])) + ' users', color='k')

    currentAxis.add_patch(Rectangle([16, 0], 4 * 3600, h, facecolor=c[3]))
    currentAxis.text(16, h * 0.95, 'EVENING', color='k')
    currentAxis.text(16, h * 0.90, '16pm-20pm', color='k')
    currentAxis.text(16, h * 0.85, str(int(august_users_binned[3])) + ' users', color='k')

    currentAxis.add_patch(Rectangle([20, 0], 4 * 3600, h, facecolor=c[4]))
    currentAxis.text(20, h * 0.95, 'NIGHT', color='k')
    currentAxis.text(20, h * 0.90, '20pm-24pm', color='k')
    currentAxis.text(20, h * 0.85, str(int(august_users_binned[4])) + ' users', color='k')

    currentAxis.text(2, h * 1.05, 'Total Users in ' + monthname + ': ' + str(int(np.sum(august_users_binned))), color='k')
    pylab.savefig(monthname + '_day.png')

def get_users_seconds(data_august):
    august_events = []
    august_seconds = []
    august_users = []
    i = 0
    for item in data_august['logs']:
        august_events.append(datetime.datetime.strptime(item['timestamp'], '%Y-%m-%d %H:%M:%S'))
        august_seconds.append(august_events[i].second+august_events[i].minute*60+august_events[i].hour*3600)
        august_users.append(data_august['logs'][i]['users'])
        i += 1
    august_seconds = np.asarray(august_seconds)
    august_users = np.asarray([float(item) for item in august_users])
    return august_users, august_seconds

def get_error_plot(seconds, data, monthname):
    correct = np.asarray([int(data['logs'][i]['queries']['correct'])for i in range(len(data['logs']))])
    error = np.asarray([int(data['logs'][i]['queries']['error'])for i in range(len(data['logs']))])
    total = np.asarray([int(data['logs'][i]['users'])for i in range(len(data['logs']))])

    error_rate1 = np.divide(error, error+correct)
    error_rate2 = np.divide(error, total)

    pylab.figure()

    pylab.subplot(211)
    pylab.plot(seconds/3600, error_rate1*100, '.')
    currentAxis = pylab.gca()
    currentAxis.text(1, np.max(error_rate1*100)*1.05, '# of logs: ' + str(np.sum(error)+np.sum(correct)), color='k')
    currentAxis.text(1, np.max(error_rate1*100)*0.95, 'Total errors: ' + str(np.sum(error)), color='k')
    currentAxis.text(1, np.max(error_rate1*100)*0.85, 'error_rate=error/(error+correct)', color='k')
    currentAxis.text(1, np.max(error_rate1*100)*0.75, 'mean error-rate: ' + str(np.mean(error_rate1)), color='k')
    currentAxis.text(1, np.max(error_rate1*100)*0.65, 'std error-rate: ' + str(np.std(error_rate1)), color='k')

    pylab.ylabel('Error rate (%)')

    pylab.subplot(212)
    pylab.plot(seconds / 3600, error_rate2 * 100, '.')
    currentAxis = pylab.gca()
    currentAxis.text(1, np.max(error_rate2*100)*1.05, '# of logs: ' + str(np.sum(error) + np.sum(correct)), color='k')
    currentAxis.text(1, np.max(error_rate2*100)*0.95, 'Total errors: ' + str(np.sum(error)), color='k')
    currentAxis.text(1, np.max(error_rate2*100)*0.85, 'error_rate=error/users', color='k')
    currentAxis.text(1, np.max(error_rate2*100)*0.75, 'mean error-rate: ' + str(np.mean(error_rate2)), color='k')
    currentAxis.text(1, np.max(error_rate2*100)*0.65, 'std error-rate: ' + str(np.std(error_rate2)), color='k')

    pylab.xlabel('Time of the day (hours)')
    pylab.ylabel('Error rate (%)')
    pylab.savefig(monthname + '_errors.png')

def get_month_plot(seconds, data, monthname):
    current_date = datetime.datetime.strptime(data['logs'][0]['timestamp'], '%Y-%m-%d %H:%M:%S')
    first_day = str(current_date.year) + str(current_date.month) + str(current_date.day)
    month = {}
    day_list = []
    j = 0
    for i in range(len(data['logs'])):
        current_date = datetime.datetime.strptime(data['logs'][i]['timestamp'], '%Y-%m-%d %H:%M:%S')
        current_day = str(current_date.year) + str(current_date.month) + str(current_date.day)
        if current_day == first_day:
            day_list.append(data['logs'][i])
        else:
            month.update({'day' + str(j + 1): day_list.copy()})
            day_list = []
            day_list.append(data['logs'][i])
            j += 1
            first_day = current_day

    month.update({'day' + str(j + 1): day_list})

    Ndays = len(month.keys())
    correct = np.zeros(Ndays)
    error = np.zeros(Ndays)
    users = np.zeros(Ndays)

    for i in range(1, Ndays+1):
        for j in range (0, len(month['day' + str(i)])):
            correct[i-1] = correct[i-1] + int(month['day'+str(i)][j]['queries']['correct'])
            error[i-1] = error[i-1] + int(month['day'+str(i)][j]['queries']['error'])
            users[i-1] = users[i-1] + int(month['day'+str(i)][j]['users'])

        if error[i-1] > 1000:
            print('Potential outlier at day ' + str(i) + '..!')

    pylab.figure()
    pylab.plot(range(1, Ndays+1), correct, label='correct')
    pylab.plot(range(1, Ndays+1), error, label='error')
    pylab.plot(range(1, Ndays+1), correct + error, label='correct + error')
    pylab.plot(range(1, Ndays+1), users, label='users')
    pylab.legend()
    pylab.savefig(monthname + '_month.png')

    return month




def clean_data(data):
    check = [int(data['logs'][i]['queries']['correct']) + int(data['logs'][i]['queries']['error']) ==
             int(data['logs'][i]['users']) for i in range(len(data['logs']))]
    logs_correct = list(compress(data['logs'], np.asarray(check)==True))
    data['logs'] = logs_correct
    return data

def remove_outliers(data, sigma_times):
    #several_sigma = 100 # rough approx
    #check = [int(data['logs'][i]['queries']['error']) < 10 for i in range(len(data['logs']))]
    relative_error = [float(data['logs'][i]['queries']['error']) / (float(data['logs'][i]['queries']['error']) +
            float(data['logs'][i]['queries']['correct'])) for i in range(len(data['logs']))]
    check = [float(data['logs'][i]['queries']['error']) / (float(data['logs'][i]['queries']['error']) +
            float(data['logs'][i]['queries']['correct'])) < np.mean(relative_error)+sigma_times*np.std(relative_error)
             for i in range(len(data['logs']))]
    logs_correct = list(compress(data['logs'], np.asarray(check)==True))
    data['logs'] = logs_correct
    return data





if __name__=='__main__':

    datapath = './data/session1/query_logs/2018/'

    with open(datapath+'08/2018_08_18452212_log.json','r') as f:
        data_august = json.load(f)

    with open(datapath+'08/2018_08_18452212_summary.json','r') as f:
        summary_august = json.load(f)

    with open(datapath+'09/2018_09_18452212_log.json','r') as f:
        data_september = json.load(f)

    with open(datapath+'09/2018_09_18452212_summary.json','r') as f:
        summary_september = json.load(f)


######  DATA CONDITIONING
## Comment in our out the following lines as per your convenience

    #data_august = clean_data(data_august)
    #data_september = clean_data(data_september)

    #data_august = remove_outliers(data_august, sigma_times=3)
    #data_september = remove_outliers(data_september, sigma_times=3)
##################


    august_users, august_seconds = get_users_seconds(data_august)
    plot_users_in_timeline(august_users, august_seconds, 'August')

    september_users, september_seconds = get_users_seconds(data_september)
    plot_users_in_timeline(september_users, september_seconds, 'September')

    get_month_plot(august_seconds, data_august, 'August')
    get_month_plot(september_seconds, data_september, 'September')

    check_august = [int(data_august['logs'][i]['queries']['correct']) + int(data_august['logs'][i]['queries']['error']) ==
             int(data_august['logs'][i]['users']) for i in range(len(data_august['logs']))]
    august_incorrect = list(compress(data_august['logs'], np.asarray(check_august)==False))
    num_august_incorrect = np.sum(np.asarray(check_august)==False)

    check_september = [int(data_september['logs'][i]['queries']['correct']) + int(data_september['logs'][i]['queries']['error']) ==
             int(data_september['logs'][i]['users']) for i in range(len(data_september['logs']))]
    september_incorrect = list(compress(data_september['logs'], np.asarray(check_september)==False))
    num_september_incorrect = np.sum(np.asarray(check_september)==False)

    get_error_plot(august_seconds, data_august, 'August')
    get_error_plot(september_seconds, data_september, 'September')

    print('this is the end')

