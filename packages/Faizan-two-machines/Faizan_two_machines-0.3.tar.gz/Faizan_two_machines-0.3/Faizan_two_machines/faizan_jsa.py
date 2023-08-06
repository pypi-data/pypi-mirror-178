from tabulate import tabulate
import warnings
warnings.filterwarnings('ignore')
class Faizan:
    def faizan_two_machine(self, df):
        c1 = df.copy()
        df.rename(columns={df.columns[0]: 'Job', df.columns[1]: 'Time_machine1', df.columns[2]: 'Time_machine2'},
                  inplace=True)
        l1 = []  # list for machine 1
        l2 = []  # list for machine 2
        t1 = list(df["Time_machine1"].values)
        t2 = list(df["Time_machine2"].values)
        letter2 = []
        letter1 = []
        while True:
            x = min(t1 + t2)
            # print(x)
            if x in t2:
                ind = t2.index(x)
                letter2.append(list(df[df["Time_machine2"] == x]['Job'])[0])
                df = df[df['Job'] !=list(df[df["Time_machine2"] == x]['Job'])[0]]
                l2.append(x)
            elif x in t1:
                ind = t1.index(x)
                letter1.append(list(df[df["Time_machine1"] == x]['Job'])[0])
                df = df[df['Job'] != list(df[df["Time_machine1"] == x]['Job'])[0]]
                l1.append(x)
            t1.pop(ind)
            t2.pop(ind)
            if len(t1) == 0:
                break
        letter2.reverse()  # since smallest jobs first, this must be reversed
        l2.reverse()
        print(f"Sequence : {letter1 + letter2}")
        letter_final = letter1 + letter2
        df = c1
        # For machine 1 execution
        class create_dict(dict):
            def __init__(self):
                self = dict()

            def add(self, key, value):
                self[key] = value

        dict2 = create_dict()
        for i in range(len(df)):
            dict2.add(i, letter_final[i])
        df['Start_time_Machine1'] = 0
        df['End_Time_Machine1'] = 0
        df_new_order = df[['Start_time_Machine1', 'End_Time_Machine1']]
        time = 0
        counter = 0
        n = len(letter1 + letter2)
        while (counter < n):
            df_new_order['Start_time_Machine1'][counter] = time;
            time += list(df[df['Job'] == dict2[counter]].Time_machine1)[0]
            df_new_order['End_Time_Machine1'][counter] = time;
            counter += 1
        i = len(df)
        df_new_order['Process'] = ""
        for i in range(i):
            df_new_order['Process'][i] = dict2[i]
        df_new_order = df_new_order[["Process", "Start_time_Machine1", "End_Time_Machine1"]]

        # For machine 2 execution
        df_new_order['Start_time_Machine2'] = 0
        df_new_order['End_Time_Machine2'] = 0
        counter = 0
        time = 0
        # For first job, as soon as it is done with machine 1, it will go to machine 2 so hard fill it
        df_new_order['Start_time_Machine2'][0] = df_new_order['End_Time_Machine1'][0]
        df_new_order['End_Time_Machine2'][0] = df_new_order['Start_time_Machine2'][0] + list(
            df[df_new_order["Process"][0] == df["Job"]]["Time_machine2"])
        for i in range(1, len(df)):
            df_new_order['Start_time_Machine2'][i] = max(df_new_order['End_Time_Machine2'][i - 1],
                                                         df_new_order['End_Time_Machine1'][i])
            df_new_order['End_Time_Machine2'][i] = df_new_order['Start_time_Machine2'][i] + list(
                df[df_new_order["Process"][i] == df["Job"]]["Time_machine2"])
        total_idle_time_machine2 = 0
        for i in range(1, len(df_new_order)):
            total_idle_time_machine2 = total_idle_time_machine2 + (
                        df_new_order['Start_time_Machine2'][i] - df_new_order["End_Time_Machine2"][i - 1])
        total_idle_time_machine2 += df_new_order['Start_time_Machine2'][
            0]  # first iteration when machine 1 executes, machine 2 is idle
        total_idle_time_machine1 = df_new_order['End_Time_Machine2'][len(df_new_order) - 1] - \
                                   df_new_order['Start_time_Machine2'][len(df_new_order) - 1]
        Total__Execution_Time = df_new_order['End_Time_Machine2'][len(df_new_order) - 1]
        print(f"Total_Execution_Time is : {Total__Execution_Time}")
        print(f"Total_Idle_Time for machine 1 is : {total_idle_time_machine1}")
        print(f"Total_Idle_Time for machine 2 is : {total_idle_time_machine2}")
        print(tabulate((df_new_order), headers='keys', tablefmt='psql'))
