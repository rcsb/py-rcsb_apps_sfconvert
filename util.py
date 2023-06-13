import math
import os
import numpy as np

PDBID = "" * 80
RESOH = 0.0
RESOL = 0.0

class SF:
    def __init__(self):
        self.a = self.b = self.c = None
        self.alpha = self.beta = self.gamma = None
        self.sg = self.nsg = None
        self.wavelength = self.symm = self.resh = self.resl = self.nobs = None
        self.hmax = self.kmax = self.lmax = self.hmin = self.kmin = self.lmin = self.nall = None
        self.H = self.K = self.L = self.Fo = self.sFo = self.Fo_au = self.sFo_au = self.Fc = self.Fc_au = None
        self.Io = self.sIo = self.F2o = self.sF2o = self.Ic = self.F2c = None
        self.fom = self.phase_c = self.phase_o = self.status = self.flag = self.free1 = self.free2 = None
        self.wave_id = self.cryst_id = self.scale_id = self.diffr_id = None
        self.I_plus = self.sI_plus = self.I_minus = self.sI_minus = None
        self.F_plus = self.sF_plus = self.F_minus = self.sF_minus = None
        self.hla = self.hlb = self.hlc = self.hld = None
        self.hla1 = self.hlb1 = self.hlc1 = self.hld1 = self.anom = self.anoms = None
        self.aud_id = self.aud_date = self.aud_rec = self.aud_meth = None
        self.dif_id = self.dif_cid = self.dif_detail = self.temp = self.treat = None
        self.d_spacing = self.a_calc = self.b_calc = self.weighted = self.fs_uncorrected = None
        self.f_uncorrected = self.gsas_i100_meas = self.i_unknown = self.is_unknown = None
        self.phase_part = self.F_part_au = self.phase_with = self.fcalc_with = None
        self.Fc_all = self.Fc_all_ph = self.fwt = self.phwt = self.delfwt = self.delphwt = None
        self.fib_co = self.fib_fo = self.fib_ly = self.wt = None
        self.pow_sc = self.pow_io = self.pow_iop = self.pow_wt = self.pow_ic = self.pow_ict = None
        self.dH = self.dK = self.dL = self.unmerge_i = self.unmerge_si = self.unmerge_angle_phi = None
        self.unmerge_std_code = self.unmerge_scale_group = None
        self.nref = self.dnref = self.nwave = self.nsymm = self.naud = self.ndif = self.npow = None



def get_resolution(h, k, l, rcell):
    aa1 = 2 * rcell[0] * rcell[1] * math.cos(math.radians(rcell[5]))
    aa2 = 2 * rcell[0] * rcell[2] * math.cos(math.radians(rcell[4]))
    aa3 = 2 * rcell[1] * rcell[2] * math.cos(math.radians(rcell[3]))

    a2 = rcell[0] * rcell[0]
    b2 = rcell[1] * rcell[1]
    c2 = rcell[2] * rcell[2]

    dist_sq = h * h * a2 + k * k * b2 + l * l * c2 + h * k * aa1 + h * l * aa2 + k * l * aa3
    resol = 0
    if dist_sq > 0.0000001:
        resol = 1.0 / math.sqrt(dist_sq)

    return resol

sf = SF()

