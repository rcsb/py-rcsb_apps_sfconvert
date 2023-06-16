import math
from sf_file import SFFile

class ResolutionCalculator:
    def __init__(self, filename):
        self._sf_file = SFFile()
        self._sf_file.readFile(filename)
        self._initialize_data()

    def _initialize_data(self):
        self._initialize_refln_data()
        self._initialize_diffrn_refln_data()
        self._initialize_counts()
        self._initialize_columns()

    def _initialize_refln_data(self):
        self._refln_data = self._sf_file.getObj("refln")
        if self._refln_data is not None:
            self._rcell, self._cell = self.calc_cell_and_recip()

    def _initialize_diffrn_refln_data(self):
        self._diffrn_refln_data = self._sf_file.getObj("diffrn_refln")

    def _initialize_counts(self):
        if(self._refln_data):self._nref = self._refln_data.getRowCount()
        if(self._diffrn_refln_data):self._dnref = self._diffrn_refln_data.getRowCount()

    def _initialize_columns(self):

        attributes = {
            "index_h": "_H",
            "index_k": "_K",
            "index_l": "_L",
            "F_meas_au": "_Fo_au",
            "F_meas_sigma_au": "_sFo_au",
            "F_meas_sigma": "_sFo",
            "F_squared_sigma": "_sF2o",
            "pdbx_I_plus_sigma": "_sI_plus",
            "pdbx_I_minus_sigma": "_sI_minus",
            "pdbx_F_plus_sigma": "_sF_plus",
            "pdbx_F_minus_sigma": "_sF_minus",
            "F_meas": "_Fo",
            "F_squared_meas": "_F2o",
            "pdbx_I_plus": "_I_plus",
            "pdbx_I_minus": "_I_minus",
            "pdbx_F_plus": "_F_plus",
            "pdbx_F_minus": "_F_minus",
            "fom": "_fom",
            "phase_calc": "_phase_c",
            "phase_meas": "_phase_o",
        }

        for attr, var in attributes.items():
            if self._refln_data.hasAttribute(attr):
                setattr(self, var, self._refln_data.getColumn(self._refln_data.getIndex(attr)))
            else:
                setattr(self, var, None)


        diffrn_attributes = {
            "intensity_net": "_unmerge_i",
            "intensity_sigma": "_unmerge_si",
            "index_h": "_dH",
            "index_k": "_dK",
            "index_l": "_dL"
        }

        for attr, var in diffrn_attributes.items():
            if self._diffrn_refln_data and self._diffrn_refln_data.hasAttribute(attr):
                setattr(self, var, self._diffrn_refln_data.getColumn(self._diffrn_refln_data.getIndex(attr)))
            else:
                setattr(self, var, None)

        self._initialize_Io()
        self._initialize_sIo()
        self._initialize_status()

    def _initialize_Io(self):
        self._Io = self._refln_data.getColumn(self._refln_data.getIndex("intensity_meas")) if self._refln_data.hasAttribute("intensity_meas") else None

        if not self._Io:
            self._Io = self._refln_data.getColumn(self._refln_data.getIndex("intensity_meas_au")) if self._refln_data.hasAttribute("intensity_meas_au") else None
            if self._Io:
                self.cif_token_change("intensity_meas_au", "intensity_meas")

            if not self._Io:
                self._Io = self._refln_data.getColumn(self._refln_data.getIndex("intensity")) if self._refln_data.hasAttribute("intensity") else None
                if self._Io:
                    self.cif_token_change("intensity", "intensity_meas")

    def _initialize_sIo(self):
        self._sIo = self._refln_data.getColumn(self._refln_data.getIndex("intensity_sigma")) if self._refln_data.hasAttribute("intensity_sigma") else None
        if not self._sIo:
            self._sIo = self._refln_data.getColumn(self._refln_data.getIndex("intensity_sigma_au")) if self._refln_data.hasAttribute("intensity_sigma_au") else None
            if self._sIo:
                self.cif_token_change("intensity_sigma_au", "intensity_sigma")

            if not self._sIo:
                self._sIo = self._refln_data.getColumn(self._refln_data.getIndex("intensity_sigm")) if self._refln_data.hasAttribute("intensity_sigm") else None
                if self._sIo:
                    self.cif_token_change("intensity_sigm", "intensity_sigma")

                if not self._sIo:
                    self._sIo = self._refln_data.getColumn(self._refln_data.getIndex("intensity_meas_sigma")) if self._refln_data.hasAttribute("intensity_meas_sigma") else None
                    if self._sIo:
                        self.cif_token_change("intensity_meas_sigma", "intensity_sigma")

                    if not self._sIo:
                        self._sIo = self._refln_data.getColumn(self._refln_data.getIndex("intensity_meas_sigma_au")) if self._refln_data.hasAttribute("intensity_meas_sigma_au") else None
                        if self._sIo:
                            self.cif_token_change("intensity_meas_sigma_au", "intensity_sigma")

    def _initialize_status(self):
        self._status = self._refln_data.getColumn(self._refln_data.getIndex("status"))
        if not self._status:
            self._status = self._refln_data.getColumn(self._refln_data.getIndex("R_free_flag"))
            if self._status:
                self.cif_token_change("R_free_flag", "status")

            if not self._status:
                self._status = self._refln_data.getColumn(self._refln_data.getIndex("statu"))
                if self._status:
                    self.cif_token_change("statu", "status")

                if not self._status:
                    self._status = self._refln_data.getColumn(self._refln_data.getIndex("status_au"))
                    if self._status:
                        self.cif_token_change("status_au", "status")

    def calc_cell_and_recip(self):
        data = self._sf_file.getObj("cell")
        if data is not None:
            a = float(data.getValue("length_a"))
            b = float(data.getValue("length_b"))
            c = float(data.getValue("length_c"))
            alpha = float(data.getValue("angle_alpha"))
            beta = float(data.getValue("angle_beta"))
            gamma = float(data.getValue("angle_gamma"))

            cell = [a, b, c, alpha, beta, gamma]
            
            rcell = [0.0] * 6

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

            # Print the reciprocal cell
            return rcell, cell
        else:
            print("No cell data found in the mmCIF file.")

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

    def calc_resolution(self):
        refln_data = self._sf_file.getObj("refln")
        if refln_data is not None:
            rcell, cell = self.calc_cell_and_recip()

            best_resolution = 0.0
            n = refln_data.getRowCount()

            for i in range(n):
                h = int(refln_data.getValue("index_h", i))
                k = int(refln_data.getValue("index_k", i))
                l = int(refln_data.getValue("index_l", i))

                resolution = self.get_resolution(h, k, l, rcell)

                if resolution > best_resolution:
                    best_resolution = resolution

            # Print the best resolution
            print("Best Resolution: {:.2f} Angstroms".format(best_resolution))
        else:
            print("No refln data found in the mmCIF file.")

    def cif_token_change(self, old_token, new_token):
        print(f"Warning! The mmcif token  _refln.{old_token} is wrong!")
        print(f"It has been corrected as _refln.{new_token}")

    def check_sf(self, nblock):

        temp_nref, nstart, n1, n2, n4, n5, nfpairF, nfpairI, nf_sFo, nf_sIo, key = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        sum_sigii, ii_sigii, ii_sigii_low, nnii, sum_ii, nnii_low, nfp, nfn, nip, nin, n_obs, n_free = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        max_H, min_H, max_K, min_K, max_L, min_L, nblock = -500, 500, -500, 500, -500, 500, None
        max_F, min_F, max_I, min_I = -500000.0, 500000.0, -5000000.0, 5000000.0
        max_R, min_R, max_F2, min_F2 = -500.0, 900.0, -500000.0, 500000.0
        ii_sigii_max = -90000
        resolution = 0

        resol = [100]
        RESOH = 0.1
        RESOL = 200


        
        if not (self._dH or self._dK or self._dL or self._H or self._K or self._L):
            print(f"Error: File has no 'index_h, index_k, index_l' (data block={nblock}).")
            return
        
        if not (self._Fo_au or self._Fo or self._Io or self._F2o or self._I_plus or self._I_minus or
                self._F_plus or self._F_minus or self._unmerge_i or self._unmerge_si):
            print(f"Error: File has no mandatory items 'F/I/F+/F-/I+/I-' (data block={nblock}). ")
            return

        if self._nref < 30 and self._dnref > 30:
            return  # do not further check the unmerged data!!
        
        if self._nref < 30:
            print(f"Error: File has too few reflections ({self._nref}) (data block={nblock}).")
            return

        if ((self._Fo_au and not self._sFo_au) or (self._Fo and not self._sFo) or
            (self._Io and not self._sIo) or (self._F2o and not self._sF2o) or
            (self._I_plus and not self._sI_plus) or (self._I_minus and not self._sI_minus) or
            (self._F_plus and not self._sF_plus) or (self._F_minus and not self._sF_minus) or
            (self._unmerge_i and not self._unmerge_si)):

            print(f"Error: Sigma values are missing (data block={nblock})!")

        if self._status is None:
            print(f"Error: File has no free set (data block={nblock}).")


        refln_data = self._sf_file.getObj("refln")
        if refln_data is not None:
            rcell, cell = self.calc_cell_and_recip()

        if (cell[0] > 0.01 and cell[1] > 0.01): key = 1


        
        for i in range(nstart, self._nref):  # check data items
            #print(f"Checking reflection {i} of {self._nref} (data block={nblock})")
            ah = int(self._H[i])
            ak = int(self._K[i])
            al = int(self._L[i])

            min_H = min(min_H, ah)
            min_K = min(min_K, ak)
            min_L = min(min_L, al)

            max_H = max(max_H, ah)
            max_K = max(max_K, ak)
            max_L = max(max_L, al)

            if not ((self._Fo_au and self._Fo_au[i] != '?') or
                    (self._Io and self._Io[i] != '?') or
                    (self._I_plus and self._I_plus[i] != '?') or
                    (self._I_minus and self._I_minus[i] != '?') or
                    (self._F_plus and self._F_plus[i] != '?') or
                    (self._F_minus and self._F_minus[i] != '?') or
                    (self._unmerge_i and self._unmerge_i[i] != '?') or
                    (self._F2o and self._F2o[i] != '?') or
                    (self._Fo and self._Fo[i] != '?')):
                continue

            temp_nref += 1
            hkl = f"HKL={ah:4d} {ak:4d} {al:4d}"

            

            if ((ah == 0 and ak == 0 and al == 0) or
                    (abs(ah) > 800 or abs(ak) > 800 or abs(al) > 800)):
                if n1 == 1:
                    print(f"Error: File has wrong indices ({hkl}).")
                    n1 += 1

            if self._sFo_au and i > 0 and float(self._sFo_au[i - 1]) == float(self._sFo_au[i]):
                nf_sFo += 1
            if self._sIo and i > 0 and float(self._sIo[i - 1]) == float(self._sIo[i]):
                nf_sIo += 1

            if self._F_plus:
                f = float(self._F_plus[i])
                nfpairF += 1
                if f < 0 and self._n4 == 1:
                    print(f"Error: File has negative amplitude (F+: {self._F_plus[i]}) for ({hkl}).")
                    n4 += 1

            if self._I_plus:
                nfpairI += 1
                f = float(self._I_plus[i])

            # Rest of the code would go here
            if key > 0:
                resolution = self.get_resolution(ah, ak, al, self._rcell)
                min_R = min(min_R, resolution)
                max_R = max(max_R, resolution)
                if min_R == resolution:
                    self._hkl_min = f"{ah:4d} {ak:4d} {al:4d}"
                if max_R == resolution:
                    self._hkl_max = f"{ah:4d} {ak:4d} {al:4d}"

                val = 0
                sval = 0
                if self._Io and self._sIo and self._sIo[i] != '?':
                    val = float(self._Io[i])
                    sval = float(self._sIo[i])
                elif self._Fo_au and self._sFo_au and self._sFo_au[i] != '?':
                    val = float(self._Fo_au[i]) * float(self._Fo_au[i])
                    sval = 2 * float(self._Fo_au[i]) * float(self._sFo_au[i])
                elif self._F2o and self._sFo and self._sF2o[i] != '?':
                    val = float(self._F2o[i])
                    sval = float(self._sF2o[i])
                elif self._Fo and self._sFo and self._sFo[i] != '?':
                    val = float(self._Fo[i]) * float(self._Fo[i])
                    sval = 2 * float(self._Fo[i]) * float(self._sFo[i])


                if sval > 0:
                    sum_sigii += sval
                    sum_ii += val
                    ratio = val / sval
                    ii_sigii += ratio
                    if resolution > 7.0:  # low resolution I/sigI
                        ii_sigii_low += ratio
                        nnii_low += 1
                    if ratio > ii_sigii_max:
                        ii_sigii_max = ratio
                    nnii += 1

            # print("Resolution: ", resolution, " ", "RESOL: ", RESOL, " ", "RESOH: ", RESOH)
            # print(f"{RESOL} + 0.01 >= {resolution} >= {RESOH} - 0.01")
            if RESOL + 0.01 >= resolution >= RESOH - 0.01:  # for onedep
                if self._F_plus and not '?' in self._F_plus[i]:
                    nfp += 1
                if self._F_minus and not '?' in self._F_minus[i]:
                    nfn += 1
                if self._I_plus and not '?' in self._I_plus[i]:
                    nip += 1
                if self._I_minus and not '?' in self._I_minus[i]:
                    nin += 1

                if ((self._Fo and not '?' in self._Fo[i]) or
                        (self._Fo_au and not '?' in self._Fo_au[i]) or
                        (self._Io and not '?' in self._Io[i]) or
                        (self._F2o and not '?' in self._F2o[i]) or
                        ((self._F_plus and not '?' in self._F_plus[i]) or
                        (self._F_minus and not '?' in self._F_minus[i])) or
                        ((self._I_plus and not '?' in self._I_plus[i]) or
                        (self._I_minus and not '?' in self._I_minus[i]))):
                    if self._status and 'o' in self._status[i]:
                        n_obs += 1
                    elif self._status and 'f' in self._status[i]:
                        n_free += 1


            # print("the resolution %.2f %.2f %ld\n", RESOH, RESOL, i)

            f_over_sf, sum_f, sum_sf, nf_Fo = 0, 0, 0, 0
            f2_over_sf2, sum_f2, sum_sf2, nf_F2o = 0, 0, 0, 0

        
            if self._Fo_au:
                f = float(self._Fo_au[i])
                if f < 0 and self._n5 == 0:
                    self._n5 += 1
                    print(f"Error: File has negative amplitude (Fo: {self._Fo_au[i]}) for ({hkl}).")


                if f < min_F: min_F = f
                if f > max_F: max_F = f

                if self._sFo_au:
                    sigf = float(self._sFo_au[i])
                    if sigf > 0 and self._sFo_au[i] != '?':
                        f_over_sf += f / sigf
                        sum_f += f
                        sum_sf += sigf
                        nf_Fo += 1

            if self._F2o:
                f = float(self._F2o[i])
                if f < min_F2: min_F2 = f
                if f > max_F2: max_F2 = f

                if self._sF2o:
                    sigf = float(self._sF2o[i])
                    if sigf > 0 and self._sF2o[i] != '?':
                        f2_over_sf2 += f / sigf
                        sum_f2 += f
                        sum_sf2 += sigf
                        nf_F2o += 1

            i_over_si, sum_i, sum_si, nf_Io, n6, n7, n8 = 0, 0, 0, 0, 0, 0, 0

            if self._Io:
                f = float(self._Io[i])
                if f < min_I: min_I = f
                if f > max_I: max_I = f

                if self._sIo:
                    sigf = float(self._sIo[i])
                    if sigf > 0 and self._sIo[i] != '?':
                        i_over_si += f / sigf
                        sum_i += f
                        sum_si += sigf
                        nf_Io += 1

            if self._fom and abs(float(self._fom[i])) > 1.01:
                if n6 == 0:
                    n6 += 1
                    print(f"Warning: File has wrong values of FOM ({self._fom[i]}) for ({hkl}).")
            if self._phase_c and abs(float(self._phase_c[i])) > 361.0:
                if n7 == 0:
                    n7 += 1
                    print(f"Warning: File has wrong values of phase ({self._phase_c[i]}) for ({hkl}).")
            if self._phase_o and abs(float(self._phase_o[i])) > 361.0:
                if n8 == 0:
                    n8 += 1
                    print(f"Warning: File has wrong values of phase ({self._phase_o[i]}) for ({hkl}).")


        if n1 > 0:
            print(f"Error: File has ({n1}) reflections with wrong indices.")

        if n2 > 0:
            print(f"Warning: File has ({n2}) reflections with negative SIGMA, (Corrected: given status '<').")

        if n4 > 0:
            print(f"Error: File has ({n4}) reflections with negative amplitude (F+).")

        if n5 > 0:
            print(f"Error: File has ({n5}) reflections with negative amplitude (Fo).")

        if temp_nref > 10 and ((nf_sFo > 0 and temp_nref - nf_sFo < 3) or (nf_sIo > 0 and temp_nref - nf_sIo < 3)):
            print(f"Warning! File has Sigma_Fo all the same!")

        # Following are the messages related to total number of reflections
        print(f"Total number of observed reflections = {(n_obs + n_free)}")
        print(f"Total number of observed reflections (status='o') = {n_obs}")
        print(f"Total number of observed reflections (status='f') = {n_free}")
        if n_obs > 0:
            rfree_p = 100 * float(n_free) / float(n_obs)
            print(f"Percentage for free set = {rfree_p:.2f}")

        if nfpairF > 10:
            print(f"Total number of Friedel pairs (F+/F-) = {nfpairF}")
            print(f"Total number of observed F+ = {nfp}")
            print(f"Total number of observed F- = {nfn}")
            print(f"Sum of observed F+ and F-  = {(nfn + nfp)}")
        
        if nfpairI > 10:
            print(f"Total number of Friedel pairs (I+/I-) = {nfpairI}")
            print(f"Total number of observed I+ = {nip}")
            print(f"Total number of observed I- = {nin}")
            print(f"Sum of observed I+ and I-  = {(nin + nip)}")
        
 


        if key > 0 and self._cell[0] > 0.001:
            print(f"Cell = {self._cell[0]:.2f} {self._cell[1]:.2f} {self._cell[2]:.2f} {self._cell[3]:.2f} {self._cell[4]:.2f} {self._cell[5]:.2f}")
            print(f"Lowest resolution= {max_R:.2f} ; corresponding HKL={self._hkl_max}")
            print(f"Highest resolution={min_R:.2f} ; corresponding HKL={self._hkl_min}")
            if RESOH > 0.11 and abs(RESOH - min_R) > 0.4 and nblock == 1:
                print(f"Warning: large difference between reported ({RESOH:.2f}) and calculated({min_R:.2f}) resolution.")
            resol[0] = min_R
        
        print(f"Max indices (Hmax={max_H:4d}  Kmax={max_K:4d}  Lmax={max_L:4d})")
        print(f"Min indices (Hmin={min_H:4d}  Kmin={min_K:4d}  Lmin={min_L:4d})")

        if self._Fo_au:
            print(f"maximum value of amplitude= {max_F:.2f}")
            print(f"minimum value of amplitude= {min_F:.2f}")
            print(f"<F/sigmaF> = {f_over_sf / nf_Fo:.2f};  <F>/<sigmaF> = {sum_f / sum_sf:.2f}")
            if sum_f / sum_sf > 140 or sum_f / sum_sf < 4:
                print(f"Warning: Value of (Fo_avg/sigFo_avg = {sum_f / sum_sf:.2f}) is out of range (check Fo or SigFo in SF file).")

        if self._F2o:
            print(f"maximum value of F square= {max_F2:.2f}")
            print(f"minimum value of F square= {min_F2:.2f}")
            print(f"<F2/sigmaF2> = {f2_over_sf2 / nf_F2o:.2f};  <F2>/<sigmaF2> = {sum_f2 / sum_sf2:.2f}")

        if self._Io:
            print(f"maximum value of intensity= {max_I:.2f}")
            print(f"minimum value of intensity= {min_I:.2f}")
            print(f"<I/sigmaI> = {i_over_si / nf_Io:.2f};  <I>/<sigmaI> = {sum_i / sum_si:.2f}")
            if sum_i / sum_si > 80 or sum_i / sum_si < 2:
                print(f"Warning: Value of (I_avg/sigI_avg = {sum_i / sum_si:.2f}) is out of range (check Io or SigIo in SF file). ")
            if f_over_sf / nf_Fo > 0 and (f_over_sf / nf_Fo > 2.5 * i_over_si / nf_Io or f_over_sf / nf_Fo < 1.0 * i_over_si / nf_Io):
                print(f"Warning: too much difference Fo/sigFo = {f_over_sf / nf_Fo:.2f};  Io/sigIo = {i_over_si / nf_Io:.2f}")


        if nnii > 10:
            print(f"Using all data:  <I/sigI>={ii_sigii / nnii:.2f}")
            print(f"Using all data:  <I>/<sigI>={sum_ii / sum_sigii:.2f}")
            print(f"Using all data:  Rsig(<sigI>/<I>)={sum_sigii / sum_ii:.3f}")
            print(f"The maximum value of <I/sigI>_max={ii_sigii_max:.2f}")

        if nnii_low > 10:
            print(f"Use data with resolution >7.0 Angstrom: <I/sigI>_low={ii_sigii_low / nnii_low:.2f}")

        return









filename = "1o08-sf.cif"  # Specify the mmCIF file you want to read
calculator = ResolutionCalculator(filename)
sf_file = SFFile()
sf_file.readFile(filename)
block_name = "r1o08sf"
block_number, block = sf_file.getBlock(block_name)
calculator.check_sf(block_number)
