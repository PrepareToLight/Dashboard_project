"""
names, DOBs, age, gender, marital status, date of hire, reasons for termination, department, 
whether they are active or terminated, position title, pay rate, manager name, and performance score.

Recent additions to the data include:

Absences
Most Recent Performance Review Date
Employee Engagement Score
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

WIDTH, HEIGHT = 12, 10
AVG_WORK_YEAR = 248
CURRENT_YEAR = 2018
_FORMAT = "png"
FONTSIZE = 30
TITLE_HEIGHT = 1.05


"""
HRtable contaions:
                "Employee_Name","Salary",
                "Position","Department","DateofHire","Termd","DateofTermination",
                "TermReason","EmploymentStatus",
                "ManagerName","RecruitmentSource","EmpSatisfaction",
                "DaysLateLast30","Absences"
"""
def main():
    df = pd.read_csv("./HRtable.csv")
    """
    Below function is responsible for
    creation of every plot in years window
    """
    #years_plots(df=df)
    #pie_month_plots(df)
    plot_dep_headcount_now(df)

def plot_dep_headcount_now(df):
    #print(df[["DateofTermination","Termd"]].head(30))
    df_present = df[df["Termd"] == 0]
    #print(df_present.shape)
    #print(df_present[df["Department"] == "Admin Offices"])
    df_grouped_dep = df_present.groupby("Department").count()
    #print(df_grouped_dep["Employee_Name"])
    """
    Department
    Admin Offices             7
    Executive Office          1
    IT/IS                    40
    Production              126
    Sales                    26
    Software Engineering      7
    """
    categories = ["Admin Offices", "Executive Office", "IT/IS", "Production","Sales", "Software-Eng"]
    values = [7,1,40,126,26,7]
    fig, ax = plt.subplots(figsize = (WIDTH,HEIGHT))
    # Create horizontal bar chart
    colors = ["black","red", 'orange','pink', 'blue', "chartreuse"]
    ax.barh(categories, values, color=colors)

    # Add labels and title
    #ax.set_xlabel('Values')
    #ax.set_ylabel('Categories')
    ax.set_title('Headcount by Department', fontsize=FONTSIZE, y=TITLE_HEIGHT)

    for i, value in enumerate(values):
        plt.text(value, i, str(value), va='center')

    plt.savefig("headcount_by_dep_now."+_FORMAT, format=_FORMAT)
    # Show the chart
    plt.show()
    
    
def pie_month_plots(df):
    df_lates = df[["Department","DaysLateLast30"]][df["DaysLateLast30"] > 0]
    #print(df_lates)
    #print(df_lates)
    
    df_sum_lates = df_lates.groupby("Department").sum()
    #print(df_sum_lates)
    """                     DaysLateLast30
    Department
    
    IT/IS                              7
    Production                        98
    Sales                             20
    Software Engineering               4
    """
    x_lates = ["IT/IS","Production","Sales","Software Engineering"]
    y_lates = list(df_sum_lates["DaysLateLast30"].to_numpy())
    
    colors = ['#ffcc99','#ff9999','#66b3ff','#99ff99','#666666']
    explode = (0.05,0.05,0.05,0.05)

    fig1, ax1 = plt.subplots(figsize=(WIDTH,HEIGHT))
    ax1.pie(y_lates, colors = colors, labels=x_lates, autopct='%1.1f%%', startangle=10, pctdistance=0.85, explode = explode)

    #draw circle
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    # Equal aspect ratio ensures that pie is drawn as a circle
    ax1.axis('equal')  
    ax1.set_title("Days Late Last 30", fontsize=FONTSIZE, y=TITLE_HEIGHT)
    plt.savefig("DaysLateLast30."+_FORMAT, format=_FORMAT)
    plt.tight_layout()
    plt.show()


def years_plots(df):
    df_rotation = df[["DateofHire","DateofTermination","Termd","Absences"]]
    doh, MIN_HIRE_YEAR, MAX_HIRE_YEAR = date_to_vectors_MINandMAX(df_rotation, "DateofHire")
    #print(dof)
    dof, MIN_FIRE_YEAR, MAX_FIRE_YEAR = date_to_vectors_MINandMAX(df_rotation,"DateofTermination")
    #print(doh)
    #print(f" MIN_HIRE_YEAR = {MIN_HIRE_YEAR}\n",
    #      f"MAX_HIRE_YEAR = {MAX_HIRE_YEAR}\n",
    #      f"MIN_FIRE_YEAR = {MIN_FIRE_YEAR}\n",
    #      f"MAX_FIRE_YEAR = {MAX_FIRE_YEAR}\n")
    
    #UNCCOMENT THIS!
    plot_array_count(doh, dof, MIN_HIRE_YEAR, MAX_HIRE_YEAR, MIN_FIRE_YEAR, MAX_FIRE_YEAR)
    
    #UNCCOMENT THIS!
    hist_hire_fire(doh, dof, MIN_HIRE_YEAR, MAX_HIRE_YEAR)

    pie_chart_work_absc(df_rotation)

def pie_chart_work_absc(df):
    # plot of ratio days worked vs absencess
    #format DD MM YY (of hire) DD MM YY (of fire)
    # (0,0,0) means end of 2018, counted as 365
    # avrg working year in poland = 248
    #print(dohf[:30])
    doh, MIN_HIRE_YEAR, MAX_HIRE_YEAR = date_to_vectors_MINandMAX(df, "DateofHire")
    #print(dof)
    dof, MIN_FIRE_YEAR, MAX_FIRE_YEAR = date_to_vectors_MINandMAX(df,"DateofTermination")
    #number of days worked by each employee
    #print(dohf[50])
    #print(count_work_days_start(doh[50],dof[50]))
    worked_days_employees = np.array([count_work_days_start(doh[i],dof[i]) for i in range(doh.shape[0])])
    worked_days_employees_sum = worked_days_employees.sum()
    #print(worked_days_employees_sum)
    absences_employees_sum = df["Absences"].sum()
    #print(df_rotation["Absences"].sum())
    labels = ["Worked days", "Absences"]
    sizes = [worked_days_employees_sum,absences_employees_sum]
    colors = ['#99ff99','#ff9999']
    explode = [0, 0.2]
    fig1, ax1 = plt.subplots(figsize=(WIDTH,HEIGHT))
    ax1.pie(sizes, colors = colors, labels=labels, autopct='%1.1f%%', startangle=25, pctdistance=0.85, explode = explode)
    #draw circle
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    # Equal aspect ratio ensures that pie is drawn as a circle
    ax1.axis('equal')  
    ax1.set_title("Working days and total absences",fontsize=FONTSIZE, y=TITLE_HEIGHT)
    plt.tight_layout()
    plt.savefig("worked_absences_piechart_years."+_FORMAT, format=_FORMAT)
    plt.show()

def count_work_days_start(arr_start,arr_end):
    month_day = {1:31,2:28,3:31,4:30,5:31,6:30,
                 7:31,8:31,9:30,10:31,11:30,12:31}#sum_val = 365
    month_day_arr = np.array([31,28,31,30,31,30,
                          31,31,30,31,30,31])
    days = month_day[arr_start[1]] - arr_start[0]
    #print(days)
    days_months = month_day_arr[arr_start[1]::].sum()
    #print(days_months)
    length = arr_end[2] - arr_start[2]
    if length < 0:
        years = CURRENT_YEAR - arr_start[2]
        days_years = 248*years
    elif length > 1:
        days_years = 248*length
    else:
        days_years = 0

    #print(days_years)
    #count days for last work year
    if length == 1:
        days_end = arr_end[0]
        days_months_end = month_day_arr[0:arr_end[1]-1].sum()
    else:
        days_end = 0
        days_months_end = 0

    return days + days_months + days_years + days_end + days_months_end



def hist_headcount(hx1, hy1, tx2, ty2, MIN_HIRE_YEAR, MAX_HIRE_YEAR):
    #print(hx1, '\n', hy1, '\n', tx2, '\n', ty2)
    y = np.zeros(13)
    y[0:4] = hy1[0:4]
    y[4::] = hy1[4::] - ty2
    y = np.array([y[0:i+1].sum() for i in range(hx1.shape[0])])
    #print(y)
    fig, ax = plt.subplots(figsize=(WIDTH,HEIGHT))
    bars = ax.bar(hx1, y)
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height,
                f'{int(height)}', ha='center', va='bottom')
    ax.set_xticks(np.arange(MIN_HIRE_YEAR, MAX_HIRE_YEAR+1, 1))
    ax.set_xticklabels(np.arange(MIN_HIRE_YEAR, MAX_HIRE_YEAR+1, 1))
    plt.xticks(rotation=90)
    ax.set_title("Headcount of Employees per year",fontsize=FONTSIZE, y=TITLE_HEIGHT)
    plt.savefig("headcount_barplot_years.png", format="png")
    plt.show()

def hist_hire_fire(doh, dof, MIN_HIRE_YEAR, MAX_HIRE_YEAR):
    fig, ax = plt.subplots(figsize=(WIDTH, HEIGHT))
    #ax.hist(doh[:,2])
    #ax.hist(dof[:,2][dof[:,2] > 0], color="red",alpha=.5)
    """
    how to create such histogram
    https://stackoverflow.com/questions/6871201/plot-two-histograms-on-single-chart-with-matplotlib
    
    plt.style.use('seaborn-deep')

    x = np.random.normal(1, 2, 5000)
    y = np.random.normal(-1, 3, 2000)
    bins = np.linspace(-10, 10, 30)

    plt.hist([x, y], bins, label=['x', 'y'])
    plt.legend(loc='upper right')
    plt.show()
    """
    counts, ages, bars = ax.hist([ 
                                 doh[:,2], dof[:,2][dof[:,2] > 0]],
                                 bins=np.arange(MIN_HIRE_YEAR, MAX_HIRE_YEAR+2,1),
                                 label=["Number of new hires","Number of terminations"
                                ])
    ax.set_xticks(np.arange(MIN_HIRE_YEAR, MAX_HIRE_YEAR+2, 1))
    ax.set_xticklabels(np.arange(MIN_HIRE_YEAR, MAX_HIRE_YEAR+2, 1))
    plt.xticks(rotation=90)
    #let's take a note that bars contains values we extracted eralier
    #in count_hf_by_year() function
    [ax.bar_label(bar) for bar in bars]
    ax.legend()
    ax.set_title("Hirings and Terminations count",fontsize=FONTSIZE,y=TITLE_HEIGHT)
    plt.savefig("hist_sidebside.png", format="png")
    plt.show()

def plot_array_count(doh, dof, MIN_HIRE_YEAR, MAX_HIRE_YEAR, MIN_FIRE_YEAR, MAX_FIRE_YEAR):
    hcount = count_hf_by_year(doh, MIN_HIRE_YEAR, MAX_HIRE_YEAR)
    fcount = count_hf_by_year(dof, MIN_FIRE_YEAR, MAX_FIRE_YEAR)
    x1, x2 = hcount[:,0], fcount[:,0]
    y1, y2 = hcount[:,1], fcount[:,1]
    #print(x1, '\n', x2)
    #print(y1, '\n', y2)
    fig, ax = plt.subplots(figsize=(WIDTH, HEIGHT))
    haired_line, = ax.plot(y1,x1)
    fired_line, = ax.plot(y2,x2,color="orange")
    ax.axvline(x=2015.619, color='red', linestyle='--')
    haired_line.set_label("Hirings")
    fired_line.set_label("Terminations")
    ax.legend()
    ax.set_title("Hirings and Terminations Plot",fontsize=FONTSIZE,y=TITLE_HEIGHT)
    plt.savefig("hiring_termination_ratio_plot.png", format="png")
    plt.show()
    #headcount plot
    hist_headcount(y1, x1, y2, x2, MIN_HIRE_YEAR, MAX_HIRE_YEAR)
    # 1 - hirings, 2 - terminations
    return (y1, x1, y2, x2)

#count hired or fired by year
def count_hf_by_year(array, min, max):
    array_count = np.array([[array[array == year].shape[0], year] for year in range(min,max+1)])
    return array_count

def date_to_int(_str):
    try:
        splited_lst = _str.split('/')
        month = int(splited_lst[0])
        day = int(splited_lst[1])
        year = int(splited_lst[2])
        return (day,month,year)
    except Exception as err:
        #print(err)
        #print(_str)
        return (0,0,0)
    
def date_to_vectors_MINandMAX(df, _str):
    #dohf = [df.loc[i].to_numpy() for i in range(df.shape[0])] #this save whole row
    """
    dohf - date of hire or faired
    """
    dohf = df[_str].to_numpy()
    dohf = np.vectorize(date_to_int)(dohf)
    #print(dohf)
    """
    dohf format :=: dd/mm/yy
    """
    MIN_YEAR = dohf[2][dohf[2] > 0].min()
    MAX_YEAR = dohf[2][dohf[2] > 0].max()
    dohf = np.array([np.array([dohf[0][i],dohf[1][i],dohf[2][i]]) for i in range(df.shape[0])])
    return (dohf,MIN_YEAR,MAX_YEAR)

def df_loads():
    df = pd.read_csv("./HRDataset_v14.csv")
    #[print(df[name].head()) for name in df.columns]
    df_new = df[["Employee_Name","Salary",
                "Position","Department","DateofHire","Termd","DateofTermination",
                "TermReason","EmploymentStatus",
                "ManagerName","RecruitmentSource","EmpSatisfaction",
                "DaysLateLast30","Absences"]]
    df_new.to_csv("HRtable.csv", index=False)

if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        df_loads()
        main()