def check_cell(cell, nblock):

    if sf.a and sf.b and sf.c and sf.alpha and sf.beta and sf.gamma:
        cell[0] = float(sf.a)
        cell[1] = float(sf.b)
        cell[2] = float(sf.c)
        cell[3] = float(sf.alpha)
        cell[4] = float(sf.beta)
        cell[5] = float(sf.gamma)

        if CELL[0] > 0.01 and nblock == 0 and (
            abs(cell[0] - CELL[0]) > 0.1 or abs(cell[1] - CELL[1]) > 0.1 or abs(cell[2] - CELL[2]) > 0.1 or
            abs(cell[3] - CELL[3]) > 0.1 or abs(cell[4] - CELL[4]) > 0.1 or abs(cell[5] - CELL[5]) > 0.1
        ):
            INFO = "Warning! SF and PDB ({0} nblock={1}) cell values mismatch.".format(PDBID, nblock + 1) # need to find PDBID
            pinfo(INFO, 0) # need to find pinfo

            if (
                abs(cell[0] - CELL[0]) > 3.0 or abs(cell[1] - CELL[1]) > 3.0 or abs(cell[2] - CELL[2]) > 3.0 or
                abs(cell[3] - CELL[3]) > 3.0 or abs(cell[4] - CELL[4]) > 3.0 or abs(cell[5] - CELL[5]) > 3.0
            ):
                INFO = "Error: ({0} nblock={1}) large cell value mismatch (>3.0).".format(PDBID, nblock + 1)
                print("cell in sf: {0:6.2f} {1:6.2f} {2:6.2f} {3:6.2f} {4:6.2f} {5:6.2f}".format(
                    cell[0], cell[1], cell[2], cell[3], cell[4], cell[5]
                ))
                print("cell in PDB: {0:6.2f} {1:6.2f} {2:6.2f} {3:6.2f} {4:6.2f} {5:6.2f}".format(
                    CELL[0], CELL[1], CELL[2], CELL[3], CELL[4], CELL[5]
                ))

                pinfo(INFO, 0)

    elif (
        CELL[0] > 0.01 and CELL[1] > 0.01 and CELL[2] > 0.01 and
        CELL[3] > 0.01 and CELL[4] > 0.01 and CELL[5] > 0.01
    ):
        cell[0] = CELL[0]
        cell[1] = CELL[1]
        cell[2] = CELL[2]
        cell[3] = CELL[3]
        cell[4] = CELL[4]
        cell[5] = CELL[5]

FTMP1 = None
FTMP2 = None

def pinfo(info, id):
    # Write all the log information about the SF file
    if "Warning" in info or "Error" in info:
        FTMP1.write(info + "\n")
        print(info)
    else:
        if id == 0:
            FTMP2.write(info + "\n")
            print(info)
        elif id == 1:
            FTMP2.write(info + "\n")
        elif id == 2:
            print(info)

def calc_recip_cell(cell, rcell):
    cosa = math.cos(math.radians(cell[3]))
    cosb = math.cos(math.radians(cell[4]))
    cosc = math.cos(math.radians(cell[5]))
    sina = math.sin(math.radians(cell[3]))
    sinb = math.sin(math.radians(cell[4]))
    sinc = math.sin(math.radians(cell[5]))

    v = cell[0] * cell[1] * cell[2] * math.sqrt(1. - cosa*cosa - cosb*cosb - cosc*cosc + 2.*cosa*cosb*cosc)

    rcell[0] = cell[1] * cell[2] * sina / v
    rcell[1] = cell[0] * cell[2] * sinb / v
    rcell[2] = cell[0] * cell[1] * sinc / v

    cosast = (cosb*cosc - cosa) / (sinb*sinc)
    cosbst = (cosa*cosc - cosb) / (sina*sinc)
    coscst = (cosa*cosb - cosc) / (sina*sinb)

    rcell[3] = math.acos(cosast) / math.radians(1.0)
    rcell[4] = math.acos(cosbst) / math.radians(1.0)
    rcell[5] = math.acos(coscst) / math.radians(1.0)


