
def intersection(list):
    def distance(v):
        d=int((5000-v)**(1/2)) #une estimation de la distance (unités ??) du stylo à la bobine en fonction de la valeur renvoyée par l'arduino (entre 0 et 1024). On doit améliorer cette approximation !
        return d

    v1,v2,v3=0 #les valeurs renvoyés par l'arduino pour chaque bobine.
         #il est recommandé que les trois bobines de référence prises dans le programme soient les bobines recvant le plus gros voltage sinon il pourrait y avoir des bugs ...
         #la bobine 1 est celle qui forme l'angle droit avec les autres bobines. Elle est prise comme point (0,0). Dans les calculs on considère les axes x et y usuels (y vertical et x horizontal). La bobine 2 est sur l'axe y tandis que la bobine 3 est sur l'axe x.
    d1=distance(v1) #Ici on a donc une estimation de à quelle distance se trouve le stylo par rapport à chacune des trois bobines.
    d2=distance(v2) #Comme on est dans l'espace, ça nous donne 3 sphères, une autour de chaque bobine.
    d3=distance(v3) #L'intersection des 3 sphères donne l'endroit où est le stylo.
    k=1 #distance (unités ?) entre les bobines.
    x=(d1**2-d3**2)/2*k+k/2
    y=(d1**2-d2**2)/2*k+k/2 #ici on a le point (x,y) de où est le stylo S'IL Y A UNE INTERSECTION. S'il n'y a pas d'intersection, la formule renvoie une valeur mais qui n'a pas de réalité physique !
    z1=(d1**2-x*2-y**2)**(1/2) #normalement si tout va bien le z est positif... et pas complexe ! (S'il est complexe le programme bug donc attention, mais normalement ça ne doit pas arriver !)
    z2=(d2**2-x**2-(y-k)**2)**(1/2) #Comme on sait que s'il n'y a pas d'interscetion on a quand même une valeur en (x,y) trompeuse, on regarde le z de chacune des sphères
    z3=(d3**2-(x-k)**2-y**2)**(1/2)  #Si le z est le même pour chacune avec (x,y) trouvé plus haut, alors l'intersection existe.
    tol=0.1 # Evidement, les instruments ne sont pas parfaits, donc on garde une sensibilité, par exemple si z1 est proche de z2 sans être toutefois pafaitement égaux, on considère que l'intersection est bien réelle. (Unités dépend des unités pour k). On test la sensibilité à la ligne suivante.

    if z1-2*tol<z2<z1+2*tol and z2-2*tol<z3<z2+2*tol: #On utilise deux fois tol car on fait deux estimations successives, les erreurs s'accumulent.
        print("l'intersection est",x,y)
    else:
        print("on a",x,y,"mais ce n'est pas une vraie intersection") #Evidement, dans la réalité si l'approximation de la distance est correcte, vu que notre stylo est un point bien réel, alors on a toujours une intersection réelle. Cependant c'est tjs utile de checker si c'est correct ou non dans le cas où l'arduino fournirait une valeur bugée pour une des bobines, on considère que le stylo est tjs au point précédent et ça empêche des sauts incohérents dû aux erreurs de mesures.
