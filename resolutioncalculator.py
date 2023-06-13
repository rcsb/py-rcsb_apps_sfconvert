import math

class ResolutionCalculator:
    def __init__(self):
        self.__PDBID = "" * 80
        self.__RESOH = 0.0
        self.__RESOL = 0.0
        self.__CELL = [0.0] * 6
        self.__a = self.__b = self.__c = None
        self.__alpha = self.__beta = self.__gamma = None
        #self.__sg = self.__nsg = None
        #self.__wavelength = self.__symm = self.__resh = self.__resl = self.__nobs = None
        #self.__hmax = self.__kmax = self.__lmax = self.__hmin = self.__kmin = self.__lmin = self.__nall = None
        self.__H = self.__K = self.__L = self.__Fo = self.__sFo = self.__Fo_au = self.__sFo_au = None
        #self.__Fc = self.__Fc_au = None
        self.__Io = self.__sIo = self.__F2o = self.__sF2o = None
        #self.__Ic = self.__F2c = None
        self.__fom = self.__phase_c = self.__phase_o = self.__status = None
        #self.__flag = self.__free1 = self.__free2 = None
        #self.__wave_id = self.__cryst_id = self.__scale_id = self.__diffr_id = None
        self.__I_plus = self.__sI_plus = self.__I_minus = self.__sI_minus = None
        self.__F_plus = self.__sF_plus = self.__F_minus = self.__sF_minus = None
        #self.__hla = self.__hlb = self.__hlc = self.__hld = None
        #self.__hla1 = self.__hlb1 = self.__hlc1 = self.__hld1 = self.__anom = self.__anoms = None
        #self.__aud_id = self.__aud_date = self.__aud_rec = self.__aud_meth = None
        #self.__dif_id = self.__dif_cid = self.__dif_detail = self.__temp = self.__treat = None
        #self.__d_spacing = self.__a_calc = self.__b_calc = self.__weighted = self.__fs_uncorrected = None
        #self.__f_uncorrected = self.__gsas_i100_meas = self.__i_unknown = self.__is_unknown = None
        #self.__phase_part = self.__F_part_au = self.__phase_with = self.__fcalc_with = None
        #self.__Fc_all = self.__Fc_all_ph = self.__fwt = self.__phwt = self.__delfwt = self.__delphwt = None
        #self.__fib_co = self.__fib_fo = self.__fib_ly = self.__wt = None
        #self.__pow_sc = self.__pow_io = self.__pow_iop = self.__pow_wt = self.__pow_ic = self.__pow_ict = None
        self.__dH = self.__dK = self.__dL = self.__unmerge_i = self.__unmerge_si = None
        #self.__unmerge_angle_phi = None
        #self.__unmerge_std_code = self.__unmerge_scale_group = None
        self.__nref = self.__dnref = None
        #self.__nwave = self.__nsymm = self.__naud = self.__ndif = self.__npow = None

    def get_resolution(self, h, k, l, rcell):
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

    def pinfo(self, info, id):
        # Write all the log information about the SF file
        if "Warning" in info or "Error" in info:
            self.FTMP1.write(info + "\n")
            print(info)
        else:
            if id == 0:
                self.FTMP2.write(info + "\n")
                print(info)
            elif id == 1:
                self.FTMP2.write(info + "\n")
            elif id == 2:
                print(info)

    def check_cell(self, cell, nblock):
        if self.__a and self.__b and self.__c and self.__alpha and self.__beta and self.__gamma:
            cell[0] = float(self.__a)
            cell[1] = float(self.__b)
            cell[2] = float(self.__c)
            cell[3] = float(self.__alpha)
            cell[4] = float(self.__beta)
            cell[5] = float(self.__gamma)

            if self.__CELL[0] > 0.01 and nblock == 0 and (
                abs(cell[0] - self.__CELL[0]) > 0.1 or abs(cell[1] - self.__CELL[1]) > 0.1 or abs(cell[2] - self.__CELL[2]) > 0.1 or
                abs(cell[3] - self.__CELL[3]) > 0.1 or abs(cell[4] - self.__CELL[4]) > 0.1 or abs(cell[5] - self.__CELL[5]) > 0.1
            ):
                INFO = "Warning! SF and PDB ({0} nblock={1}) cell values mismatch.".format(self.__PDBID, nblock + 1)
                self.pinfo(INFO, 0)

                if (
                    abs(cell[0] - self.__CELL[0]) > 3.0 or abs(cell[1] - self.__CELL[1]) > 3.0 or abs(cell[2] - self.__CELL[2]) > 3.0 or
                    abs(cell[3] - self.__CELL[3]) > 3.0 or abs(cell[4] - self.__CELL[4]) > 3.0 or abs(cell[5] - self.__CELL[5]) > 3.0
                ):
                    INFO = "Error: ({0} nblock={1}) large cell value mismatch (>3.0).".format(self.__PDBID, nblock + 1)
                    print("cell in sf: {0:6.2f} {1:6.2f} {2:6.2f} {3:6.2f} {4:6.2f} {5:6.2f}".format(
                        cell[0], cell[1], cell[2], cell[3], cell[4], cell[5]
                    ))
                    print("cell in PDB: {0:6.2f} {1:6.2f} {2:6.2f} {3:6.2f} {4:6.2f} {5:6.2f}".format(
                        self.__CELL[0], self.__CELL[1], self.__CELL[2], self.__CELL[3], self.__CELL[4], self.__CELL[5]
                    ))

                    self.pinfo(INFO, 0)

        elif (
            self.__CELL[0] > 0.01 and self.__CELL[1] > 0.01 and self.__CELL[2] > 0.01 and
            self.__CELL[3] > 0.01 and self.__CELL[4] > 0.01 and self.__CELL[5] > 0.01
        ):
            cell[0] = self.__CELL[0]
            cell[1] = self.__CELL[1]
            cell[2] = self.__CELL[2]
            cell[3] = self.__CELL[3]
            cell[4] = self.__CELL[4]
            cell[5] = self.__CELL[5]
       
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

    def check_sf(self, j, resol):
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
        n=self.__nref
        file = self.__PDBID

        self.check_cell(cell, j) #get cell for block j
        
        mess = "Warning:"
        if j == 0: 
            mess = "Error:"
        
        if not (self.__H or self.__K or self.__L or self.__dH or self.__dK or self.__dL):
            INFO = f"{mess} File ({file}) has no 'index_h, index_k, index_l' (data block={nblock})."
            self.pinfo(INFO, 0)
            return


        if not (self.__Fo_au or self.__Fo or self.__Io or self.__F2o or self.__I_plus or self.__I_minus or self.__F_plus or self.__F_minus or self.__unmerge_i or self.__unmerge_si):
            INFO = f"{mess} File ({file}) has no mandatory items 'F/I/F+/F-/I+/I-' (data block={nblock})."
            self.pinfo(INFO, 0)
            return

        if n < 30 and self.__dnref > 30:
            return  # do not further check the unmerged data!!

        if n < 30:
            INFO = f"Error:  File ({file}) has too few reflections ({n}) (data block={nblock})."
            self.pinfo(INFO, 0)
            return

        if (self.__Fo_au and not self.__sFo_au) or (self.__Fo and not self.__sFo) or (self.__Io and not self.__sIo) or (self.__F2o and not self.__sF2o) or (self.__I_plus and not self.__sI_plus) or (self.__I_minus and not self.__sI_minus) or (self.__F_plus and not self.__sF_plus) or (self.__F_minus and not self.__sF_minus) or (self.__unmerge_i and not self.__unmerge_si):
            INFO = f"Warning: File ({file}) sigma values are missing (data block={nblock})!"
            self.pinfo(INFO, 0)

        if j == 0 and not self.__status:
            INFO = f"Warning: File ({file}) has no free set (data block={nblock})."
            self.pinfo(INFO, 0)

        if cell[0] > 0.01 and cell[1] > 0.01:
            key = 1
            self.calc_recip_cell(cell, rcell)


        for i in range(nstart, n):
            ah = int(self.__H[i])
            ak = int(self.__K[i])
            al = int(self.__L[i])

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

            if not ((self.__Fo_au and self.__Fo_au[i][0] != '?') or (self.__Io and self.__Io[i][0] != '?') or
                    (self.__I_plus and self.__I_plus[i][0] != '?') or (self.__I_minus and self.__I_minus[i][0] != '?') or
                    (self.__F_plus and self.__F_plus[i][0] != '?') or (self.__F_minus and self.__F_minus[i][0] != '?') or
                    (self.__unmerge_i and self.__unmerge_i[i][0] != '?') or
                    (self.__F2o and self.__F2o[i][0] != '?') or (self.__Fo and self.__Fo[i][0] != '?')):
                continue

            nref += 1

            hkl = f"HKL={ah:4d} {ak:4d} {al:4d}"

            if (ah == 0 and ak == 0 and al == 0) or (abs(ah) > 800 or abs(ak) > 800 or abs(al) > 800):
                n1 += 1
                if n1 == 1:
                    INFO = f"Error: File ({file}) has wrong indices ({hkl})."
                    self.pinfo(INFO, 0)

            if self.__sFo_au and i > 0 and float(self.__sFo_au[i - 1]) == float(self.__sFo_au[i]):
                nf_sFo += 1
            if self.__sIo and i > 0 and float(self.__sIo[i - 1]) == float(self.__sIo[i]):
                nf_sIo += 1

            if self.__F_plus:
                f = float(self.__F_plus[i])
                nfpairF += 1
                if f < 0 and n4 == 1:
                    n4 += 1
                    INFO = f"Error: File ({file}) has negative amplitude (F+: {self.__F_plus[i]}) for ({hkl})."
                    self.pinfo(INFO, 0)

            if self.__I_plus:
                nfpairI += 1
                f = float(self.__I_plus[i])

            if key > 0:
                resolution = self.get_resolution(ah, ak, al, rcell)
                if resolution < min_R:
                    min_R = resolution
                    hkl_min = f"{ah:4d} {ak:4d} {al:4d}"
                if resolution > max_R:
                    max_R = resolution
                    hkl_max = f"{ah:4d} {ak:4d} {al:4d}"
                
                val = 0
                sval = 0
                if self.__Io and self.__sIo and self.__sIo[i][0] != '?':
                    val = float(self.__Io[i])
                    sval = float(self.__sIo[i])
                elif self.__Fo_au and self.__sFo_au and self.__sFo_au[i][0] != '?':
                    val = float(self.__Fo_au[i]) * float(self.__Fo_au[i])
                    sval = 2 * float(self.__Fo_au[i]) * float(self.__sFo_au[i])
                elif self.__F2o and self.__sFo and self.__sF2o[i][0] != '?':
                    val = float(self.__F2o[i])
                    sval = float(self.__sF2o[i])
                elif self.__Fo and self.__sFo and self.__sFo[i][0] != '?':
                    val = float(self.__Fo[i]) * float(self.__Fo[i])
                    sval = 2 * float(self.__Fo[i]) * float(self.__sFo[i])

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

            if resolution <= self.__RESOL + 0.01 and resolution >= self.__RESOH - 0.01:
                if self.__F_plus and '?' not in self.__F_plus[i]:
                    nfp += 1
                if self.__F_minus and '?' not in self.__F_minus[i]:
                    nfn += 1
                if self.__I_plus and '?' not in self.__I_plus[i]:
                    nip += 1
                if self.__I_minus and '?' not in self.__I_minus[i]:
                    nin += 1

                if (self.__Fo and '?' not in self.__Fo[i]) or (self.__Fo_au and '?' not in self.__Fo_au[i]) or (self.__Io and '?' not in self.__Io[i]) or (self.__F2o and '?' not in self.__F2o[i]) or ((self.__F_plus and '?' not in self.__F_plus[i]) or (self.__F_minus and '?' not in self.__F_minus[i])) or ((self.__I_plus and '?' not in self.__I_plus[i]) or (self.__I_minus and '?' not in self.__I_minus[i])):
                    if self.__status and 'o' in self.__status[i]:
                        n_obs += 1
                    elif self.__status and 'f' in self.__status[i]:
                        n_free += 1

            #    print(f"the resolution {RESOH:.2f} {RESOL:.2f} {i}")

            if self.__Fo_au:
                f = float(self.__Fo_au[i])
                if f < 0 and n5 == 1:
                    n5 += 1
                    INFO = f"Error: File ({file}) has negative amplitude (Fo: {self.__Fo_au[i]}) for ({hkl})."
                    self.pinfo(INFO, 0)

                if f < min_F:
                    min_F = f
                if f > max_F:
                    max_F = f

                if self.__sFo_au:
                    sigf = float(self.__sFo_au[i])
                    if sigf > 0 and '?' not in self.__sFo_au[i]:
                        f_over_sf += f / sigf
                        sum_f += f
                        sum_sf += sigf
                        nf_Fo += 1

            if self.__F2o:
                f = float(self.__F2o[i])
                if f < min_F2:
                    min_F2 = f
                if f > max_F2:
                    max_F2 = f
                if self.__sF2o:
                    sigf = float(self.__sF2o[i])
                    if sigf > 0 and '?' not in self.__sF2o[i]:
                        f2_over_sf2 += f / sigf
                        sum_f2 += f
                        sum_sf2 += sigf
                        nf_F2o += 1

            if self.__Io:
                f = float(self.__Io[i])
                if f < min_I:
                    min_I = f
                if f > max_I:
                    max_I = f
                if self.__sIo:
                    sigf = float(self.__sIo[i])
                    if sigf > 0 and '?' not in self.__sIo[i]:
                        i_over_si += f / sigf
                        sum_i += f
                        sum_si += sigf
                        nf_Io += 1

            if self.__fom and abs(float(self.__fom[i])) > 1.01:
                if n6 == 1:
                    n6 += 1
                    INFO = f"Warning: File ({file}) has wrong values of FOM ({self.__fom[i]}) for ({hkl})."
                    self.pinfo(INFO, 0)
            if self.__phase_c and abs(float(self.__phase_c[i])) > 361.0:
                if n7 == 1:
                    n7 += 1
                    INFO = f"Warning: File ({file}) has wrong values of phase ({self.__phase_c[i]}) for ({hkl})."
                    self.pinfo(INFO, 0)
            if self.__phase_o and abs(float(self.__phase_o[i])) > 361.0:
                if n8 == 1:
                    n8 += 1
                    INFO = f"Warning: File ({file}) has wrong values of phase ({self.__phase_o[i]}) for ({hkl})."
                    self.pinfo(INFO, 0)


        if n1 > 0:
            INFO = f"Error: File ({file}) has ({n1}) reflections with wrong indices."
            self.pinfo(INFO, 0)

        if n2 > 0:
            INFO = f"Warning: File ({file}) has ({n2}) reflections with negative SIGMA, (Corrected: given status '<')."
            self.pinfo(INFO, 0)

        if n4 > 0:
            INFO = f"Error: File ({file}) has ({n4}) reflections with negative amplitude (F+)."
            self.pinfo(INFO, 0)

        if n5 > 0:
            INFO = f"Error: File ({file}) has ({n5}) reflections with negative amplitude (Fo)."
            self.pinfo(INFO, 0)

        if nref > 10 and ((nf_sFo > 0 and nref - nf_sFo < 3) or (nf_sIo > 0 and nref - nf_sIo < 3)):
            INFO = f"Warning! File ({file}) has Sigma_Fo all the same!"
            self.pinfo(INFO, 0)

        INFO = f"Total number of observed reflections = {(n_obs + n_free)}"
        self.pinfo(INFO, 1)

        INFO = f"Total number of observed reflections (status='o') = {n_obs}"
        self.pinfo(INFO, 1)

        INFO = f"Total number of observed reflections (status='f') = {n_free}"
        self.pinfo(INFO, 1)

        if n_obs > 0:
            rfree_p = 100 * float(n_free) / float(n_obs)
            INFO = f"Percentage for free set = {rfree_p:.2f}"
            self.pinfo(INFO, 1)

        if nfpairF > 10:
            INFO = f"Total number of Friedel pairs (F+/F-) = {nfpairF}"
            self.pinfo(INFO, 1)
            INFO = f"Total number of observed F+ = {nfp}"
            self.pinfo(INFO, 1)
            INFO = f"Total number of observed F- = {nfn}"
            self.pinfo(INFO, 1)
            INFO = f"Sum of observed F+ and F- = {nfn + nfp}"
            self.pinfo(INFO, 1)

        if nfpairI > 10:
            INFO = f"Total number of Friedel pairs (I+/I-) = {nfpairI}"
            self.pinfo(INFO, 1)
            INFO = f"Total number of observed I+ = {nip}"
            self.pinfo(INFO, 1)
            INFO = f"Total number of observed I- = {nin}"
            self.pinfo(INFO, 1)
            INFO = f"Sum of observed I+ and I- = {nin + nip}"
            self.pinfo(INFO, 1)

        if key > 0 and cell[0] > 0.001:
            INFO = f"Cell = {cell[0]:.2f} {cell[1]:.2f} {cell[2]:.2f} {cell[3]:.2f} {cell[4]:.2f} {cell[5]:.2f}"
            self.pinfo(INFO, 1)

            INFO = f"Lowest resolution = {max_R:7.2f}; corresponding HKL = {hkl_max}"
            self.pinfo(INFO, 1)
            INFO = f"Highest resolution = {min_R:7.2f}; corresponding HKL = {hkl_min}"
            self.pinfo(INFO, 1)
            if self.__RESOH > 0.11 and abs(self.__RESOH - min_R) > 0.4 and nblock == 1:
                INFO = f"Warning: large difference between reported ({self.__RESOH:.2f}) and calculated ({min_R:.2f}) resolution."
                self.pinfo(INFO, 1)
            resol[0] = min_R
            

        INFO = f"Max indices (Hmax={max_H:4d}  Kmax={max_K:4d}  Lmax={max_L:4d})"
        self.pinfo(INFO, 1)
        INFO = f"Min indices (Hmin={min_H:4d}  Kmin={min_K:4d}  Lmin={min_L:4d})"
        self.pinfo(INFO, 1)

        if self.__Fo_au:
            INFO = f"maximum value of amplitude = {max_F:.2f}"
            self.pinfo(INFO, 1)

            INFO = f"minimum value of amplitude = {min_F:.2f}"
            self.pinfo(INFO, 1)

            INFO = f"<F/sigmaF> = {f_over_sf / nf_Fo:.2lf}; <F>/<sigmaF> = {sum_f / sum_sf:.2lf};"
            self.pinfo(INFO, 1)
            if sum_f / sum_sf > 140 or sum_f / sum_sf < 4:
                INFO = f"Warning: Value of (Fo_avg/sigFo_avg = {sum_f / sum_sf:.2lf}) is out of range (check Fo or SigFo in SF file)."
                self.pinfo(INFO, 0)

        if self.__F2o:
            INFO = f"maximum value of F square = {max_F2:.2f}"
            self.pinfo(INFO, 1)
            INFO = f"minimum value of F square = {min_F2:.2f}"
            self.pinfo(INFO, 1)
            INFO = f"<F2/sigmaF2> = {f2_over_sf2 / nf_F2o:.2lf}; <F2>/<sigmaF2> = {sum_f2 / sum_sf2:.2lf};"
            self.pinfo(INFO, 1)

        if self.__Io:
            INFO = f"maximum value of intensity = {max_I:.2f}"
            self.pinfo(INFO, 1)
            INFO = f"minimum value of intensity = {min_I:.2f}"
            self.pinfo(INFO, 1)
            INFO = f"<I/sigmaI> = {i_over_si / nf_Io:.2lf}; <I>/<sigmaI> = {sum_i / sum_si:.2lf};"
            self.pinfo(INFO, 1)
            if sum_i / sum_si > 80 or sum_i / sum_si < 2:
                INFO = f"Warning: Value of (I_avg/sigI_avg = {sum_i / sum_si:.2lf}) is out of range (check Io or SigIo in SF file)."
                self.pinfo(INFO, 0)

            if f_over_sf / nf_Fo > 0 and (f_over_sf / nf_Fo > 2.5 * i_over_si / nf_Io or f_over_sf / nf_Fo < 1.0 * i_over_si / nf_Io):
                INFO = f"Warning: too much difference Fo/sigFo = {f_over_sf / nf_Fo:.2lf}; Io/sigIo = {i_over_si / nf_Io:.2lf};"
                self.pinfo(INFO, 0)

        if nnii > 10:
            INFO = f"Using all data: <I/sigI> = {ii_sigii / nnii:.2lf}"
            self.pinfo(INFO, 1)

            INFO = f"Using all data: <I>/<sigI> = {sum_ii / sum_sigii:.2lf}"
            self.pinfo(INFO, 1)

            INFO = f"Using all data: Rsig(<sigI>/<I>) = {sum_sigii / sum_ii:.3lf};"
            self.pinfo(INFO, 1)

            INFO = f"The maximum value of <I/sigI>_max = {ii_sigii_max:.2lf}"
            self.pinfo(INFO, 1)

        if nnii_low > 10:
            INFO = f"Use data with resolution >7.0 Angstrom: <I/sigI>_low = {ii_sigii_low / nnii_low:.2f}"
            self.pinfo(INFO, 1)

        return