
#
# script to make the calculations (created by XOPPY:crystal)
#

import numpy
from xoppylib.crystals.tools import bragg_calc2, run_diff_pat
import xraylib
from dabax.dabax_xraylib import DabaxXraylib

#
# run bragg_calc (preprocessor) and create file xcrystal.bra
#
bragg_dictionary = bragg_calc2(
    descriptor = "Si",
    hh         = 1,
    kk         = 1,
    ll         = 1,
    temper     = 1.0,
    emin       = 7900.0,
    emax       = 8100.0,
    estep      = 1.0,
    ANISO_SEL=0,
    fileout="xcrystal.bra",
    do_not_prototype=0,  # 0=use site groups (recommended), 1=use all individual sites
    verbose=False,
    material_constants_library=xraylib,)

#
# run external (fortran) diff_pat (note that some parameters may not be used)
#
bragg_dict = run_diff_pat(
    bragg_dictionary,
    preprocessor_file="xcrystal.bra",
    MOSAIC             = 0,
    GEOMETRY           = 0,
    SCAN               = 2,
    UNIT               = 1,
    SCANFROM           = -100.0,
    SCANTO             = 100.0,
    SCANPOINTS         = 200,
    ENERGY             = 8000.0,
    ASYMMETRY_ANGLE    = 0.0,
    THICKNESS          = 0.7,
    MOSAIC_FWHM        = 0.1,
    RSAG               = 125.0,
    RMER               = 1290.0,
    ANISOTROPY         = 0,
    POISSON            = 0.22,
    CUT                = "2 -1 -1 ; 1 1 1 ; 0 0 0",
    FILECOMPLIANCE     = "mycompliance.dat",
    )

for key in bragg_dictionary:
    print(">>>>>>>", key)
#
# example plot
#
from srxraylib.plot.gol import plot
data = numpy.loadtxt("diff_pat.dat", skiprows=5)
plot(data[:,0], data[:,-1])

#
# end script
#





#
# #
# # script to make the calculations (created by XOPPY:crystal)
# #
#
# from xoppylib.crystals.tools import bragg_calc2
# import os
#
# import numpy
# from xoppylib.crystals.tools import run_diff_pat
# import xraylib
# from dabax.dabax_xraylib import DabaxXraylib
#
# dx = DabaxXraylib()
#
# #
# # compute bragg_calc (preprocessor)
# #
#
#
# for file in ["xcrystal.bra"]:
#     try:
#         os.remove(os.path.join(locations.home_bin_run(), file))
#     except:
#         pass
#
# CRYSTAL_DESCRIPTOR = "YB66"
# MILLER_INDEX_H     = 0
# MILLER_INDEX_K     = 0
# MILLER_INDEX_L     = 4
# TEMPER             = 1.0
# SCAN               = 2
# SCANFROM           = 0.0
# SCANTO             = 100.0
# SCANPOINTS         = 200
# ENERGY = 8000.0
# material_constants_library = DabaxXraylib()
#
# if SCAN == 3:  # energy scan
#     emin = SCANFROM - 1
#     emax = SCANTO + 1
# else:
#     emin = ENERGY - 100.0
#     emax = ENERGY + 100.0
#
# print("Using crystal descriptor: ", CRYSTAL_DESCRIPTOR)
#
# bragg_dictionary = bragg_calc2(
#                                descriptor=CRYSTAL_DESCRIPTOR,
#                                hh=MILLER_INDEX_H, kk=MILLER_INDEX_K, ll=MILLER_INDEX_L,
#                                temper=float(TEMPER),
#                                emin=emin, emax=emax,
#                                estep=(SCANTO - SCANFROM) / SCANPOINTS, fileout="xcrystal.bra",
#                                material_constants_library=material_constants_library,
#                                )
#
# #
# #
# #
# bragg_dict = run_diff_pat(
#     bragg_dictionary,
#     # CRYSTAL_DESCRIPTOR = "YB66",
#     # MILLER_INDEX_H     = 0,
#     # MILLER_INDEX_K     = 0,
#     # MILLER_INDEX_L     = 4,
#     # TEMPER             = 1.0,
#     MOSAIC             = 0,
#     GEOMETRY           = 0,
#     SCAN               = 2,
#     UNIT               = 1,
#     SCANFROM           = 0.0,
#     SCANTO             = 100.0,
#     SCANPOINTS         = 200,
#     ENERGY             = 8000.0,
#     ASYMMETRY_ANGLE    = 0.0,
#     THICKNESS          = 0.7,
#     MOSAIC_FWHM        = 0.1,
#     RSAG               = 125.0,
#     RMER               = 1290.0,
#     ANISOTROPY         = 0,
#     POISSON            = 0.22,
#     CUT                = "2 -1 -1 ; 1 1 1 ; 0 0 0",
#     FILECOMPLIANCE     = "mycompliance.dat",
#     # material_constants_library=dx,
#     )
#
# #
# # example plot
# #
# from srxraylib.plot.gol import plot
# data = numpy.loadtxt("diff_pat.dat", skiprows=5)
# plot(data[:,0], data[:,-1])
#
# #
# # end script
# #
