import math
import os
import argparse
from sf_convert_project.src.sf_convert.sffile.sf_file import SFFile
#from ..sffile.sf_file import SFFile
from sf_convert_project.src.sf_convert.utils.pinfo_file import pinfo
#from .pinfo_file import pinfo
from mmcif.api.DataCategory import DataCategory
from mmcif.api.PdbxContainers import DataContainer
from mmcif.io.PdbxWriter import PdbxWriter

class CheckSfFile:
    def __init__(self, sffile, fout_path, pinfo_value = 0):
        self.__sf_file = sffile
        self.__pinfo_value = pinfo_value
        self.__fout_path = fout_path

    def initialize_data(self):
        self.initialize_refln_data()
        self.initialize_diffrn_refln_data()
        self.initialize_counts()
        self.initialize_columns()

    def initialize_refln_data(self):
        self.__refln_data = self.__sf_block.getObj("refln")
        if self.__refln_data is not None:
            self.__rcell, self.__cell = self.calc_cell_and_recip()

    def initialize_diffrn_refln_data(self):
        self.__diffrn_refln_data = self.__sf_block.getObj("diffrn_refln")

    def initialize_counts(self):
        if self.__refln_data:
            self.__nref = self.__refln_data.getRowCount()
        if self.__diffrn_refln_data:
            self.__dnref = self.__diffrn_refln_data.getRowCount()

    def initialize_columns(self):
        attributes = {
            "index_h": "H",
            "index_k": "K",
            "index_l": "L",
            "F_meas_au": "Fo_au",
            "F_meas_sigma_au": "sFo_au",
            "F_meas_sigma": "sFo",
            "F_squared_sigma": "sF2o",
            "pdbx_I_plus_sigma": "sI_plus",
            "pdbx_I_minus_sigma": "sI_minus",
            "pdbx_F_plus_sigma": "sF_plus",
            "pdbx_F_minus_sigma": "sF_minus",
            "F_meas": "Fo",
            "F_squared_meas": "F2o",
            "pdbx_I_plus": "I_plus",
            "pdbx_I_minus": "I_minus",
            "pdbx_F_plus": "F_plus",
            "pdbx_F_minus": "F_minus",
            "fom": "fom",
            "phase_calc": "phase_c",
            "phase_meas": "phase_o",
        }

        for attr, var in attributes.items():
            if self.__refln_data.hasAttribute(attr):
                setattr(self, var, self.__refln_data.getColumn(self.__refln_data.getIndex(attr)))
                setattr(self, "_CheckSfFile__"+var, self.__refln_data.getColumn(self.__refln_data.getIndex(attr)))

            else:
                setattr(self, "_CheckSfFile__"+var, None)

        diffrn_attributes = {
            "intensity_net": "unmerge_i",
            "intensity_sigma": "unmerge_si",
            "index_h": "dH",
            "index_k": "dK",
            "index_l": "dL"
        }

        for attr, var in diffrn_attributes.items():
            if self.__diffrn_refln_data and self.__diffrn_refln_data.hasAttribute(attr):
                setattr(self, "_CheckSfFile__"+var, self.__diffrn_refln_data.getColumn(self.__diffrn_refln_data.getIndex(attr)))
            else:
                setattr(self, "_CheckSfFile__"+var, None)

        self.initialize_Io()
        self.initialize_sIo()
        self.initialize_status()

    def initialize_Io(self):
        # Check if attribute "intensity_meas" is present
        if self.__refln_data.hasAttribute("intensity_meas"):
            self.__Io = self.__refln_data.getColumn(self.__refln_data.getIndex("intensity_meas"))
        else:
            self.__Io = None

        # If self.__Io is still None, check for attribute "intensity_meas_au"
        if not self.__Io:
            if self.__refln_data.hasAttribute("intensity_meas_au"):
                self.__Io = self.__refln_data.getColumn(self.__refln_data.getIndex("intensity_meas_au"))

            # If attribute "intensity_meas_au" is present and was successfully set to self.__Io, change the token
            if self.__Io:
                self.cif_token_change("intensity_meas_au", "intensity_meas")

        # If self.__Io is still None, check for attribute "intensity"
        if not self.__Io:
            if self.__refln_data.hasAttribute("intensity"):
                self.__Io = self.__refln_data.getColumn(self.__refln_data.getIndex("intensity"))

            # If attribute "intensity" is present and was successfully set to self.__Io, change the token
            if self.__Io:
                self.cif_token_change("intensity", "intensity_meas")

    def initialize_sIo(self):
        # Check if attribute "intensity_sigma" is present
        if self.__refln_data.hasAttribute("intensity_sigma"):
            self.__sIo = self.__refln_data.getColumn(self.__refln_data.getIndex("intensity_sigma"))
        else:
            self.__sIo = None

        # If self.__sIo is still None, check for attribute "intensity_sigma_au"
        if not self.__sIo:
            if self.__refln_data.hasAttribute("intensity_sigma_au"):
                self.__sIo = self.__refln_data.getColumn(self.__refln_data.getIndex("intensity_sigma_au"))

            # If attribute "intensity_sigma_au" is present and was successfully set to self.__sIo, change the token
            if self.__sIo:
                self.cif_token_change("intensity_sigma_au", "intensity_sigma")

        # If self.__sIo is still None, check for attribute "intensity_sigm"
        if not self.__sIo:
            if self.__refln_data.hasAttribute("intensity_sigm"):
                self.__sIo = self.__refln_data.getColumn(self.__refln_data.getIndex("intensity_sigm"))

            # If attribute "intensity_sigm" is present and was successfully set to self.__sIo, change the token
            if self.__sIo:
                self.cif_token_change("intensity_sigm", "intensity_sigma")

        # If self.__sIo is still None, check for attribute "intensity_meas_sigma"
        if not self.__sIo:
            if self.__refln_data.hasAttribute("intensity_meas_sigma"):
                self.__sIo = self.__refln_data.getColumn(self.__refln_data.getIndex("intensity_meas_sigma"))

            # If attribute "intensity_meas_sigma" is present and was successfully set to self.__sIo, change the token
            if self.__sIo:
                self.cif_token_change("intensity_meas_sigma", "intensity_sigma")

        # If self.__sIo is still None, check for attribute "intensity_meas_sigma_au"
        if not self.__sIo:
            if self.__refln_data.hasAttribute("intensity_meas_sigma_au"):
                self.__sIo = self.__refln_data.getColumn(self.__refln_data.getIndex("intensity_meas_sigma_au"))

            # If attribute "intensity_meas_sigma_au" is present and was successfully set to self.__sIo, change the token
            if self.__sIo:
                self.cif_token_change("intensity_meas_sigma_au", "intensity_sigma")

    def initialize_status(self):
        self.__status = self.__refln_data.getColumn(self.__refln_data.getIndex("status"))
        if not self.__status:
            self.__status = self.__refln_data.getColumn(self.__refln_data.getIndex("R_free_flag"))
            if self.__status:
                self.cif_token_change("R_free_flag", "status")

            if not self.__status:
                self.__status = self.__refln_data.getColumn(self.__refln_data.getIndex("statu"))
                if self.__status:
                    self.cif_token_change("statu", "status")

                if not self.__status:
                    self.__status = self.__refln_data.getColumn(self.__refln_data.getIndex("status_au"))
                    if self.__status:
                        self.cif_token_change("status_au", "status")

    def calc_cell_and_recip(self):
        data = self.__sf_block.getObj("cell")
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

            return rcell, cell
        else:
            pinfo("No cell data found in the mmCIF file.")

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
        refln_data = self._sf_block.getObj("refln")
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

            pinfo("Best Resolution: {:.2f} Angstroms".format(best_resolution), self.__pinfo_value)
        else:
            pinfo("No refln data found in the mmCIF file.", self.__pinfo_value)

    def cif_token_change(self, old_token, new_token):
        pinfo(f"Warning! The mmcif token  _refln.{old_token} is wrong!", self.__pinfo_value)
        pinfo(f"It has been corrected as _refln.{new_token}", self.__pinfo_value)

    def check_sf(self, nblock):

        self.__sf_block = self.__sf_file.getBlockByIndex(nblock)
        pinfo(f"Data_block_id={self.__sf_block.getName()}, block_number={nblock+1}\n", self.__pinfo_value)
        self.initialize_data()

        temp_nref, nstart, n1, n2, n4, n5, nfpairF, nfpairI, nf_sFo, nf_sIo, key = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        sum_sigii, ii_sigii, ii_sigii_low, nnii, sum_ii, nnii_low, nfp, nfn, nip, nin, n_obs, n_free = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        max_H, min_H, max_K, min_K, max_L, min_L = -500, 500, -500, 500, -500, 500
        max_F, min_F, max_I, min_I = -500000.0, 500000.0, -5000000.0, 5000000.0
        max_R, min_R, max_F2, min_F2 = -500.0, 900.0, -500000.0, 500000.0
        ii_sigii_max = -90000
        resolution = 0
        i_over_si, sum_i, sum_si, nf_Io, n6, n7, n8 = 0, 0, 0, 0, 0, 0, 0
        f_over_sf, sum_f, sum_sf, nf_Fo = 0, 0, 0, 0
        f2_over_sf2, sum_f2, sum_sf2, nf_F2o = 0, 0, 0, 0

        resol = [100]
        RESOH = 0.1
        RESOL = 200
        
        if not (self.__dH or self.__dK or self.__dL or self.__H or self.__K or self.__L):
            pinfo(f"Error: File has no 'index_h, index_k, index_l' (data block= {nblock + 1}).", self.__pinfo_value)
            return
        
        if not (self.__Fo_au or self.__Fo or self.__Io or self.__F2o or self.__I_plus or self.__I_minus or
                self.__F_plus or self.__F_minus or self.__unmerge_i or self.__unmerge_si):
            pinfo(f"Error: File has no mandatory items 'F/I/F+/F-/I+/I-' (data block= {nblock + 1}). ", self.__pinfo_value)
            return

        if self.__nref < 30 and self.__dnref > 30:
            return  # do not further check the unmerged data!!
        
        if self.__nref < 30:
            pinfo(f"Error: File has too few reflections ({self.__nref}) (data block= {nblock + 1}).", self.__pinfo_value)
            return

        if ((self.__Fo_au and not self.__sFo_au) or (self.__Fo and not self.__sFo) or
            (self.__Io and not self.__sIo) or (self.__F2o and not self.__sF2o) or
            (self.__I_plus and not self.__sI_plus) or (self.__I_minus and not self.__sI_minus) or
            (self.__F_plus and not self.__sF_plus) or (self.__F_minus and not self.__sF_minus) or
            (self.__unmerge_i and not self.__unmerge_si)):

            pinfo(f"Error: Sigma values are missing (data block= {nblock + 1})!", self.__pinfo_value)

        if self.__status is None:
            pinfo(f"Error: File has no free set (data block= {nblock + 1}).", self.__pinfo_value)

        refln_data = self.__sf_block.getObj("refln")
        if refln_data is not None:
            rcell, cell = self.calc_cell_and_recip()

        if (cell[0] > 0.01 and cell[1] > 0.01): key = 1
        
        for i in range(nstart, self.__nref):  # check data items
            #pinfo(f"Checking reflection {i} of {self._nref} (data block= {nblock + 1})")
            ah = int(self.__H[i])
            ak = int(self.__K[i])
            al = int(self.__L[i])

            min_H = min(min_H, ah)
            min_K = min(min_K, ak)
            min_L = min(min_L, al)

            max_H = max(max_H, ah)
            max_K = max(max_K, ak)
            max_L = max(max_L, al)

            if not ((self.__Fo_au and self.__Fo_au[i] != '?') or
                    (self.__Io and self.__Io[i] != '?') or
                    (self.__I_plus and self.__I_plus[i] != '?') or
                    (self.__I_minus and self.__I_minus[i] != '?') or
                    (self.__F_plus and self.__F_plus[i] != '?') or
                    (self.__F_minus and self.__F_minus[i] != '?') or
                    (self.__unmerge_i and self.__unmerge_i[i] != '?') or
                    (self.__F2o and self.__F2o[i] != '?') or
                    (self.__Fo and self.__Fo[i] != '?')):
                continue

            temp_nref += 1
            hkl = f"HKL={ah:4d} {ak:4d} {al:4d}"

            if ((ah == 0 and ak == 0 and al == 0) or
                    (abs(ah) > 800 or abs(ak) > 800 or abs(al) > 800)):
                if n1 == 1:
                    pinfo(f"Error: File has wrong indices ({hkl}).", self.__pinfo_value)
                    n1 += 1

            #--------------------------------------------------------------

            def is_float(value):
                try:
                    float(value)
                    return True
                except ValueError:
                    return False

            if self.__sFo_au and i > 0 and is_float(self.__sFo_au[i - 1]) and is_float(self.__sFo_au[i]):
                if float(self.__sFo_au[i - 1]) == float(self.__sFo_au[i]):
                    nf_sFo += 1
            if self.__sIo and i > 0 and is_float(self.__sIo[i - 1]) and is_float(self.__sIo[i]):
                if float(self.__sIo[i - 1]) == float(self.__sIo[i]):
                    nf_sIo += 1


            # if self.__sFo_au and i > 0 and float(self.__sFo_au[i - 1]) == float(self.__sFo_au[i]):
            #     nf_sFo += 1
            # if self.__sIo and i > 0 and float(self.__sIo[i - 1]) == float(self.__sIo[i]):
            #     nf_sIo += 1

            if self.__F_plus:
                f = float(self.__F_plus[i])
                nfpairF += 1
                if f < 0 and self.__n4 == 1:
                    pinfo(f"Error: File has negative amplitude (F+: {self.__F_plus[i]}) for ({hkl}).", self.__pinfo_value)
                    n4 += 1

            if self.__I_plus:
                nfpairI += 1
                f = float(self.__I_plus[i])

            if key > 0:
                resolution = self.get_resolution(ah, ak, al, self.__rcell)

                if min_R > resolution:
                    min_R = resolution
                    self.__hkl_min = f"{ah: 4d} {ak: 4d} {al: 4d}"

                if max_R < resolution:
                    max_R = resolution
                    self.__hkl_max = f"{ah: 4d} {ak: 4d} {al: 4d}"

                val = 0
                sval = 0
                if self.__Io and self.__sIo and self.__sIo[i] != '?':
                    val = float(self.__Io[i])
                    sval = float(self.__sIo[i])
                elif self.__Fo_au and self.__sFo_au and self.__sFo_au[i] != '?':
                    val = float(self.__Fo_au[i]) * float(self.__Fo_au[i])
                    sval = 2 * float(self.__Fo_au[i]) * float(self.__sFo_au[i])
                elif self.__F2o and self.__sFo and self.__sF2o[i] != '?':
                    val = float(self.__F2o[i])
                    sval = float(self.__sF2o[i])
                elif self.__Fo and self.__sFo and self.__sFo[i] != '?':
                    val = float(self.__Fo[i]) * float(self.__Fo[i])
                    sval = 2 * float(self.__Fo[i]) * float(self.__sFo[i])

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

            if RESOL + 0.01 >= resolution >= RESOH - 0.01:  # for onedep
                if self.__F_plus and not '?' in self.__F_plus[i]:
                    nfp += 1
                if self.__F_minus and not '?' in self.__F_minus[i]:
                    nfn += 1
                if self.__I_plus and not '?' in self.__I_plus[i]:
                    nip += 1
                if self.__I_minus and not '?' in self.__I_minus[i]:
                    nin += 1

                if ((self.__Fo and not '?' in self.__Fo[i]) or
                        (self.__Fo_au and not '?' in self.__Fo_au[i]) or
                        (self.__Io and not '?' in self.__Io[i]) or
                        (self.__F2o and not '?' in self.__F2o[i]) or
                        ((self.__F_plus and not '?' in self.__F_plus[i]) or
                        (self.__F_minus and not '?' in self.__F_minus[i])) or
                        ((self.__I_plus and not '?' in self.__I_plus[i]) or
                        (self.__I_minus and not '?' in self.__I_minus[i]))):
                    if self.__status and 'o' in self.__status[i]:
                        n_obs += 1
                    elif self.__status and 'f' in self.__status[i]:
                        n_free += 1

            if self.__Fo_au:
                f = float(self.__Fo_au[i])
                if f < 0 and self.__n5 == 0:
                    self.__n5 += 1
                    pinfo(f"Error: File has negative amplitude (Fo: {self.__Fo_au[i]}) for ({hkl}).", self.__pinfo_value)

                if f < min_F: min_F = f
                if f > max_F: max_F = f

                if self.__sFo_au:
                    sigf = float(self.__sFo_au[i])
                    if sigf > 0 and self.__sFo_au[i] != '?':
                        f_over_sf += f / sigf
                        sum_f += f
                        sum_sf += sigf
                        nf_Fo += 1
                    


            if self.__F2o:
                f = float(self.__F2o[i])
                if f < min_F2: min_F2 = f
                if f > max_F2: max_F2 = f

                if self.__sF2o:
                    sigf = float(self.__sF2o[i])
                    if sigf > 0 and self.__sF2o[i] != '?':
                        f2_over_sf2 += f / sigf
                        sum_f2 += f
                        sum_sf2 += sigf
                        nf_F2o += 1

            if self.__Io:
                f = float(self.__Io[i])
                if f < min_I: min_I = f
                if f > max_I: max_I = f

                if self.__sIo:
                    sigf = float(self.__sIo[i])
                    if sigf > 0 and self.__sIo[i] != '?':
                        i_over_si += f / sigf
                        sum_i += f
                        sum_si += sigf
                        nf_Io += 1

            if self.__fom and abs(float(self.__fom[i])) > 1.01:
                if n6 == 0:
                    n6 += 1
                    pinfo(f"Warning: File has wrong values of FOM ({self.__fom[i]}) for ({hkl}).", self.__pinfo_value)

            if self.__phase_c and abs(float(self.__phase_c[i])) > 361.0:
                if n7 == 0:
                    n7 += 1
                    pinfo(f"Warning: File has wrong values of phase ({self.__phase_c[i]}) for ({hkl}).", self.__pinfo_value)

            if self.__phase_o and abs(float(self.__phase_o[i])) > 361.0:
                if n8 == 0:
                    n8 += 1
                    pinfo(f"Warning: File has wrong values of phase ({self.__phase_o[i]}) for ({hkl}).", self.__pinfo_value)


        if n1 > 0:
            pinfo(f"Error: File has ({n1}) reflections with wrong indices.", self.__pinfo_value)

        if n2 > 0:
            pinfo(f"Warning: File has ({n2}) reflections with negative SIGMA, (Corrected: given status '<').", self.__pinfo_value)

        if n4 > 0:
            pinfo(f"Error: File has ({n4}) reflections with negative amplitude (F+).", self.__pinfo_value)

        if n5 > 0:
            pinfo(f"Error: File has ({n5}) reflections with negative amplitude (Fo).", self.__pinfo_value)

        if temp_nref > 10 and ((nf_sFo > 0 and temp_nref - nf_sFo < 3) or (nf_sIo > 0 and temp_nref - nf_sIo < 3)):
            pinfo(f"Warning! File has Sigma_Fo all the same!", self.__pinfo_value)

        # Following are the messages related to total number of reflections
        pinfo(f"Total number of observed reflections = {(n_obs + n_free)}", self.__pinfo_value)
        pinfo(f"Total number of observed reflections (status='o') = {n_obs}", self.__pinfo_value)
        pinfo(f"Total number of observed reflections (status='f') = {n_free}", self.__pinfo_value)
        if n_obs > 0:
            rfree_p = 100 * float(n_free) / float(n_obs)
            pinfo(f"Percentage for free set = {rfree_p:.2f}", self.__pinfo_value)

        if nfpairF > 10:
            pinfo(f"Total number of Friedel pairs (F+/F-) = {nfpairF}", self.__pinfo_value)
            pinfo(f"Total number of observed F+ = {nfp}", self.__pinfo_value)
            pinfo(f"Total number of observed F- = {nfn}", self.__pinfo_value)
            pinfo(f"Sum of observed F+ and F-  = {(nfn + nfp)}", self.__pinfo_value)
        
        if nfpairI > 10:
            pinfo(f"Total number of Friedel pairs (I+/I-) = {nfpairI}", self.__pinfo_value)
            pinfo(f"Total number of observed I+ = {nip}", self.__pinfo_value)
            pinfo(f"Total number of observed I- = {nin}", self.__pinfo_value)
            pinfo(f"Sum of observed I+ and I-  = {(nin + nip)}", self.__pinfo_value)

        if key > 0 and self.__cell[0] > 0.001:
            pinfo(f"Cell = {self.__cell[0]:.2f} {self.__cell[1]:.2f} {self.__cell[2]:.2f} {self.__cell[3]:.2f} {self.__cell[4]:.2f} {self.__cell[5]:.2f}", self.__pinfo_value)
            pinfo(f"Lowest resolution= {max_R:.2f} ; corresponding HKL={self.__hkl_max}", self.__pinfo_value)
            pinfo(f"Highest resolution={min_R:.2f} ; corresponding HKL={self.__hkl_min}", self.__pinfo_value)
            if RESOH > 0.11 and abs(RESOH - min_R) > 0.4 and nblock == 0:
                pinfo(f"Warning: large difference between reported ({RESOH:.2f}) and calculated({min_R:.2f}) resolution.", self.__pinfo_value)
            resol[0] = min_R
        
        pinfo(f"Max indices (Hmax={max_H:4d}  Kmax={max_K:4d}  Lmax={max_L:4d})", self.__pinfo_value)
        pinfo(f"Min indices (Hmin={min_H:4d}  Kmin={min_K:4d}  Lmin={min_L:4d})", self.__pinfo_value)

        if self.__Fo_au:
            pinfo(f"maximum value of amplitude= {max_F:.2f}", self.__pinfo_value)
            pinfo(f"minimum value of amplitude= {min_F:.2f}", self.__pinfo_value)
            pinfo(f"<F/sigmaF> = {f_over_sf / nf_Fo:.2f};  <F>/<sigmaF> = {sum_f / sum_sf:.2f}", self.__pinfo_value)
            if sum_f / sum_sf > 140 or sum_f / sum_sf < 4:
                pinfo(f"Warning: Value of (Fo_avg/sigFo_avg = {sum_f / sum_sf:.2f}) is out of range (check Fo or SigFo in SF file).", self.__pinfo_value)

        if self.__F2o:
            pinfo(f"maximum value of F square= {max_F2:.2f}", self.__pinfo_value)
            pinfo(f"minimum value of F square= {min_F2:.2f}", self.__pinfo_value)
            pinfo(f"<F2/sigmaF2> = {f2_over_sf2 / nf_F2o:.2f};  <F2>/<sigmaF2> = {sum_f2 / sum_sf2:.2f}", self.__pinfo_value)

        if self.__Io:
            pinfo(f"maximum value of intensity= {max_I:.2f}", self.__pinfo_value)
            pinfo(f"minimum value of intensity= {min_I:.2f}", self.__pinfo_value)
            pinfo(f"<I/sigmaI> = {i_over_si / nf_Io:.2f};  <I>/<sigmaI> = {sum_i / sum_si:.2f}", self.__pinfo_value)
            if sum_i / sum_si > 80 or sum_i / sum_si < 2:
                pinfo(f"Warning: Value of (I_avg/sigI_avg = {sum_i / sum_si:.2f}) is out of range (check Io or SigIo in SF file). ", self.__pinfo_value)

            if nf_Fo :
                if f_over_sf / nf_Fo > 0 and (f_over_sf / nf_Fo > 2.5 * i_over_si / nf_Io or f_over_sf / nf_Fo < 1.0 * i_over_si / nf_Io):
                    pinfo(f"Warning: too much difference Fo/sigFo = {f_over_sf / nf_Fo:.2f};  Io/sigIo = {i_over_si / nf_Io:.2f}", self.__pinfo_value)

        if nnii > 10:
            pinfo(f"Using all data:  <I/sigI>={ii_sigii / nnii:.2f}", self.__pinfo_value)
            pinfo(f"Using all data:  <I>/<sigI>={sum_ii / sum_sigii:.2f}", self.__pinfo_value)
            pinfo(f"Using all data:  Rsig(<sigI>/<I>)={sum_sigii / sum_ii:.3f}", self.__pinfo_value)
            pinfo(f"The maximum value of <I/sigI>_max={ii_sigii_max:.2f}", self.__pinfo_value)

        if nnii_low > 10:
            pinfo(f"Use data with resolution >7.0 Angstrom: <I/sigI>_low={ii_sigii_low / nnii_low:.2f}", self.__pinfo_value)

        pinfo(f"\n", self.__pinfo_value)

        return

    def float_or_zero(self, value):
        try:
            float(value)
            return float(value)
        except ValueError:
            return 0

    def other_to_f(self, i):
        sp1 = 0
        sp2 = 0
        I = 0
        Is = 0

        F = 0
        Fs = 0.01

        if self.__Io:  # Io
            if self.__Io[i] != '?':
                I = float(self.__Io[i])

                if I > 0 and self.__sIo:
                    F = math.sqrt(I)
                    Fs = float(self.__sIo[i]) / (2.0 * F)

        elif self.__sI_plus and self.__sI_minus:  # I_plus
            sp1 = -1 if self.__sI_plus[i] == '?' else float(self.__sI_plus[i])
            sp2 = -1 if self.__sI_minus[i] == '?' else float(self.__sI_minus[i])

            I = 0
            Is = 0

            if sp1 < 0 and sp2 < 0:
                pass
            elif sp1 > 0 and sp2 < 0:
                I = float(self.__I_plus[i])
                Is = float(self.__sI_plus[i])
            elif sp1 < 0 and sp2 > 0:
                I = float(self.__I_minus[i])
                Is = float(self.__sI_minus[i])
            elif sp1 > 0 and sp2 > 0:
                I = (float(self.__I_plus[i]) + float(self.__I_minus[i])) / 2.0
                Is = (float(self.__sI_plus[i]) + float(self.__sI_minus[i])) / 2.0

            if I > 0:
                F = math.sqrt(I)
                Fs = Is / (2.0 * F)

        elif self.__F_plus and self.__F_minus:  # F_plus
            if self.__F_plus[i] == '?' and self.__F_minus[i] == '?':
                F = 0
                Fs = 0
            elif self.__F_plus[i] != '?' and self.__F_minus[i] == '?':
                F = float(self.__F_plus[i])
                if self.__sF_plus:
                    Fs = float(self.__sF_plus[i])
            elif self.__F_plus[i] == '?' and self.__F_minus[i] != '?':
                F = float(self.__F_minus[i])
                if self.__sF_minus:
                    Fs = float(self.__sF_minus[i])
            elif self.__F_plus[i] != '?' and self.__F_minus[i] != '?':
                F = (float(self.__F_plus[i]) + float(self.__F_minus[i])) / 2.0
                if self.__sF_plus and self.__sF_minus:
                    Fs = (float(self.__sF_plus[i]) + float(self.__sF_minus[i])) / 2.0

        return F, Fs

    def i_to_f(self, i, I, sI, sf_default):
        f = 0.0
        sf = 0.0

        if float(I) > 0:
            f = math.sqrt(float(I))
            if sI and float(sI[i]) > 0:
                sf = float(sI[i]) / (2.0 * f)
            else:
                sf = sf_default

        fp = "{:.2f}".format(f)
        sigfp = "{:.2f}".format(sf)

        return fp, sigfp

    def write_sf_4_validation(self, nblock=0):
    
        file_name = 'sf_4_validate.cif'
        file_path = os.path.join(self.__fout_path, file_name)


        self.__sf_block = self.__sf_file.getBlockByIndex(nblock)
        self.initialize_data()

        myDataList = []
        curContainer = DataContainer("cif2cif")

        nf, i, ah, ak, al = 0, 0, 0, 0, 0
        F, Fs, sig = 0.0, 0.0, 0.01
        resol, i_sigi, af, afs = 0.0, 0.0, 0.0, 0.0
        fout = None
        # Need to ask Ezra about this
        RESCUT, SIGCUT = 0.0, 0.0
        n = self.__nref

        rcell, CELL = self.calc_cell_and_recip()

        if(CELL[0] > 2 and CELL[4] > 2):
            data = self.__sf_block.getObj("symmetry")
            SYMM = data.getValue("space_group_name_H-M")
            aCat = DataCategory("symmetry")

            if(nblock > 0):
                aCat.appendAttribute("Int_Tables_number")
                aCat.append((nblock,))

            if(len(SYMM)>1):
                aCat.appendAttribute("space_group_name_H-M")
                aCat.append((SYMM,))

            curContainer.append(aCat)
            
            if(CELL[0] > 0.5 and CELL[2] > 0.5):
                bCat = DataCategory("cell")
                bCat.appendAttribute("length_a")
                bCat.appendAttribute("length_b")
                bCat.appendAttribute("length_c")
                bCat.appendAttribute("angle_alpha")
                bCat.appendAttribute("angle_beta")
                bCat.appendAttribute("angle_gamma")
                bCat.append((CELL[0], CELL[1], CELL[2], CELL[3], CELL[4], CELL[5]))
                curContainer.append(bCat)


        cCat = DataCategory("refln")
        cCat.appendAttribute("index_h")
        cCat.appendAttribute("index_k")
        cCat.appendAttribute("index_l")
        cCat.appendAttribute("status")
        cCat.appendAttribute("F_meas_au")
        cCat.appendAttribute("F_meas_sigma_au")
        cCat.appendAttribute("d_spacing")
        cCat.appendAttribute("I_over_sigI")

        if(self.__Io and self.__sIo):
            cCat.appendAttribute("intensity_meas")
            cCat.appendAttribute("intensity_sigma")

        if(self.__F_plus and self.__sF_plus and self.__F_minus and self.__sF_minus):
            cCat.appendAttribute("pdbx_F_plus")
            cCat.appendAttribute("pdbx_F_plus_sigma")
            cCat.appendAttribute("pdbx_F_minus")
            cCat.appendAttribute("pdbx_F_minus_sigma")

        if(self.__I_plus and self.__sI_plus and self.__I_minus and self.__sI_minus):
            cCat.appendAttribute("pdbx_I_plus")
            cCat.appendAttribute("pdbx_I_plus_sigma")
            cCat.appendAttribute("pdbx_I_minus")
            cCat.appendAttribute("pdbx_I_minus_sigma")

        fp = "?"
        sigfp = "?"

        for i in range(n):

            if(self.__status):
                if(self.__status[i] != "o" and self.__status[i] != "f"):
                    continue
                flag = self.__status[i]
            else:
                flag = "o"

            if(self.__Fo_au):
                fp = self.__Fo_au[i]
                if(self.__sFo_au):
                    if(self.__sFo_au[i] != "?"):
                        sigfp = self.__sFo_au[i]
                    else:
                        sigfp = f"{sig:.4f}"
                else:
                    sigfp = f"{sig:.4f}"

            elif(self.__Io):
                fp, sigfp = self.i_to_f(i, self.__Io[i], self.__sIo, sig)

            elif(self.__I_plus or self.__F_plus):
                F, Fs = self.other_to_f(i)
                fp = f"{F:.4f}"
                sigfp = f"{Fs:.4f}"

            elif(self.__Fo):
                fp = self.__Fo[i]
                if(self.__sFo):
                    if(float(self.__sFo[i]) > sig):
                        sigfp = self.__sFo[i]
                    else:
                        sigfp = f"{sig:.4f}"
                else:
                    sigfp = f"{sig:.4f}"

            elif(self.__F2o):
                fp, sigfp = self.i_to_f(i, self.__F2o[i], self.__sF2o, sig)

            ah = int(self.__H[i])
            ak = int(self.__K[i])
            al = int(self.__L[i])
            resol = self.get_resolution(ah, ak, al, rcell)

            i_sigi = 0.0
            if (self.__Io and self.__sIo and float(self.__sIo[i])>0):
                i_sigi = float(self.__Io[i])/float(self.__sIo[i])
            else:
                af = self.float_or_zero(fp)
                afs = self.float_or_zero(sigfp)
                if (afs>0): 
                    i_sigi = af/(2*afs)

            if(RESCUT > 0.0001 and resol < RESCUT and resol > 0.0001): continue
            if(abs(SIGCUT) > 0.0001 and i_sigi < SIGCUT): continue

            values_to_append = (self.__H[i], self.__K[i], self.__L[i], flag, fp, sigfp, resol, i_sigi)

            if self.__Io and self.__sIo:
                values_to_append += (self.__Io[i], self.__sIo[i])

            if self.__F_plus and self.__sF_plus and self.__F_minus and self.__sF_minus:
                values_to_append += (self.__F_plus[i], self.__sF_plus[i], self.__F_minus[i], self.__sF_minus[i])

            if self.__I_plus and self.__sI_plus and self.__I_minus and self.__sI_minus:
                values_to_append += (self.__I_plus[i], self.__sI_plus[i], self.__I_minus[i], self.__sI_minus[i])

            cCat.append(values_to_append)

            nf += 1

        curContainer.append(cCat)
        myDataList.append(curContainer)

        with open(file_path, "w") as ofh:
                pdbxW = PdbxWriter(ofh)
                pdbxW.setAlignmentFlag(flag=True)
                pdbxW.write(myDataList)

        #print("\nNumber of reflections for validation set = %d" % nf)
    
    def check_sf_all_blocks(self, n):
        for i in range(n):
            self.check_sf(i)   
