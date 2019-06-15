import colorlover as cl
from numpy import array

def palette_de_couleurs(nb_of_colors):
    """ Input: the length of the list with different colors
        Output: a list with rgb colors in an ascending order
        """
    
    bupu = cl.scales['9']['seq']['Reds']
    bupu500 = cl.interp( bupu, nb_of_colors ) # Map color scale to 500 bins
    colors=cl.to_rgb(bupu500)
    for i in range(nb_of_colors):
        color= colors[i][3:]
        c=array((0,0,0))
        for j in range(3):
            c[j]=color.strip("()").split(",")[j]
        colors[i]=c
    return colors


"""
print(cl.scales)
print("\n")
print(palette_de_couleurs(9))
"""