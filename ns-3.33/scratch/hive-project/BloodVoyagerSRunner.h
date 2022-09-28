/*
 * Describing class to run Blood-Voyager-S with selected parameters
 */

#ifndef CLASS_BLOOD_VOYAGER_S_RUNNER
#define CLASS_BLOOD_VOYAGER_S_RUNNER

using namespace std;

namespace ns3
{
    class BloodVoyagerSRunner
    {
    public:

        /***
         * Run Blood Voyager S simulation with selected parameters to predefined file
         * @param numberOfNanobots is the number of nanobots being injected into bloodstream
         * @param simulationDuration is the duration of simulation in SECONDS
         * @param injectionVessel is the number of vessel nanobots will be injected in
         * @return 0 if successful, 1 otherwise
         */
        static int Run(unsigned int numberOfNanobots, unsigned int simulationDuration, unsigned int injectionVessel);
    };
}
#endif
