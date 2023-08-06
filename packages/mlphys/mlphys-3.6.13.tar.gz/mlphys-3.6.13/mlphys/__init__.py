"""
Please keep these lines. Thank you!
"""
__author__ = 'Sanjaya Lohani'
__email__ = 'slohani@mlphys.com'
__licence__ = 'Apache 2.0'
__website__ = "sanjayalohani.com"



print("""
                *-* Machine Learning for Physical Sciences *-*
**********************************************************************************
                    #    # #      #####  #    # #   #  ####  
                    ##  ## #      #    # #    #  # #  #      
                    # ## # #      #    # ######   #    ####  
                    #    # #      #####  #    #   #        # 
                    #    # #      #      #    #   #   #    # 
                    #    # ###### #      #    #   #    ####  
**********************************************************************************
                                                            slohani@mlphys.com
""")
from mlphys.deepqis.simulator import measurements, distributions
from mlphys.deepqis.utils import Fidelity_Measure, Purity_Measure, Positive_Partial_Trace, Alpha_Measure, \
    Concurrence_Measure, gen_basis_array, gen_basis_order, Max_Eigen_Measure, Rank_Measure, Extract_Net
from mlphys.deepqis.network import inference
from mlphys.deepqis.optimization import bme, linear_inversion, mle
from mlphys.fso.lgoam.source import OAM_Intensity_Phase
from mlphys.fso.turbulence import gdo_corrected_phase_mask, phase_mask, propagate
from mlphys import version

