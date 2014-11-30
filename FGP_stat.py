#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import glob
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_pdf import PdfPages


def stat_FG(play_data_dir, team_name_1, out_dir):
    '''
    stat_FG will perform statistics of the FGP (Field Goal Percentage) of some team
    play_data_dir <- could be the play-by-play data directory, such as 'Desktop/play_data/2006-2007.regular_season'
    team_name_1 <- should be the abbreviation name of the team you want to check
    out_dir <- the output directory
    '''
    os.chdir(play_data_dir)
    all_plays_team_1 = glob.glob('*' + team_name_1 + '*.csv')
    all_plays_team_1 = sorted(all_plays_team_1)
    pp = PdfPages(out_dir + '/' + team_name_1 + '.pdf')
    for each_game in all_plays_team_1:
        (date, teams, extention) = each_game.split('.') #get the date and team names of some game
        with open (each_game, mode='r') as ori_data:
            lines = ori_data.readlines()[1:]

        if teams[0:3] == team_name_1:
            team_name_2 = teams[3:6]
        else:
            team_name_2 = teams[0:3] #get the name of team 2

        team_1_FG = open(out_dir + '/' + date + '_' + team_name_1 + '_FG', mode='w')
        team_2_FG = open(out_dir + '/' + date + '_' + team_name_2 + '_FG', mode='w')
        team_1_shot_total_no = 0
        team_2_shot_total_no = 0
        team_1_shot_made_no = 0
        team_2_shot_made_no = 0
        team_1_shot_stat = []
        team_2_shot_stat = []
        for each_line in lines:
            s = []
            s = each_line.split(',')
            if s[13] == 'shot' :
                if s[12] == team_name_1:
                    if s[27] == 'made':
                        team_1_shot_made_no += 1
                    team_1_shot_total_no += 1
                    team_1_shot_made_percent = (team_1_shot_made_no / team_1_shot_total_no) * 100
                    team_1_shot_stat.append(team_1_shot_made_percent)
                    team_1_FG.write(str(team_1_shot_made_no) + '\t' + str(team_1_shot_total_no) + '\t' + str(team_1_shot_made_percent) + '%' + '\n')
                else:
                    if s[27] == 'made':
                        team_2_shot_made_no += 1
                    team_2_shot_total_no += 1
                    team_2_shot_made_percent = (team_2_shot_made_no / team_2_shot_total_no) * 100
                    team_2_FG.write(str(team_2_shot_made_no) + '\t' + str(team_2_shot_total_no) + '\t' + str(team_2_shot_made_percent) + '%' + '\n')
                    team_2_shot_stat.append(team_2_shot_made_percent)
            else:
                pass
        plt.figure() #if no this step, accident will happen
        plt.xlabel('shot_time')
        plt.ylabel('Probability')
        plt.title(date + '_' + team_name_1 + '_vs_' + team_name_2)
        team1 = plt.plot(range(1, team_1_shot_total_no + 1), team_1_shot_stat, 'r--o', label=team_name_1)
        team2 = plt.plot(range(1, team_2_shot_total_no + 1), team_2_shot_stat, 'b^-', label=team_name_2)
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=1, ncol=2, mode="expand", borderaxespad=0.)
        pp.savefig()
        team_1_FG.close()
        team_2_FG.close()
    pp.close()

def main():
    play_data_dir = 'second_spectrum/2006-2007.regular_season'
    team_name_1 = 'CHI'
    out_dir = '/home/yang/Desktop/Second_sp'
    test_1 = stat_FG(play_data_dir, team_name_1, out_dir)

main()
