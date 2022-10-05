import LeptonInjector as LI
from math import pi
import os 

xs_folder = os.path.join( os.path.dirname(__file__), '..' )

n_events    = 1000
diff_xs     = xs_folder + "/test_xs.fits"
total_xs    = xs_folder + "/test_xs_total.fits"
# Ranged Mode, described in  Section II.A
is_ranged   = True 
# Particles chosen for NuMu-CC using Table II.1
final_1     = LI.Particle.MuMinus
final_2     = LI.Particle.Hadrons
# Build the Injector object described in Section 2
the_injector = LI.injector( n_events , final_1, final_2, diff_xs, total_xs, is_ranged)

deg = pi/180.
minE        = 1000.     # [GeV]
maxE        = 100000.   # [GeV]
gamma       = 2. 
minZenith   = 80.*deg
maxZenith   = 180.*deg
minAzimuth  = 0.*deg
maxAzimuth  = 180.*deg

# constructing the Controller object described in Section II
controller  = LI.Controller( the_injector, minE, maxE, gamma, minAzimuth, maxAzimuth, minZenith, maxZenith)  

# specify the output
controller.Output("./data_output.h5")
controller.LICFile("./config.lic")

# Starts the Process, as illustrated in Figure II.1
controller.Execute()
