import multiprocessing
import sys
import os

print multiprocessing.cpu_count()
print str(sys.argv)
print 'hello World'

#now do all the things you dream of!
#Don't let your todo list stay memes!

prog = 'usearch_multi.py'

os.chdir('scripts/')
print 'about to run ' + prog + ' with '+sys.argv[1] + ' '+sys.argv[2]
os.system('python ' + prog + ' ' +sys.argv[1] + ' '+sys.argv[2])
