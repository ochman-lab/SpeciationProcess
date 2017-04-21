chemin = "/Users/louis-mariebobay/Desktop/landscape/"
#chemin = "/work/03239/lbobay/landscape/"

########################################################################
import math

 
def mean( echantillon ) :
    size = len( echantillon )
    moyenne = float(sum( echantillon )) / float(size)
    return moyenne


def stat_variance( echantillon ) :
    n = float(len( echantillon )) # taille
    mq = mean( echantillon )**2
    s = sum( [ x**2 for x in echantillon ] )
    variance = s / n - mq
    return variance


def stat_ecart_type( echantillon ) :
    variance = stat_variance( echantillon )
    ecart_type = math.sqrt( variance )
    return ecart_type

def median( echantillon) :
	echantillon.sort()
	size = len( echantillon )
	if len( echantillon ) % 2 == 0:
		M= float(echantillon[size / 2 - 1] + echantillon[size / 2]) / 2
	else:
		M= echantillon[size / 2]
	return M

def ninetyfive( echantillon) :
	echantillon.sort()
	size = len( echantillon )
	i95 = int( float(size) * 95/100 ) - 1
	return echantillon[i95]


def five( echantillon) :
	echantillon.sort()
	size = len( echantillon )
	i5 = int( float(size) * 5/100 ) - 1
	return echantillon[i5]


########################################################################


species=[]
f=open('../selected_species.txt','r')
for l in f:
	a=l.strip('\n').split('\t')
	species.append(a[0])

f.close()



dico={}
liste={}
for sp in species:
	print sp
	dico[sp]={}
	liste[sp]=[]
	f=open('../results/' + sp + '/rm1.txt',"r")
	for l in f:
		a=l.strip("\n").split("\t")
		subset = a[0]
		b=subset.split("-")
		nb = len(b)
		#if "SAEN3" not in b and "SAEN88" not in b:  ###########################
		if 1==1:
			if nb > 3:
				if float(a[2]) > 0:
					rm = float(a[1])/float(a[2])
					if dico[sp].has_key(nb):
						dico[sp][nb].append(rm)
					else:
						dico[sp][nb] = [rm]
						liste[sp].append(nb)
	f.close()




for sp in species:
	liste[sp].sort()
	h=open('../results/' + sp + '/graph.txt',"w")
	h.write("Nb\tMean\tMedian\tSD\n")
	for nb in liste[sp]:
		h.write(str(nb) + "\t" + str(mean(dico[sp][nb])) + "\t" + str(median(dico[sp][nb])) + "\t"  +  str(stat_ecart_type(dico[sp][nb])) + "\n"  )
	h.close()











		