def check_sf(j, resol):
    # check various errors in the single set; j, the block number

    hkl_min, hkl_max, hkl, mess, file = "", "", "", "", ""
    
    ah,ak,al,key,nstart,n1,n2, n4,n5,n6,n7,n8 = 0,0,0,0,0,0,0,0,0,0,0,0
    max_H, min_H, max_K, min_K,max_L, min_L,nblock = -500, 500, -500, 500, -500, 500, 0
    
    nfp, nfn, nip, nin, n_obs, n_free,nnii, nnii_low, nref = 0, 0, 0, 0, 0, 0, 0, 0, 0
    n, i, nf_sFo, nf_sIo, nfpairF, nfpairI, nf_Fo, nf_F2o, nf_Io = 0, 0, 0, 0, 0, 0, 0, 0, 0
    
    f, sigf, resolution, rfree_p, max_F, min_F, max_I, min_I, max_R, min_R, max_F2, min_F2 = 0, 0, 0, 0, -500000, 500000, -5000000, 5000000, -500, 900, -500000, 500000
    rcell, cell = [0]*6, [0]*6
    
    sum_i, sum_si, sum_f, sum_sf, i_over_si, f_over_sf, sum_f2, sum_sf2, f2_over_sf2, val, sval, ii_sigii, ii_sigii_low, sum_sigii, sum_ii, ratio, ii_sigii_max = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -90000
    
    nblock=j+1
    resol[0]=100
    
    nstart=0
    n=sf.nref
    file = PDBID

    check_cell(cell, j) #get cell for block j
    
    mess = "Warning:"
    if j == 0: 
        mess = "Error:"
    
    if not (sf.H or sf.K or sf.L or sf.dH or sf.dK or sf.dL):
        INFO = f"{mess} File ({file}) has no 'index_h, index_k, index_l' (data block={nblock})."
        pinfo(INFO, 0)
        return


    if not (sf.Fo_au or sf.Fo or sf.Io or sf.F2o or sf.I_plus or sf.I_minus or sf.F_plus or sf.F_minus or sf.unmerge_i or sf.unmerge_si):
        INFO = f"{mess} File ({file}) has no mandatory items 'F/I/F+/F-/I+/I-' (data block={nblock})."
        pinfo(INFO, 0)
        return

    if n < 30 and sf.dnref > 30:
        return  # do not further check the unmerged data!!

    if n < 30:
        INFO = f"Error:  File ({file}) has too few reflections ({n}) (data block={nblock})."
        pinfo(INFO, 0)
        return

    if (sf.Fo_au and not sf.sFo_au) or (sf.Fo and not sf.sFo) or (sf.Io and not sf.sIo) or (sf.F2o and not sf.sF2o) or (sf.I_plus and not sf.sI_plus) or (sf.I_minus and not sf.sI_minus) or (sf.F_plus and not sf.sF_plus) or (sf.F_minus and not sf.sF_minus) or (sf.unmerge_i and not sf.unmerge_si):
        INFO = f"Warning: File ({file}) sigma values are missing (data block={nblock})!"
        pinfo(INFO, 0)

    if j == 0 and not sf.status:
        INFO = f"Warning: File ({file}) has no free set (data block={nblock})."
        pinfo(INFO, 0)

    if cell[0] > 0.01 and cell[1] > 0.01:
        key = 1
        calc_recip_cell(cell, rcell)


    for i in range(nstart, n):
        ah = int(sf.H[i])
        ak = int(sf.K[i])
        al = int(sf.L[i])

        if ah < min_H:
            min_H = ah
        if ak < min_K:
            min_K = ak
        if al < min_L:
            min_L = al

        if ah > max_H:
            max_H = ah
        if ak > max_K:
            max_K = ak
        if al > max_L:
            max_L = al

        if not ((sf.Fo_au and sf.Fo_au[i][0] != '?') or (sf.Io and sf.Io[i][0] != '?') or
                (sf.I_plus and sf.I_plus[i][0] != '?') or (sf.I_minus and sf.I_minus[i][0] != '?') or
                (sf.F_plus and sf.F_plus[i][0] != '?') or (sf.F_minus and sf.F_minus[i][0] != '?') or
                (sf.unmerge_i and sf.unmerge_i[i][0] != '?') or
                (sf.F2o and sf.F2o[i][0] != '?') or (sf.Fo and sf.Fo[i][0] != '?')):
            continue

        nref += 1

        hkl = f"HKL={ah:4d} {ak:4d} {al:4d}"

        if (ah == 0 and ak == 0 and al == 0) or (abs(ah) > 800 or abs(ak) > 800 or abs(al) > 800):
            n1 += 1
            if n1 == 1:
                INFO = f"Error: File ({file}) has wrong indices ({hkl})."
                pinfo(INFO, 0)

        if sf.sFo_au and i > 0 and float(sf.sFo_au[i - 1]) == float(sf.sFo_au[i]):
            nf_sFo += 1
        if sf.sIo and i > 0 and float(sf.sIo[i - 1]) == float(sf.sIo[i]):
            nf_sIo += 1

        if sf.F_plus:
            f = float(sf.F_plus[i])
            nfpairF += 1
            if f < 0 and n4 == 1:
                n4 += 1
                INFO = f"Error: File ({file}) has negative amplitude (F+: {sf.F_plus[i]}) for ({hkl})."
                pinfo(INFO, 0)

        if sf.I_plus:
            nfpairI += 1
            f = float(sf.I_plus[i])

        if key > 0:
            resolution = get_resolution(ah, ak, al, rcell)
            if resolution < min_R:
                min_R = resolution
                hkl_min = f"{ah:4d} {ak:4d} {al:4d}"
            if resolution > max_R:
                max_R = resolution
                hkl_max = f"{ah:4d} {ak:4d} {al:4d}"
            
            val = 0
            sval = 0
            if sf.Io and sf.sIo and sf.sIo[i][0] != '?':
                val = float(sf.Io[i])
                sval = float(sf.sIo[i])
            elif sf.Fo_au and sf.sFo_au and sf.sFo_au[i][0] != '?':
                val = float(sf.Fo_au[i]) * float(sf.Fo_au[i])
                sval = 2 * float(sf.Fo_au[i]) * float(sf.sFo_au[i])
            elif sf.F2o and sf.sFo and sf.sF2o[i][0] != '?':
                val = float(sf.F2o[i])
                sval = float(sf.sF2o[i])
            elif sf.Fo and sf.sFo and sf.sFo[i][0] != '?':
                val = float(sf.Fo[i]) * float(sf.Fo[i])
                sval = 2 * float(sf.Fo[i]) * float(sf.sFo[i])

            if sval > 0:
                sum_sigii += sval
                sum_ii += val
                ratio = val / sval
                ii_sigii += ratio
                if resolution > 7.0:
                    ii_sigii_low += ratio
                    nnii_low += 1
                if ratio > ii_sigii_max:
                    ii_sigii_max = ratio
                nnii += 1

        if resolution <= RESOL + 0.01 and resolution >= RESOH - 0.01:
            if sf.F_plus and '?' not in sf.F_plus[i]:
                nfp += 1
            if sf.F_minus and '?' not in sf.F_minus[i]:
                nfn += 1
            if sf.I_plus and '?' not in sf.I_plus[i]:
                nip += 1
            if sf.I_minus and '?' not in sf.I_minus[i]:
                nin += 1

            if (sf.Fo and '?' not in sf.Fo[i]) or (sf.Fo_au and '?' not in sf.Fo_au[i]) or (sf.Io and '?' not in sf.Io[i]) or (sf.F2o and '?' not in sf.F2o[i]) or ((sf.F_plus and '?' not in sf.F_plus[i]) or (sf.F_minus and '?' not in sf.F_minus[i])) or ((sf.I_plus and '?' not in sf.I_plus[i]) or (sf.I_minus and '?' not in sf.I_minus[i])):
                if sf.status and 'o' in sf.status[i]:
                    n_obs += 1
                elif sf.status and 'f' in sf.status[i]:
                    n_free += 1

        #    print(f"the resolution {RESOH:.2f} {RESOL:.2f} {i}")

        if sf.Fo_au:
            f = float(sf.Fo_au[i])
            if f < 0 and n5 == 1:
                n5 += 1
                INFO = f"Error: File ({file}) has negative amplitude (Fo: {sf.Fo_au[i]}) for ({hkl})."
                pinfo(INFO, 0)

            if f < min_F:
                min_F = f
            if f > max_F:
                max_F = f

            if sf.sFo_au:
                sigf = float(sf.sFo_au[i])
                if sigf > 0 and '?' not in sf.sFo_au[i]:
                    f_over_sf += f / sigf
                    sum_f += f
                    sum_sf += sigf
                    nf_Fo += 1

        if sf.F2o:
            f = float(sf.F2o[i])
            if f < min_F2:
                min_F2 = f
            if f > max_F2:
                max_F2 = f
            if sf.sF2o:
                sigf = float(sf.sF2o[i])
                if sigf > 0 and '?' not in sf.sF2o[i]:
                    f2_over_sf2 += f / sigf
                    sum_f2 += f
                    sum_sf2 += sigf
                    nf_F2o += 1

        if sf.Io:
            f = float(sf.Io[i])
            if f < min_I:
                min_I = f
            if f > max_I:
                max_I = f
            if sf.sIo:
                sigf = float(sf.sIo[i])
                if sigf > 0 and '?' not in sf.sIo[i]:
                    i_over_si += f / sigf
                    sum_i += f
                    sum_si += sigf
                    nf_Io += 1

        if sf.fom and abs(float(sf.fom[i])) > 1.01:
            if n6 == 1:
                n6 += 1
                INFO = f"Warning: File ({file}) has wrong values of FOM ({sf.fom[i]}) for ({hkl})."
                pinfo(INFO, 0)
        if sf.phase_c and abs(float(sf.phase_c[i])) > 361.0:
            if n7 == 1:
                n7 += 1
                INFO = f"Warning: File ({file}) has wrong values of phase ({sf.phase_c[i]}) for ({hkl})."
                pinfo(INFO, 0)
        if sf.phase_o and abs(float(sf.phase_o[i])) > 361.0:
            if n8 == 1:
                n8 += 1
                INFO = f"Warning: File ({file}) has wrong values of phase ({sf.phase_o[i]}) for ({hkl})."
                pinfo(INFO, 0)


    if n1 > 0:
        INFO = f"Error: File ({file}) has ({n1}) reflections with wrong indices."
        pinfo(INFO, 0)

    if n2 > 0:
        INFO = f"Warning: File ({file}) has ({n2}) reflections with negative SIGMA, (Corrected: given status '<')."
        pinfo(INFO, 0)

    if n4 > 0:
        INFO = f"Error: File ({file}) has ({n4}) reflections with negative amplitude (F+)."
        pinfo(INFO, 0)

    if n5 > 0:
        INFO = f"Error: File ({file}) has ({n5}) reflections with negative amplitude (Fo)."
        pinfo(INFO, 0)

    if nref > 10 and ((nf_sFo > 0 and nref - nf_sFo < 3) or (nf_sIo > 0 and nref - nf_sIo < 3)):
        INFO = f"Warning! File ({file}) has Sigma_Fo all the same!"
        pinfo(INFO, 0)

    INFO = f"Total number of observed reflections = {(n_obs + n_free)}"
    pinfo(INFO, 1)

    INFO = f"Total number of observed reflections (status='o') = {n_obs}"
    pinfo(INFO, 1)

    INFO = f"Total number of observed reflections (status='f') = {n_free}"
    pinfo(INFO, 1)

    if n_obs > 0:
        rfree_p = 100 * float(n_free) / float(n_obs)
        INFO = f"Percentage for free set = {rfree_p:.2f}"
        pinfo(INFO, 1)

    if nfpairF > 10:
        INFO = f"Total number of Friedel pairs (F+/F-) = {nfpairF}"
        pinfo(INFO, 1)
        INFO = f"Total number of observed F+ = {nfp}"
        pinfo(INFO, 1)
        INFO = f"Total number of observed F- = {nfn}"
        pinfo(INFO, 1)
        INFO = f"Sum of observed F+ and F- = {nfn + nfp}"
        pinfo(INFO, 1)

    if nfpairI > 10:
        INFO = f"Total number of Friedel pairs (I+/I-) = {nfpairI}"
        pinfo(INFO, 1)
        INFO = f"Total number of observed I+ = {nip}"
        pinfo(INFO, 1)
        INFO = f"Total number of observed I- = {nin}"
        pinfo(INFO, 1)
        INFO = f"Sum of observed I+ and I- = {nin + nip}"
        pinfo(INFO, 1)

    if key > 0 and cell[0] > 0.001:
        INFO = f"Cell = {cell[0]:.2f} {cell[1]:.2f} {cell[2]:.2f} {cell[3]:.2f} {cell[4]:.2f} {cell[5]:.2f}"
        pinfo(INFO, 1)

        INFO = f"Lowest resolution = {max_R:7.2f}; corresponding HKL = {hkl_max}"
        pinfo(INFO, 1)
        INFO = f"Highest resolution = {min_R:7.2f}; corresponding HKL = {hkl_min}"
        pinfo(INFO, 1)
        if RESOH > 0.11 and abs(RESOH - min_R) > 0.4 and nblock == 1:
            INFO = f"Warning: large difference between reported ({RESOH:.2f}) and calculated ({min_R:.2f}) resolution."
            pinfo(INFO, 1)
        resol[0] = min_R
        

    INFO = f"Max indices (Hmax={max_H:4d}  Kmax={max_K:4d}  Lmax={max_L:4d})"
    pinfo(INFO, 1)
    INFO = f"Min indices (Hmin={min_H:4d}  Kmin={min_K:4d}  Lmin={min_L:4d})"
    pinfo(INFO, 1)

    if sf.Fo_au:
        INFO = f"maximum value of amplitude = {max_F:.2f}"
        pinfo(INFO, 1)

        INFO = f"minimum value of amplitude = {min_F:.2f}"
        pinfo(INFO, 1)

        INFO = f"<F/sigmaF> = {f_over_sf / nf_Fo:.2lf}; <F>/<sigmaF> = {sum_f / sum_sf:.2lf};"
        pinfo(INFO, 1)
        if sum_f / sum_sf > 140 or sum_f / sum_sf < 4:
            INFO = f"Warning: Value of (Fo_avg/sigFo_avg = {sum_f / sum_sf:.2lf}) is out of range (check Fo or SigFo in SF file)."
            pinfo(INFO, 0)

    if sf.F2o:
        INFO = f"maximum value of F square = {max_F2:.2f}"
        pinfo(INFO, 1)
        INFO = f"minimum value of F square = {min_F2:.2f}"
        pinfo(INFO, 1)
        INFO = f"<F2/sigmaF2> = {f2_over_sf2 / nf_F2o:.2lf}; <F2>/<sigmaF2> = {sum_f2 / sum_sf2:.2lf};"
        pinfo(INFO, 1)

    if sf.Io:
        INFO = f"maximum value of intensity = {max_I:.2f}"
        pinfo(INFO, 1)
        INFO = f"minimum value of intensity = {min_I:.2f}"
        pinfo(INFO, 1)
        INFO = f"<I/sigmaI> = {i_over_si / nf_Io:.2lf}; <I>/<sigmaI> = {sum_i / sum_si:.2lf};"
        pinfo(INFO, 1)
        if sum_i / sum_si > 80 or sum_i / sum_si < 2:
            INFO = f"Warning: Value of (I_avg/sigI_avg = {sum_i / sum_si:.2lf}) is out of range (check Io or SigIo in SF file)."
            pinfo(INFO, 0)

        if f_over_sf / nf_Fo > 0 and (f_over_sf / nf_Fo > 2.5 * i_over_si / nf_Io or f_over_sf / nf_Fo < 1.0 * i_over_si / nf_Io):
            INFO = f"Warning: too much difference Fo/sigFo = {f_over_sf / nf_Fo:.2lf}; Io/sigIo = {i_over_si / nf_Io:.2lf};"
            pinfo(INFO, 0)

    if nnii > 10:
        INFO = f"Using all data: <I/sigI> = {ii_sigii / nnii:.2lf}"
        pinfo(INFO, 1)

        INFO = f"Using all data: <I>/<sigI> = {sum_ii / sum_sigii:.2lf}"
        pinfo(INFO, 1)

        INFO = f"Using all data: Rsig(<sigI>/<I>) = {sum_sigii / sum_ii:.3lf};"
        pinfo(INFO, 1)

        INFO = f"The maximum value of <I/sigI>_max = {ii_sigii_max:.2lf}"
        pinfo(INFO, 1)

    if nnii_low > 10:
        INFO = f"Use data with resolution >7.0 Angstrom: <I/sigI>_low = {ii_sigii_low / nnii_low:.2f}"
        pinfo(INFO, 1)

    return