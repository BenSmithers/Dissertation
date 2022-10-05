import LeptonWeighter as LW
import h5py as h5
import numpy as np

"""
This calculates the weight of each event in the LeptonInjector example script. 
"""

# These objects are all defined in Section III.A

# Create generator
#    if there were multiple LIC files, you would instead make a list of Generators
net_generation = [LW.MakeGeneratorsFromLICFile("config.lic")]

# This cross section object takes four differential cross sections (dS/dEdxdy) 
#            Neutrino CC-DIS xs
#       Anti-Neutrino CC-DIS xs
#            Neutrino NC-DIS xs
#       Anti-Neutrino NC-DIS xs
cross_section_location = "/path/to/cross_sections/"
xs = LW.CrossSectionFromSpline(
                    cross_section_location+"/dsdxdy_nu_CC_iso.fits",
                    cross_section_location+"/dsdxdy_nubar_CC_iso.fits",
                    cross_section_location+"/dsdxdy_nu_NC_iso.fits",
                    cross_section_location+"/dsdxdy_nubar_NC_iso.fits")

#                         GeV      unitless        GeV
flux_params={ 'constant': 10**-18, 'index':-2, 'scale':10**5 }
liveTime   = 3.1536e7 # [s]


flux = LW.PowerLawFlux( flux_params['constant'] , flux_params['index'] , flux_params['scale'] )

# build weighter
weight_event = LW.Weighter( flux, xs, net_generation )

def get_weight( props ):
    """
    This function takes the "properties" object from a LI-Event. It then calculates and returns the weight
    """
    LWevent = LW.Event()
    LWevent.energy = props[0]
    LWevent.zenith = props[1]
    LWevent.azimuth = props[2]
    
    LWevent.interaction_x = props[3]
    LWevent.interaction_y = props[4]
    LWevent.final_state_particle_0 = LW.ParticleType( props[5] )
    LWevent.final_state_particle_1 = LW.ParticleType( props[6] )
    LWevent.primary_type = LW.ParticleType( props[7] )
    LWevent.radius = props[8]
    LWevent.total_column_depth = props[9]
    LWevent.x = 0
    LWevent.y = 0
    LWevent.z = 0
    
    weight = weight_event(LWevent)

    # this would alert us that something bad is happening 
    if weight==np.nan:
        raise ValueError("Bad Weight!")

    return( weight*liveTime )


data_file = h5.File("data_output.h5")
injector_list = data_file.keys() # Each injector is treated as an entry in a dictionary 
print("Loaded {} Injectors: {}".format(len(injector_list), injector_list))

for injector in data_file.keys():
    print("Evaluating {}".format(injector))
    for event in range(len( data_file[injector]['properties'] )):
        print("     Event {0:06d} Weight: {}".format(event, get_weight( data_file[injector]['properties'][event]) ))

data_file.close()
