import sys
import subprocess

def ExtractingVarInputs(argv):

    varignoredfile = open("VarEdgesIgnore","r")
    ignorevarsraw = varignoredfile.readline()
    ignorevars = ignorevarsraw.split()
    ignorevarsset = set(ignorevars)
    varignoredfile.close()

    subprocess.run(["cp",argv[2],"in.temp/"])

    subprocess.run(["/home/ubuntu/AFLplusplus/afl-fuzz", "-i", "in.temp/", "-o", "out.temp/", "-m", "none", "-d", "-E", "1", "--", argv[1], "@@"])

    actualinfilename = argv[2].split('/')
    actualinfilename = actualinfilename[len(actualinfilename)-1]

    subprocess.run(["rm","in.temp/"+actualinfilename])

    outfuzzerstatsfile = open("out.temp/default/fuzzer_stats","r")
    lines = outfuzzerstatsfile.readlines()

    atoks = None
    for aline in lines:
        if "var_bytes" in  aline:
            atoks = aline.split()
            atoks = atoks[2:len(atoks)]
            atoks = set(atoks)
    outfuzzerstatsfile.close()

    foundvaredges = atoks - ignorevarsset

    if len(foundvaredges) > 0:
        foundvarinputsfile = open("VarInputsFound","a")
        foundvarinputsfile.write(argv[2]+"\n")
        foundvarinputsfile.close()
        foundvaredgesfile = open("var.edges.for.inputs/"+actualinfilename,"w")
        for avaredge in foundvaredges:
            foundvaredgesfile.write(avaredge+" ")
        foundvaredgesfile.close()

if __name__=="__main__":
    ExtractingVarInputs(sys.argv)
