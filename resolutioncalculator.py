import math
from sf_file import SFFile

class ResolutionCalculator:
    def __init__(self, filename):
        self.sf_file = SFFile()
        self.sf_file.readFile(filename)

    def calc_recip_cell(self, cell):
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

        return rcell

    def convert_reflections(self, reflection_data):
        h_list = []
        k_list = []
        l_list = []

        for reflection in reflection_data:
            h = int(reflection[3])
            k = int(reflection[4])
            l = int(reflection[5])

            h_list.append(h)
            k_list.append(k)
            l_list.append(l)

        return h_list, k_list, l_list

    def calc_cell(self):
        data = self.sf_file.getObj("cell")
        if data is not None:
            a = float(data.getValue("length_a"))
            b = float(data.getValue("length_b"))
            c = float(data.getValue("length_c"))
            alpha = float(data.getValue("angle_alpha"))
            beta = float(data.getValue("angle_beta"))
            gamma = float(data.getValue("angle_gamma"))

            cell = [a, b, c, alpha, beta, gamma]
            rcell = self.calc_recip_cell(cell)

            # Print the reciprocal cell
            return rcell
        else:
            print("No cell data found in the mmCIF file.")

    def calc_hkl(self):
        refln_data = self.sf_file.getObj("refln")
        if refln_data is not None:
            h_list, k_list, l_list = self.convert_reflections(refln_data)

            # Print the converted lists
            print("h values:", h_list)
            print("k values:", k_list)
            print("l values:", l_list)
        else:
            print("No refln data found in the mmCIF file.")

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
        refln_data = self.sf_file.getObj("refln")
        if refln_data is not None:
            h_list, k_list, l_list = self.convert_reflections(refln_data)
            rcell = self.calc_cell()

            best_resolution = 0.0
            for h, k, l in zip(h_list, k_list, l_list):
                resolution = self.get_resolution(h, k, l, rcell)

                if resolution > best_resolution:
                    best_resolution = resolution

            # Print the best resolution
            print("Best Resolution:", best_resolution)
        else:
            print("No refln data found in the mmCIF file.")






filename = "1o08-sf.cif"  # Specify the mmCIF file you want to read
calculator = ResolutionCalculator(filename)
calculator.calc_resolution()