# -------------------------------------------------- MAIN FUNCTION ----------------------------------------------------------- #



# def main():
#     parser = argparse.ArgumentParser(description='Process some integers.')
#     parser.add_argument('--sffile', type=str, required=True, help='Path to the SF file')
#     parser.add_argument('--pinfo_value', type=int, default=0, help='Value for pinfo')
#     parser.add_argument('--fout_path', type=str, default=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))), 'output'), help='Optional path to the output file for write_sf_4_validation')
#     parser.add_argument('--nblock', type=int, default=0, help='Optional nblock value for write_sf_4_validation')
#     parser.add_argument('--check_all', action='store_true', help='Check all SF blocks if this flag is set')
#     parser.add_argument('--write_validation', action='store_true', help='Write SF for validation if this flag is set')

#     args = parser.parse_args()

#     sffile = SFFile()
#     sffile.readFile(args.sffile)
#     n = sffile.getBlocksCount()


#     pinfo("", 2)
#     pinfo(f"Total number of data blocks = {n} \n\n", args.pinfo_value)

#     calculator = CheckSfFile(sffile, args.fout_path, args.pinfo_value)

#     if args.write_validation:
#         calculator.write_sf_4_validation(args.nblock)

#     if args.check_all:
#         check_sf_all_blocks(calculator, n)

