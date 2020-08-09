import matplotlib.animation as animation
from library import *

countries = list(country_index.keys())

country_name = countries[13]

start_year = 1950
end_year   = 2100

video_enable = False

def update_plot(num, plot):

    fig1, ax, plot_m, plot_f, all_text = plot 
    year = start_year + num 
    print(year)

    stats = {}
    try:
        stats = prepare_data(country_name,year) 
    except Exception as error:
        print(">> Error occured: {}".format(error))
        return plot_m,plot_f

    male = stats['male']
    female = stats['female'] 

    for rect, y in zip(plot_m, male):
        rect.set_width(round(y,2))

    for rect, y in zip(plot_f, female):
        rect.set_width(round(y,2))

    text_male, text_female, text_titles = all_text
    for x, txt in enumerate(text_male):
        txt.set_position((round(male[x]-2.25,1), x))
        txt.set_text("{0:0.1f}%".format(abs(male[x])))

    for x, txt in enumerate(text_female):
        txt.set_position((round(female[x]+.25,1), x))
        txt.set_text("{0:0.1f}%".format(abs(female[x])))

    text_titles[0].set_text("{}".format(year))
    text_titles[1].set_text("Population: {0:0.0f} million".format(stats['population']))
    text_titles[2].set_text("Sex Ratio: {0:3d}:1000 ".format(stats['sex_ratio']))
    text_titles[3].set_text("Dep. Ratio: {0:0.1f}% ".format(stats['dependent_ratio']))
    
    return plot_m,plot_f

#------------------------------------------

print("Ploting for {} Years: {} -> {}".format(country_name,start_year,end_year))
stats = prepare_data(country_name,start_year)

plot = first_plot(stats,country_name,start_year)

period = end_year-start_year

if video_enable:
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=2, metadata=dict(artist='Jayam'), bitrate=1800)

line_ani = animation.FuncAnimation(plot[0], update_plot, frames=period, fargs=[plot], interval=500, repeat=False) #, blit=True)

if video_enable:
    line_ani.save("{}.mp4".format(country_name), writer=writer)

plt.show()
