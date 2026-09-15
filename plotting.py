import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from PIL import Image, ImageDraw, ImageFont
import json
import glob
import os
from datetime import datetime

def plothours(totals, totalhours, sickintervals, filepath, name):
    totals = totals[::-1]
    xs = [x for x in range(len(totals))]
    plt.plot(xs, totals)
    totalhoursmean = totals.copy()
    for i in range(len(sickintervals)):
        plt.axvspan(sickintervals[i][0], sickintervals[i][1] - 1, ymin=0.048, ymax=0.98, alpha=0.3, color='tab:gray')
        totalhoursmean[sickintervals[i][0] - 1 : sickintervals[i][1]] = totals[sickintervals[i][0] - 1], totals[sickintervals[i][1] - 1]
        antall_dager_syk = sickintervals[i][1] - 1 - sickintervals[i][0] + 1
    if len(sickintervals) != 0 and sickintervals[-1][-1] == len(totals) - 1:
        del totalhoursmean[-1]
    plt.xlabel('dager')
    plt.ylabel('timer')
    plt.title(f'antall timer studert i løpet av {len(totals)} dager, {name}')
    plt.grid(axis = 'y',zorder = 0,linestyle=':')
    if len(sickintervals) == 0:
        custom_legend = [Line2D([0], [0], color='tab:blue', lw=3), Line2D([0], [0], color='tab:blue', lw=3)]
        plt.legend(custom_legend, [f'totalt= {np.round(totalhours,2)}h', f'gjennomsnitt = {np.round(np.mean(totals),2)}h'])
    else:
        custom_legend = [Line2D([0], [0], color='tab:blue', lw=3), Line2D([0], [0], color='tab:blue', lw=3), Line2D([0], [0], color='tab:gray', lw=3)]
        plt.legend(custom_legend, [f'totalt= {np.round(totalhours,2)}h', f'gj.snitt, u/syk = {np.round(np.mean(totalhoursmean),2)}h', f"syk {antall_dager_syk} dager"])
    plt.savefig(f'timer{name}.png')
    plt.close()

def plotbarchart(totals, totalsweekdays, sickintervals, weekdays, name):
    weekdaysavg = np.zeros(7)
    weekdaysmodified = weekdays.copy()
    for sickinterval in sickintervals:
        intervallength = sickinterval[1] - sickinterval[0]
        numberofweeks = intervallength // 7
        extradays = intervallength % 7
        weekdaysmodified -= numberofweeks
        for daynumber in range(sickinterval[2], sickinterval[2] + extradays):
            day = daynumber % 7
            weekdaysmodified[day] -= 1

    for day in range(0,7):
        weekdaysavg[day] = totalsweekdays[day] / weekdaysmodified[day]

    plt.bar(['mandag','tirsdag','onsdag','torsdag','fredag','lørdag','søndag'], weekdaysavg, edgecolor = 'black', color='pink', label = 'antall timer')
    plt.xlabel('ukedager')
    plt.ylabel('timer')
    plt.title(f'antall timer studert per ukedag i løpet av {len(totals)} dager, {name}')
    plt.grid(axis = 'y', zorder = 0, linestyle=':')
    plt.legend()
    plt.savefig(f'ukedager{name}.png')
    plt.close()

def plotstackedbarchart(totals, hoursindextype, totalshourindextype, courses, name):
    colours = ['mediumslateblue', 'slateblue', 'mediumpurple', 'blueviolet']
    bottom = 0
    for i in range (len(totalshourindextype)):
        plt.bar(courses, totalshourindextype[i], bottom = bottom, edgecolor = 'black', color=colours[i], label = hoursindextype[i])
        bottom += totalshourindextype[i]
    plt.xlabel('fag')
    plt.ylabel('timer')
    plt.title(f'fordeling av tidsbruk per fag på {len(totals)} dager, {name}')
    plt.grid(axis = 'y', zorder = 0, linestyle=':')
    plt.legend()
    plt.savefig(f'fordeling{name}.png')
    plt.close()

def plotwriting(totalscourses, numberofcourses, courses, filepath, name):
    spacing = 50
    height = spacing * (numberofcourses + 1) + 15
    image = Image.new("RGB", (512, height), "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", size=25)
    placement = 15
    draw.text((15, placement), f"TIMER JOBBET PER FAG {name}", font=font, fill=(0, 0, 0))
    placement += spacing
    for i in range(numberofcourses):
        draw.text((15, placement), f"antall timer brukt på {courses[i]}: {np.round(totalscourses[i], 1)}", font=font, fill=(0, 0, 0))
        placement += spacing
    image.save(f'fag{name}.png')