# if __name__ == "__main__":
#     main()

# -------------------------------------------------- MAIN FUNCTION ----------------------------------------------------------- #

def main():
    # Define the input and output formats
    input_formats = ['MTZ', 'mmCIF', 'CIF', 'CNS', 'Xplor', 'SHELX', 'HKL2000', 
                     'Scalepack', 'Dtrek', 'TNT', 'SAINT', 'EPMR', 'XSCALE', 
                     'XPREP', 'XTALVIEW', 'X-GEN', 'XENGEN', 'MULTAN', 'MAIN', 'OTHER']
    output_formats = ['mmCIF', 'MTZ', 'CNS', 'TNT', 'SHELX', 'EPMR', 'XTALVIEW', 
                      'HKL2000', 'Dtrek', 'XSCALE', 'MULTAN', 'MAIN', 'OTHER']

    parser = argparse.ArgumentParser(description='Structure factor conversion')
    parser.add_argument('-i', type=str, choices=input_formats, help='Input format')
    parser.add_argument('-o', type=str, choices=output_formats, required=True, help='Output format')
    parser.add_argument('-sf', type=str, required=True, help='Data file')
    parser.add_argument('-out', type=str, help='Output file')
    parser.add_argument('-label', type=str, help='Label name for CNS & MTZ')
    parser.add_argument('-freer', type=int, help='A free test number in the reflection (SF) file')
    parser.add_argument('-pdb', type=str, help='A PDB file (add items to the converted SF file if missing)')
    parser.add_argument('-sf_type', type=str, choices=['I', 'F'], help='I (intensity) or F (amplitude). Only for shelx or TNT')
    parser.add_argument('-detail', type=str, help='A note to the data set')
    parser.add_argument('-wave', type=float, help='Wavelength. It overwrites the existing one')
    parser.add_argument('-diags', type=str, help='Log file containing warning/error message')
    parser.add_argument('-man', type=str, help='Cells & symmetry (a,b,c,alpha,beta,gamma,p21)')
    parser.add_argument('-flag', type=int, help='A number for re-setting the Rfree random test set')
    parser.add_argument('-format', action='store_true', help='Guess the format of the SF file')
    parser.add_argument('-audit', type=str, help='Update the audit record')
    parser.add_argument('-valid', type=str, help='Check various SF errors, and correct')
    parser.add_argument('-rescut', type=float, help='High resolution cutoff for SF_4_validate.cif')
    parser.add_argument('-sigcut', type=float, help='I/SigI cutoff for SF_4_validate.cif')
    parser.add_argument('-cif_check', action='store_true', help='Check pdbx dictionary. (local use only)')
    parser.add_argument('-ext_data', type=str, help='Extract data from SF file')

    args = parser.parse_args()

#     # Process the arguments and call the corresponding functions
#     # e.g. 
#     if args.i:
#         fun1(args.i)
#     if args.o:
#         fun2(args.o)
#     # etc...

# def fun1(input):
#     print("Processing input", input)

# def fun2(output):
#     print("Processing output", output)

# ... Add more functions to handle other parameters

if __name__ == "__main__":
    main()


# -------------------------------------------------- END OF MAIN FUNCTION ----------------------------------------------------------- #

#python -m src.sf_convert.utils.checksffile --sffile src/sf_convert/cif_files/5pny-sf.cif --write_validation --pinfo_value 1 --check_all
#python your_script.py --sffile path/to/your/file --pinfo_value 1 --check_all --write_validation --fout_path path/to/your/output/file --nblock 5