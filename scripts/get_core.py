from multiprocessing import Pool
import multiprocessing
import os
from config import *

#species=getSpeciesOfSize(500)


def getCore(spec):

	species = [spec]

	"""
	network={}
	for sp in species:
		network[sp]=[]
		f=open('../results/' + sp + '/out.network.txt.I12' ,'r' )
		for l in f:
			a=l.strip("\n").split("\t")
			network[sp].append(a)
		f.close()

	for sp in species:
		h=open('../results/' + sp + '/new_strains.txt' ,'w' )
		for st in network[sp][0]:
			h.write(st + '\n')
		h.close()

	"""

	strains=getGenomes(species)

	exclusion=[]

	genes={}
	parent={}
	tmp={}
	for sp in species:
		tmp[sp]={}
		genes[sp]=[]
		for st in strains[sp]:
			nb=0
			f=open(PATH_TO_OUTPUT + sp + '/genes/' + st,"r")
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
		f=open(PATH_TO_OUTPUT + sp + '/out.input_' + sp + '.txt.I12',"r")
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
			os.system('rm ' + PATH_TO_OUTPUT + sp + '/align/*' )
		except OSError:
			pass
		h=open(PATH_TO_OUTPUT + sp + '/orthologs.txt',"w")
		nb=0
		for lili in core[sp]:
			nb+=1
			ortho = "ortho" + str(nb)
			h.write(ortho + "\t" + "\t".join(lili) + "\n")
			g=open(PATH_TO_OUTPUT + sp + '/align/' + ortho + ".fa","w")
			for id in lili:
				g.write(">" + id + "\n" + seq[sp][id]  )
			g.close()	
		h.close()
		#removed the part that mentions network and clusters because works without... (len(networks[sp]) 'clusters')
		print sp,' There are ',nb,' core genes and ',doublons[sp],' doublons ',mean(genes[sp]), ' genes on average for',len(strains[sp]),' strains.  Ratio=',100*nb/mean(genes[sp]),' %'
		ratio = nb/mean(genes[sp])
		if ratio >= 0.20:
			k=open('../selected_species.txt','a')
			k.write(sp + '\t' + str(len(strains[sp])) + '\n')
			k.close()

if __name__ == '__main__':
	k=open('../selected_species.txt','w')
	k.seek(0)
	k.truncate()
	k.close()	

#	species = getSpeciesOfSize(500)	
	species = ['Acetobacter_pasteurianus']
	print multiprocessing.cpu_count()
	p = Pool(multiprocessing.cpu_count()*2)
	p.map(getCore,species)