def sick(totalswithday):
    totalswithday = totalswithday[::-1]
    sickintervals = []
    j = -1
    for i in range(len(totalswithday)):
        if totalswithday[i][0] == 0.0 and i > j:
            sick = True
            j = i
            while sick == True and i < len(totalswithday) and j < len(totalswithday):
                if j < len(totalswithday) - 1 and totalswithday[j+1][0] != 0.0:
                    sick = False
                elif j == len(totalswithday) -1 and totalswithday[j][0] == 0.0:
                    sick = False
                j = j + 1
            # Dersom du har vært syk i mer enn 3 dager (altså 0h i mer enn 3 dager)
            if j-i > 3:
                sickintervals.append((i, j, int(totalswithday[i][1])))
        else:
            sick = False
    return sickintervals

def gettitlename(filepath, month = None):
    filename = filepath.split('\\')[1]
    semestername = filename.split('.')[0]
    year = semestername[len(semestername) -2 :]
    imagename = semestername[0]
    imagename += year
    if month or month == 0:
        monthdatetime = datetime.strptime(str(month + 1), "%m")
        monthname = datetime.strftime(monthdatetime, "%b")
        imagename += monthname
    return imagename.upper()

def monthobject(numberofcourses):
    monthtotals = []
    for _ in range(0, 12):
        monthtotals.append({'totalswithday': [], 'totalsweekdays': np.zeros(7),
                            'weekdays': np.zeros(7), 'totalshoursindextype': np.zeros((4, numberofcourses)),
                            'totalscourses': np.zeros(numberofcourses)})
    return monthtotals

def plotall(totalswithday, totalsweekdays, weekdays, hoursindextype, totalshourindextype,
            totalscourses, courses, numberofcourses, filepath, name):
    totalswithday = np.array(totalswithday)
    totals = list(totalswithday[:,0])
    totalswithday = list(totalswithday)
    totalhours = np.sum(totals)
    sickintervals = sick(totalswithday)
    plothours(totals, totalhours, sickintervals, filepath, name)
    plotbarchart(totals, totalsweekdays, sickintervals, weekdays, name)
    plotstackedbarchart(totals, hoursindextype, totalshourindextype, courses, name)
    plotwriting(totalscourses, numberofcourses, courses, filepath, name)

def make_images():
    files = list(filter(os.path.isfile, glob.glob('*.json')))
    files.sort(key = lambda x:os.path.getmtime(x))
    filepath = files[-1]
    name = gettitlename(filepath)

    totalswithday = []

    with open(filepath, 'r', encoding = 'utf-8') as f:
        data = json.load(f)
        firstelem = data[list(data.keys())[0]]
        courses = list(firstelem.keys())
        numberofcourses = len(courses) - 1
        totalscourses = np.zeros(numberofcourses)
        totalsweekdays = np.zeros(7)
        weekdays = np.zeros(7)
        totalshourindextype = np.zeros((4, numberofcourses))
        hoursindextype = list(list(firstelem[list(firstelem.keys())[1]].keys()))
        monthtotals = monthobject(numberofcourses)
        del hoursindextype[-1]
        del courses[0]
        for key, date in data.items():
            totaldate = 0
            counter = 0
            weekday = date['weekday']
            month = key.split(" ")[0]
            monthdatetime = datetime.strptime(month, "%b")
            monthnumber = monthdatetime.month - 1
            for course in date.keys():
                if course == 'weekday':
                    continue
                time = date[course]['Total']
                totaldate += time
                totalscourses[counter] += time
                monthtotals[monthnumber]['totalscourses'][counter] += time
                for typeindex, type in enumerate(date[course]):
                    if type == 'Total':
                        continue
                    totalshourindextype[typeindex][counter] += date[course][list(date[course].keys())[typeindex]]
                    monthtotals[monthnumber]['totalshoursindextype'][typeindex][counter] += date[course][list(date[course].keys())[typeindex]]
                counter += 1
            totalswithday.append((totaldate, weekday))
            totalsweekdays[weekday] += totaldate
            weekdays[weekday] += 1
            monthtotals[monthnumber]['totalswithday'].append((totaldate, weekday))
            monthtotals[monthnumber]['totalsweekdays'][weekday] += totaldate
            monthtotals[monthnumber]['weekdays'][weekday] += 1

    plotall(totalswithday, totalsweekdays, weekdays, hoursindextype, totalshourindextype,
            totalscourses, courses, numberofcourses, filepath, name)

    for monthnumber, month in enumerate(monthtotals):
        name = gettitlename(filepath, monthnumber)
        if len(month['totalswithday']) == 0:
            continue
        totalswithday = month['totalswithday']
        totalsweekdays = month['totalsweekdays']
        weekdays = month['weekdays']
        totalscourses = month['totalscourses']
        totalshourindextype = month['totalshoursindextype']

        plotall(totalswithday, totalsweekdays, weekdays, hoursindextype, totalshourindextype,
                totalscourses, courses, numberofcourses, filepath, name)