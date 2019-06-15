#--------------------------------------------------------------------------------
# Interface visuelle Turtle avec nombre de capteurs variables
# Plotting des valeurs de chaque capteur
#
# Andru Onciul
#--------------------------------------------------------------------------------


############## IMPORTS ############################################################################################################################################

import turtle as turtle
import time
import numpy as np
from serial import Serial
from color import palette_de_couleurs
from matplotlib import pyplot as plt

############## Setting the variables ############################################################################################################################################

maxcount= 300
nb_of_captors= 6
port = Serial('COM4', 115200)
nb_dif_colors= 20
colors= palette_de_couleurs(nb_dif_colors)
beugvalue= 100

############## Set up the screen ############################################################################################################################################

wn = turtle.Screen()
wn.bgcolor("white")
wn.colormode(255)
wn.setup(width = 1.0, height = 1.0)

############## Grading scale visual/Echelle du voltage ################################################################################################################################################

## Grading scale size
legend_start=(-1000,790)
legend_length= 2000
legendturtle_size= 5

## Creating the turtles for grading
for i in range(nb_dif_colors):
    t=turtle.Turtle()
    t.penup()
    t.speed(0)
    t.shape("square")
    t.shapesize(legendturtle_size,legendturtle_size)
    t.color(colors[i])
    t.setposition(legend_start[0] + (legend_length/len(colors))*(i) ,legend_start[1])
    
## Write the values of grading
volt_values=["0 V","1 V","2 V","3 V","4 V","5 V"]
mypen=turtle.Turtle()
mypen.speed(0)
mypen.penup()
mypen.setposition(legend_start[0] - legendturtle_size*10 , legend_start[1] - legendturtle_size*19)
for i in range(6):
    mypen.write(volt_values[i],False,align="center",font=("Arial black",12,"normal"))
    mypen.forward((legend_length+legendturtle_size*4)/5)
mypen.hideturtle()

############## Setting up the changing color squares ##############################################################################################################################
        
## Creating the turtles that will change colors
captors_size= 20
captors_startpos= (-(captors_size*8 * 3),-550)

t= [0 for i in range(nb_of_captors)]
for i in range(nb_of_captors):
    ## Creating and positioning the turtles
    t[i]=turtle.Turtle()
    t[i].penup()
    t[i].shape("square")
    t[i].shapesize(captors_size,captors_size)
    t[i].color("red")
    x= captors_startpos[0] + (i%3)* captors_size*20
    y= captors_startpos[1] + (i//3)* captors_size*20
    t[i].setposition(x,y)
    ## Writing theirs names
    if i//3==0:
        mypen.setposition(x,y-260)
        #print("A%s pos:(%s,%s)" % (i,x,y-250))
    elif i//3==1:
        mypen.setposition(x,y+210)
        #print("A%s pos:(%s,%s)" % (i,x,y+250))
    mypen.write("A%s"%(i),False,align="center",font=("Arial black",14,"bold"))
    #print("turtle n%s position: x: %s  y: %s" % (i,x,y))

############## MAIN FUNCTION ##########################################################################################################################################################

def main_fct():

############## Functions ##########################################################################################################################################################
    ## Defining the color changing function
    def color_turtle(nb,turtle):
        """ Input: Takes in an int (nb) that corresponds to a color and a turtle (t)
            Function: Changes the color of that turtle
            """
        
        if nb == None:
            #print("Incorrect value for voltage" )
            pass
        elif 0<=nb<=5000:
            turtle.color(colors[(nb * ((len(colors)-1))//5000)])
            print("color of  ",turtle,"  changed to ",(nb*((len(colors)-1))//5000),"/",len(colors))
        elif nb>5000:
            turtle.color(colors[ len(colors)-1 ])
            print("BEUG trop grand (nb>5000): ","color of  ",turtle," changed to max color")
        
    ## Function that reads values from port
    def get_reading(port):
        """Reads value on port. Each space(" ") means a new value begins.
            """
        number=""
        while(port.inWaiting() != 0):
            byte=port.read() #on lit un caractère
            car=str(byte)[2:-1]
            if car!= " ":
                number+= car
            else:
                return int(number)
    ##MAIN LOOP
    start=time.time()
    
    print("-"*30,"Program begins","-"*30)
    l= [ np.zeros(maxcount) for i in range(nb_of_captors) ]
    count=0
    
    ## Loop that changes the colors of the turtle
    while count < maxcount:
        port.write(b'K')
        dist= np.zeros(nb_of_captors)
        for i in range(nb_of_captors):
            voltage= get_reading(port)
            color_turtle(voltage,t[i])
            l[i][count]= voltage
            dist[i]=voltage
        print("dist= ",dist)
        count+=1

    end=time.time()

    ## Print perfomance
    total_time= end-start
    time_per_refresh= (total_time)/maxcount
    print("\n")
    print("-"*35,"Program performance","-"*35)
    print("Time for program: %ss" % (total_time)," for %s refreshes" % maxcount)
    print("Time per refresh: %ss" % (time_per_refresh) )
    print("-"*91)
    print("\n")

    ## Plotting 
    x=np.arange(0,maxcount,1)
    for i in range(nb_of_captors):
        liste= l[i]
        plt.subplot( int('33'+str(i+1)) )
        plt.plot(x,liste,'red',label="A%s voltage"%(i))
        plt.ylabel("milliVolt (mV)")
        plt.ylim((0,5000))
        plt.legend()

    mng = plt.get_current_fig_manager()
    mng.window.state("zoomed")
    plt.show()
    wn.mainloop()
    
############## Keyboard binding ##########################################################################################################################################################
wn.listen()
wn.onkey(main_fct,"space")    #quand on presse la touche space la fonction main_fct() s'éxecute
wn.mainloop()

