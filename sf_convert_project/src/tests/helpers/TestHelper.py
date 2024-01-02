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
        assert bcur.getName() == bref.getName(), "%s != %s" % (bcur.getName(), bref.getName())
    pass
