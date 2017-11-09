from multiprocessing import Pool
import multiprocessing
import os
from config import *

#species=getSpeciesOfSize(500)


species = getSingleSpecies()
strains=getStrains(species)
specialStrain = getCompStrain()+'.fa'
exclusion=[]
genes={}
parent={}
tmp={}
strains[species[0]].append(specialStrain)
for sp in species:
	tmp[sp]={}
	genes[sp]=[]
	for st in strains[sp]:
		nb=0
		if st != specialStrain:
			#print 'normal strain'
			f=open(PATH_TO_OUTPUT + sp + '/genes/' + st,"r")
		else:
			#print 'special strain'
			f=open(PATH_TO_UPLOAD + st,"r")
		for l in f:
			if l[0] == ">":
				#should add .strip('+').strip('-')
				id = l.strip("\n").strip(">").split(" ")[0]
				if parent.has_key(id):
					print "PROBLEM !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
				parent[id] = st
				nb+=1
				tmp[sp][id]=[]
			else:
				tmp[sp][id].append(l)
		f.close()
		genes[sp].append(nb)




seq={}
for sp in species:
	seq[sp]={}
	for id in tmp[sp]:
		seq[sp][id] = "".join(tmp[sp][id])

tmp={}

doublons={}
core={}
for sp in species:
	doublons[sp]=0
	core[sp]=[]
	f = None
	try:
		f=open(PATH_TO_UPLOAD+ 'out.input_' + sp + '.txt.I12',"r")
	except:
		print 'Skipping! '+ str(sp)
		continue
	for l in f:
		a=l.strip("\n").split("\t")
		tmp=[]
		for id in a:
			try:
				st = parent[id]
				if st in strains[sp]:
					tmp.append(id)
			except KeyError:
				pass
		a=list(tmp)
		if len(a) >= 0.85 * len(strains[sp]):
			tmp=[]
			tag=0
			b=[]
			for id in a:
				if parent.has_key(id):
					st = parent[id]
					if st not in tmp:
						tmp.append(st)
					else:
					#	print 'doublon'
					#	very noisy output, so removed
						tag=1
					b.append(st)
			if tag == 1:
				doublons[sp] += 1
			if len(tmp) >= 0.85 * len(strains[sp]) and tag==0:
			#	print sp,' ',len(tmp),' ',len(strains[sp])
			#also very noisy output, so removed
				core[sp].append(a)
	f.close()

for sp in species:
	try:
		files = os.listdir(PATH_TO_UPLOAD + 'align/')
		for f in files:
			os.remove(f)
	except OSError:
		pass
	h=open(PATH_TO_UPLOAD + 'orthologs.txt',"w")
	nb=0
	for lili in core[sp]:
		#### Change to only do this if lili contains 'gene####'
		tag = False
		for id in lili:
			if 'gene' in id:
				tag = True 
		if tag:
			nb+=1
			ortho = "ortho" + str(nb)
			h.write(ortho + "\t" + "\t".join(lili) + "\n")
			g=open(PATH_TO_UPLOAD+ 'align/' + ortho + ".fa","w")
			for id in lili:
				g.write(">" + id + "\n" + seq[sp][id]  )
			g.truncate()
			g.close()	
	h.close()
	###Also append nb to the file with our criticalstats
	critInfoFD = open(PATH_TO_UPLOAD+'crit_stats.txt','a')
	critInfoFD.write('Number of core genes orthologous to your genome: '+str(nb)+'\n')
	critInfoFD.close()

	#removed the part that mentions network and clusters because works without... (len(networks[sp]) 'clusters')
	ratio = 0
	if mean(genes[sp]) > 0:	
		ratio = nb/mean(genes[sp])
		print sp,' There are ',nb,' core genes and ',doublons[sp],' doublons ',mean(genes[sp]), ' genes on average for',len(strains[sp]),' strains.  Ratio=',100*nb/mean(genes[sp]),' %'