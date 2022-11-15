# Engineering Thesis Project

Analysing efficiency of simulated flow guided medical nano-network consisting of some number of nanobots.
Flow of nanobots is simulated by ns3 module Blood-Voyager-S, then evaluated in four defined scenarios by created python modules

## Main 'Medical' Scenarios:

### Scenario 1
Plotting probability density function and distribution method describing chances of delivery in time span of width 30 minutes
as function of time of flow in blood system.

a) Nano-sensor working in superior vena cava and reception device in one of jugular veins (one with larger blood flow)

b) Nano-sensor working in superior vena cava and reception device in cephalic vein in left arm

### Scenario 2
Plotting mean delivery time of packet by the system depending on number of nanobots


## Additional Scenarios:

### Scenario 1
Measuring throughput on the cephalic vein, by assessing how many data will be delivered assuming all nanobots are carrying information
Both directions will be analysed, from nano-sensor and to access point device

### Scenario 2
Probability of packet delivery depending on length of packet (from 64 bits up to 512 bits)

### Scenario 3
Measuring collision ratio defined as number of collisions divided by number of flow accidents depending on number of nanobots