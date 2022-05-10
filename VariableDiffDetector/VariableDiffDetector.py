import sys
import subprocess

EXCLUDES = []

EXCLUDES_FILES = []

def VariableTesterScript(argv):

    tempf = open("foundvars","w")
    tempf.close()

    f = open(argv[1],"r")
    lines = f.readlines()
    currfname = ""
    for aline in lines:
        atoks = aline.split()
        if len(atoks) > 0:
            if atoks[0] == "File":
                colonidx = atoks[1].find(":")
                currfname = atoks[1][0:colonidx]
            if currfname in EXCLUDES_FILES:
                continue
            alasttok = atoks[len(atoks)-1]
            if alasttok[len(alasttok)-1] == ';' and atoks[0][len(atoks[0])-1] == ':':
                if "const" not in atoks:
                    if ')' in alasttok: # a function pointer variable find the actual var name
                        for atok in atoks:
                            if '(' in atok and ')' in atok:
                                openbrkidx = atok.find('(')
                                closebrkdix = atok.find(')')
                                alasttok = atok[openbrkidx+1:closebrkdix]
                                break
                    semcolidx = alasttok.find(';')
                    if semcolidx > 0:
                        alasttok = alasttok[0:semcolidx]
                    if '[' in alasttok:
                        openbrkidx = alasttok.find('[')
                        alasttok = alasttok[0:openbrkidx]
                    while '*' in alasttok:
                        alasttok = alasttok.lstrip('*')                    
                    varnamestr = "'" + currfname+"'::"+alasttok
                    # print(aline)
                    print(varnamestr)
                    if varnamestr not in EXCLUDES:
                        gdbexecfile = open("gdbexec","w")
                        gdbexecfile.write("b old_main\n")
                        gdbexecfile.write("run "+argv[3]+"\n")
                        gdbexecfile.write("set logging file iter1\n")
                        gdbexecfile.write("set logging overwrite on\n")
                        gdbexecfile.write("set logging on\n")
                        gdbexecfile.write("p "+varnamestr+'\n')
                        gdbexecfile.write("set logging off\n")
                        gdbexecfile.write("c\n")
                        gdbexecfile.write("set logging file iter2\n")
                        gdbexecfile.write("set logging overwrite on\n")
                        gdbexecfile.write("set logging on\n")
                        gdbexecfile.write("p "+varnamestr+'\n')
                        gdbexecfile.write("set logging off\n")
                        gdbexecfile.write("q\n")
                        gdbexecfile.close()
                        subprocess.call(['gdb',argv[2],'-batch-silent','-x','gdbexec'])

                        iter1file = open("iter1","r")
                        iter2file = open("iter2","r")

                        iter1data = iter1file.read()
                        iter2data = iter2file.read()
                        iter1stripidx = iter1data.find('=')
                        iter2stripidx = iter2data.find('=')
                        iter1data = iter1data[iter1stripidx+1:len(iter1data)]
                        iter2data = iter2data[iter2stripidx+1:len(iter2data)]

                        if iter1data != iter2data:
                            foundouts = open("foundvars","a")
                            foundouts.write("found!: "+varnamestr+"\n")
                            foundouts.close()

                        iter1file.close()
                        iter2file.close()
            
    f.close()

if __name__=="__main__":
    VariableTesterScript(sys.argv)
