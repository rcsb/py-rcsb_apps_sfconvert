from sf_file import SFFile

filename = "1o08-sf.cif"

sf_file = SFFile()
sf_file.readFile(filename)


refln_data = sf_file.getObj("refln")

fom = refln_data.getColumn(refln_data.getIndex("fom"))

n = refln_data.getAttributeList()
print(n)
# for i in range(len(n)):
#     print(refln_data.getIndex(n[i]))

print("------------------")

print(refln_data.getIndex("fom"))
print(refln_data.hasAttribute("fom"))