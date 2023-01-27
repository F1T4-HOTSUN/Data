import time
import re

import pandas as pd

from hol_api_caller import *


class Session:
    def __init__(self):
        self.day = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
        self.ab_data = ['W-MON', 'W-TUE', 'W-WED', 'W-THU', 'W-FRI', 'W-SAT', 'W-SUN']

    def session_data(self, prf_id, dtguidance, prf_start_date, prf_end_date, hol_list):
        data = []
        prf_hol_list = []

        hol_flag = False

        if 'HOL' in dtguidance:
            hol_flag = True

        # ['토요일 ~ 일요일(13:00,15:00)', 'HOL(11:00,14:00,16:00)']
        sp = dtguidance.split(', ')

        hol_idx = [i for i in range(len(sp)) if 'HOL' in sp[i]]

        if len(hol_idx) == 1:
            hol_pop = sp.pop(hol_idx[0]).replace(')', '')
            hol_pop_list = re.split('[(,]', hol_pop)

        for i in sp:
            i = i.replace(')', '')
            # ['토요일 ~ 일요일', '13:00', '15:00']
            # ['HOL', '11:00', '14:00', '16:00']
            sp_time = re.split('[(,]', i)
            if '~' not in sp_time[0] and sp_time[0] != 'HOL':
                idx = self.day.index(sp_time[0])
                self.add_session(sp_time, prf_start_date, prf_end_date, idx, hol_flag, hol_list, prf_hol_list, prf_id,
                                 data)
            elif '~' in sp_time[0]:
                sp_tilde = sp_time[0].split(' ~ ')
                start_idx = self.day.index(sp_tilde[0])
                cnt = start_idx
                for idx in range(start_idx, start_idx + 7):
                    self.add_session(sp_time, prf_start_date, prf_end_date, cnt, hol_flag, hol_list, prf_hol_list,
                                     prf_id,
                                     data)
                    if self.day[cnt] == sp_tilde[1]:
                        break
                    cnt += 1
                    cnt = cnt % 7

        start_date = time.strptime(prf_start_date, '%Y-%m-%d')
        end_date = time.strptime(prf_end_date, '%Y-%m-%d')

        if hol_flag:
            for h in hol_list:
                if start_date <= time.strptime(h, '%Y-%m-%d') <= end_date:
                    prf_hol_list.append(h)

            for hol_idx in range(1, len(hol_pop_list)):
                for holiday in prf_hol_list:
                    date_time = {
                        'performance_id': prf_id,
                        'prf_session_date': holiday,
                        'prf_session_time': hol_pop_list[hol_idx],
                        'remaining_seat': 200,
                        'total_seat': 200
                    }
                    data.append(date_time)
        return data

    def add_session(self, sp_time, prf_start_date, prf_end_date, idx, hol_flag, hol_list, prf_hol_list, prf_id, data):
        for j in range(1, len(sp_time)):
            day = pd.date_range(prf_start_date, prf_end_date, freq=self.ab_data[idx]).format(
                formatter=lambda x: x.strftime('%Y-%m-%d'))
            for k in day:
                if hol_flag and k in hol_list:
                    prf_hol_list.append(k)
                    continue
                date_time = {
                    'performance_id': prf_id,
                    'prf_session_date': k,
                    'prf_session_time': sp_time[j],
                    'remaining_seat': 200,
                    'total_seat': 200
                }
                data.append(date_time)
