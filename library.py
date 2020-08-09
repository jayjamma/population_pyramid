import os.path 
import requests
import csv
import matplotlib.pyplot as plt

country_index = { 

  "World"    : 900,     #0
  "India"    : 356,     #1
  "China"    : 156,     #2
  "Japan"    : 392,     #3
  "Nigeria"  : 566,     #4
  "Brazil"   : 76,      #5
  "Bolivia"  : 68,      #6
  "Ghana"    : 288,     #7
  "Pakistan" : 586,     #8
  "Mexico"   : 484,     #9
  "Germany" : 276,      #10
  "Italy"    : 380,     #11
  "United States" : 840, #12
  "Latvia" : 428, #13
}
 
csv_path = "CSV"

def download_data(country_name,year):
    headers = requests.utils.default_headers()
    headers.update({'User-agent': 'Mozilla/5.0'})

    if country_name in country_index.keys(): 
       country_code = country_index[country_name]
    else:
       print("Country code is not available for #{country_code}\n")
       return
       
    filename =  os.path.join(csv_path,"{0}-{1}.csv".format(country_name,year))

    print("Downloading for: {} year {}".format(country_name,year),end='')
    url = "https://www.populationpyramid.net/api/pp/{0}/{1}/?csv=true".format(country_code,year)

    response = requests.get(url, headers=headers)

    data =response.content 

    file = open(filename, "wb")
    file.write(data)
    print(" {} bytes".format(len(data)))

def prepare_data(country_name,year):

    filename =  os.path.join(csv_path,"{0}-{1}.csv".format(country_name,year))

    file = open(filename, "rt")

    age = []
    male = []
    female = []

    total = 0

    csv_reader = csv.reader(file)
    count = 0
    for row in csv_reader:
        count = count+1
        if count == 1:
            continue
            
        age.append(row[0])
        m = int(row[1])
        f = int(row[2])
        total = total + (m + f) 
        male.append(m) 
        female.append(f)

    pop = total/(1000*1000)
    sex_r = int(1000*(sum(female)/(sum(male))))

    dep_age_grps = [ '0-4', '5-9', '10-14', '15-19',
        '60-64', '65-69', '70-74', '75-79','80-84','85-89','90-94','95-99','100+'  ] 
    
    non_dep_total = 0     

    dep_total = 0

    for (a,m,f) in zip(age,male,female):
        if a in dep_age_grps:
            #print("Dep Age: {} Male {} female {}".format(a,m,f))
            dep_total = dep_total + (m + f)
        else:
            #print("Non-Dep Age: {} Male {} female {}".format(a,m,f))
            non_dep_total = non_dep_total + (m + f)            

    dep_r = dep_total/non_dep_total*100

    count = len(male)
    for x in range(count):
        male[x] = male[x]*100*-1/total
        female[x] = female[x]*100/total


    dep = 0

    stats = { 
        "age"        : age,
        "male"       : male, 
        "female"     : female, 
        "population" : pop, 
        "sex_ratio"  : sex_r,
        "dependent_ratio" : dep_r 
    }

    return stats

def first_plot(stats,country_name,year):

    max_x = 16

    age    = stats['age']
    male   = stats['male']
    female = stats['female']
    sex_r  = stats['sex_ratio']
    pop    = stats['population']
    dep_r  = stats['dependent_ratio']

    fig1 = plt.figure()
    ax = fig1.add_subplot(111)
    plot_m = ax.barh(age,male, color = "steelblue")
    plot_f = ax.barh(age,female, color = "#EE7989")

    text_male = []
    text_female = []
    text_titles = []

    count = len(male)
    for x in range(count):
        text_male.append(ax.text(round(male[x]-2,1), x, "{0:0.1f}%".format(abs(male[x]))))
        text_female.append(ax.text(round(female[x]+.25,1), x, "{0:0.1f}%".format(abs(female[x]))))

    plt.xticks(range(-1*max_x, max_x,2))

    text_titles.append(ax.text(max_x-8,count-2,"{}".format(year),fontsize=18))
    text_titles.append(ax.text(-1*max_x+1,count-4,"Population: {0:0.0f} million".format(pop)))
    text_titles.append(ax.text(-1*max_x+1,count-5,"Sex Ratio: 1000:{0:3d} ".format(sex_r)))
    text_titles.append(ax.text(-1*max_x+1,count-6,"Dep. Ratio: {0:0.2f} ".format(dep_r)))
    text_titles.append(ax.text(-1*max_x+1,count-2,"{}".format(country_name),fontsize=18))

    all_text = [ text_male, text_female, text_titles ]

    return [ fig1, ax, plot_m, plot_f, all_text ]


