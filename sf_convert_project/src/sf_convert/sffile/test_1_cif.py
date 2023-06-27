
# if len(lines) < 2:
#     print(f"Error! File ({inpfile}) is wrong! too few lines ({len(lines)})")
#     return

def guess_cif_format(inpfile):
    pattern_found = False
    with open(inpfile, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('_reflns.'):
                pattern_found = True
                break
    
    if pattern_found:
        print("CIF")
    else:
        print("Not CIF")

def guess_mmCIF_format(inpfile):
    pattern_found = False
    with open(inpfile, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('_refln.'):
                pattern_found = True
                break
    
    if pattern_found:
        print("mmCIF")
    else:
        print("Not mmCIF")

def guess_cns_format(inpfile):
    n3 = m1 = m2 = mm1 = 0

    with open(inpfile, 'r') as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()

        if line.startswith("INDE") or (line.startswith("DECLare") and "RECIproca" in line[20:]):
            if "FOBS=" in line or "FO=" in line or " F_" in line or "F=" in line:
                m1 += 1
            if "IOBS=" in line or "IO=" in line or "I=" in line:
                m2 += 1
            if " FOBS " in line:
                mm1 += 1
            n3 += 1
            if n3 > 300:
                break
        elif "FOBS=" in line or "FO=" in line or "F=" in line:
            n3 += 1
            m1 += 1
            if m1 > 300:
                break
        elif "IOBS=" in line or " IO=" in line or " I=" in line:
            n3 += 1
            m2 += 1
            if m2 > 300:
                break

    if n3 >= 50 and mm1 < 10:
        # if m1 > 100 and m2 > 100:
        #     print("CNS, I&F")
        # elif m1 > 50 and m2 < 10:
        #     print("CNS, F")
        # elif m2 > 50 and m1 < 10:
        #     print("CNS, I")
        # else:
            print("CNS")
    elif n3 >= 50 and mm1 > 10:
        print("xplor")

def guess_tnt_format(inpfile):
    n4 = 0
    with open(inpfile, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith("HKL"):
                n4 += 1
                if n4 > 200:
                    break
    if n4 >= 100:
        print("TNT")

def guess_xscale_format(inpfile):
    n5 = 0
    with open(inpfile, 'r') as file:
        for line in file:
            line = line.strip()
            if (line.startswith('!SPACE_GROUP_NUMBER=') or
                line.startswith('!UNIT_CELL_CONSTANTS=') or
                line.startswith('!ITEM_H=') or
                line.startswith('!ITEM_K=') or
                line.startswith('!ITEM_L=')):
                n5 += 1
                if n5 > 4:
                    print("XSCALE")
                    break
    print("Not XSCALE")

def guess_dtrek_format(inpfile):
    with open(inpfile, 'r') as f:
        lines = f.readlines()

    n6 = 0
    for line in lines:
        line = line.strip()
        if (line.startswith("CRYSTAL_MOSAICITY=") or  
            line.startswith("CRYSTAL_SPACEGROUP=") or
            line.startswith("CRYSTAL_UNIT_CELL=") or
            line.startswith("nH") or
            line.startswith("nK") or
            line.startswith("nL")):
            n6 += 1
            if n6 > 5:
                print("DTREK")
                break

    print("Not DTREK")

def guess_scalepack_format(inpfile):
    with open(inpfile, 'r') as f:
        lines = f.readlines()

    n7 = 0
    for i, line in enumerate(lines):
        strs = line.split()
        if ((i == 0 and strs[0] == "1" and len(strs) == 1) or
            (i == 1 and (strs[0] == "-985" or strs[0] == "-987") and len(strs) == 1) or
            (i == 2 and '.' in strs[0] and len(line) > 60) and len(strs) == 6):
            n7 += 1
            if n7 >= 3:
                break

    if n7 > 1:
        print("SCALEPACK")

    print("Not SCALEPACK")

def guess_shelx_format(inpfile):
    with open(inpfile, 'r') as file:
        lines = file.readlines()

    n8 = 0
    for line in lines:
        if len(line) > 50 and len(line.strip()) == 32:
            n8 += 1

    if n8 >= 200:
        print("SHELX")
    else:
        print("Not SHELX")

def guess_saint_format(inpfile):
    with open(inpfile, 'r') as f:
        lines = f.readlines()

    n9 = 0
    for i, line in enumerate(lines):
        if i > 50 and len(line.strip()) > 150:
            n9 += 1
            if n9 >= 200:
                break

    if n9 >= 200:
        print("SAINT")
    else:
        print("Not SAINT")

def main():
    inpfile = "1o08.cif"
    guess_cif_format(inpfile)
    inpfile = "7xvx-sf.cif.mmcif"
    #inpfile = "5pny-sf.cif.mmcif"
    guess_mmCIF_format(inpfile)
    inpfile = "cns-sf6.cv"
    guess_cns_format(inpfile)

    guess_scalepack_format("1o08.cif")

if __name__ == "__main__":
    main()
