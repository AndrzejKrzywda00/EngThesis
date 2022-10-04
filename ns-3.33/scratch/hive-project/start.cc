#include <iostream>
#include "BloodVoyagerSRunner.h"
#include "DataBaseReader.h"
#include "DataFlowAnalyzer.h"
#include "THzTransmissionSimulator.h"
#include "BloodVesselData.h"

/*
 * Script to run big scale simulation of information propagation through medical nano-network in human organism.
 * Running scheme:
 * 1. Simulating nanobots movement in bloodstream
 * 2. Accessing, grouping and saving the data from file to objects
 * 3. Analysing the flow of information and saving statistics
 */

using namespace ns3;
using namespace std;

int
main ()
{
    Time::SetResolution (Time::FS);
    int hours = 1;
    int injectionVessel = 10;
    int numberOfNanobots = 5;

    int simulationDuration = hours * 60 * 2;

    BloodVoyagerSRunner::Run (numberOfNanobots, simulationDuration, injectionVessel);

    string dataFilePath = "/home/andrzej/ns-allinone-3.33/ns-3.33/csvNano.csv";
    DataBaseReader* reader = DataBaseReader::CreateFromFile (dataFilePath);
    vector<string> rawData = reader->GetAll ();

    DataFlowAnalyzer flow (rawData);
    flow.SetAccessPointVessel (17);
    vector<int> dataSources;
    dataSources.push_back (1);
    dataSources.push_back (5);
    dataSources.push_back (20);

    // preparing data of blood vessels
    ns3::BloodVesselData bvData;
    bvData.AddAll ("/home/andrzej/ns-allinone-3.33/ns-3.33/vasculature.csv");
    bvData.SaveToCsv();

    // preparing data of nanobots flow
    flow.SetDataSourceVessels (dataSources);
    flow.SetNumberOfNanobots (numberOfNanobots);
    flow.Simulate();

    vector<ns3::DataPackage> packages = flow.GetDataPackages();
    cout << "Successful packages size is " << packages.size() << endl;
    return 0;
}