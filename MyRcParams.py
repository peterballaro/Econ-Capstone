import matplotlib as mpl 
def mympl(backround_color='white', font_family="serif"):
    mpl.rcParams['axes.spines.right'] = False
    mpl.rcParams['axes.spines.left'] = False
    mpl.rcParams['axes.spines.top'] = False
    #mpl.rcParams['axes.spines.bottom'] = True
    mpl.rcParams['figure.facecolor'] = backround_color 
    mpl.rcParams["axes.facecolor"] = backround_color
    mpl.rcParams["font.family"] = font_family