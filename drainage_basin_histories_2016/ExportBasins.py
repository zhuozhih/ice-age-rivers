#! /usr/bin/python
from grass import script as grass

# IMPORT TIME-STEPS
# from plot_topo_basins_alltimes_20160808.py
def get_time_steps():
  indexmaps = grass.parse_command('g.list', type='vect', patt='drainage_basins_??????').keys()
  indexmaps = sorted(indexmaps)[::-1]
  ages = []
  for indexmap in indexmaps:
    age = str(indexmap.split('_')[-1])
    if len(age) == 6:
      ages.append( age )
  return ages
  
# Limit plotted rivers to those that are being shown in the plots
# from plot_topo_basins_alltimes_20160808.py
wherestr = "river = 'Mississippi' OR river = 'Colorado' OR river = 'Rio Grande' OR river = 'Susquehanna' OR river = 'Hudson' OR river = 'Saint Lawrence' OR river = 'Hudson Strait' OR river = 'Mackenzie' OR river = 'Columbia'"

# EXPORT BASINS AT ALL TIME-STEPS
ages = get_time_steps()
for age in ages:
  print age
  drainage_basins = 'drainage_basins_'+age
  drainage_basins_ESurf = 'drainage_basins_ESurf_'+age
  #grass.run_command('v.build', map=drainage_basins, quiet=True)
  grass.run_command('v.extract', input=drainage_basins, output='drainage_basins_ESurf_', where=wherestr, overwrite=True, quiet=True)
  try:
    grass.run_command('v.out.ogr', input='drainage_basins_ESurf_', output=drainage_basins, quiet=True)
  except:
    print "... > Shapefile exists!"

for age in ages:
  try:
    grass.run_command('v.out.ogr', input='drainage_basins_ESurf_', output=drainage_basins+'.kml', format='KML', quiet=True)
  except:
    print "... > KML exists!"

