/*
 * Class BloodVoyagerSRunner implementation
 */

#include "BloodVoyagerSRunner.h"
#include "../../src/blood-voyager-s/Bloodcircuit.h"

namespace ns3 {
    int
    BloodVoyagerSRunner::Run (unsigned int numberOfNanobots, unsigned int simulationDuration, unsigned int injectionVessel) {
        CommandLine cmd;
        cmd.AddValue ("simulationDuration", "simulationDuration", simulationDuration);
        cmd.AddValue("numOfNanobots", "numOfNanobots", numberOfNanobots);
        cmd.AddValue ("injectionVessel", "injectionVessel", injectionVessel);
        return Bloodcircuit::BeginnSimulation (simulationDuration, numberOfNanobots, injectionVessel);
    }
}

