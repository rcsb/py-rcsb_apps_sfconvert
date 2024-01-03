# Some helper functions for comparing
from mmcif.io.IoAdapterCore import IoAdapterCore
import os


def comp_sfcif(ref, cur):
    """Compares SF ref and cur by performing tests"""
    io = IoAdapterCore()

    assert os.path.exists(ref), "%s does not exist" % ref
    assert os.path.exists(cur), "%s does not exist" % cur

    coref = io.readFile(ref)
    cocur = io.readFile(cur)
    assert coref
    assert cocur

    assert len(coref) == len(cocur)

    for block in range(len(coref)):
        bcur = cocur[block]
        bref = coref[block]

        # Check block names
        assert bcur.getName() == bref.getName(), "block name mismatch %s != %s" % (bcur.getName(), bref.getName())

        # Check list of categories - sort needed?
        clist = bcur.getObjNameList()
        rlist = bref.getObjNameList()

        assert rlist == clist, "categories mismatch %s vs %s" % (clist, rlist)

        # Compare data....
        exclusions = {"refln": ["crystal_id", "wavelength_id", "scale_group_code"]}
        for cat in clist:
            cobj = bcur.getObj(cat)
            robj = bref.getObj(cat)

            # Check number of rows

            assert cobj.getRowCount() == robj.getRowCount(), "Number of rows in %s mismatch" % cat

            calist = cobj.getAttributeList()
            ralist = robj.getAttributeList()

            afilter = exclusions.get(cat, [])

            cset = create_set(calist, afilter)
            rset = create_set(ralist, afilter)

            assert cset == rset, "Attribute mismatch cat %s: %s vs %s" % (cat, rset, cset)

            # Compare data items
            for row in range(cobj.getRowCount()):
                for attr in cset:
                    rval = robj.getValue(attr, row)
                    cval = cobj.getValue(attr, row)
                    if is_float(rval) or is_float(cval):
                        assert abs(float(rval) - float(cval)) < 0.5, "cat %s row %s mismatch %s %s" % (cat, row, rval, cval)
                    elif is_int(rval) or is_int(cval):
                        assert int(rval) == int(cval), "cat %s row %s mismatch %s %s" % (cat, row, rval, cval)
                    else:
                        assert rval == cval, "cat %s row %s mismatch %s %s" % (cat, row, rval, cval)


def create_set(list_in, afilter):
    rset = set()
    for e in list_in:
        if e not in afilter:
            rset.add(e)

    return rset


def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


def is_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False
