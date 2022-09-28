/*
 * Implementation of class THZ Transmission Simulator
 */

#include "NanobotRecord.h"
#include "THzTransmissionSimulator.h"
#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/mobility-module.h"
#include "ns3/internet-module.h"
#include "ns3/applications-module.h"

namespace ns3 {

    THzTransmissionSimulator::THzTransmissionSimulator () {}

    THzTransmissionSimulator::~THzTransmissionSimulator () {}

    void
    THzTransmissionSimulator::SetTransmissionParameters (double vesselBloodSpeed, double vesselLength)
    {
        // in bytes
        packetLength = 20;
        frameLength = packetLength + 52;

        const double diameter = 0.25 / 100;
        int timeInMilliseconds = (int) round(vesselLength / vesselBloodSpeed * 1000);

        //LogComponentEnable("THzUdpClient", LOG_LEVEL_ALL);
        //LogComponentEnable("THzMacNano", LOG_LEVEL_ALL);
        //LogComponentEnable("THzNetDevice", LOG_LEVEL_ALL);
        //LogComponentEnable("THzPhyNano", LOG_LEVEL_ALL);
        //LogComponentEnable("THzChannel", LOG_LEVEL_ALL);
        //LogComponentEnable("TrafficGenerator", LOG_LEVEL_ALL);
        //LogComponentEnable("THzEnergyModel", LOG_LEVEL_ALL);
        //LogComponentEnable("THzSpectrumValueFactory", LOG_LEVEL_ALL);
        //LogComponentEnable("THzSpectrumPropagationLossModel", LOG_LEVEL_ALL);

        this->SetupNodes ();
        this->SetupEnergyParameters ();
        this->SetupChannel ();
        this->SetupMobility (vesselBloodSpeed, diameter, vesselLength);
        this->SetupIPLayer ();
        this->SetupTraffic (timeInMilliseconds);
    }

    bool
    THzTransmissionSimulator::Success ()
    {
        std::fstream in;
        in.open ("nano_2way_sucessful.txt");
        bool success = in.good();
        std::remove ("nano_2way_sucessful.txt");
        std::remove ("nano_2way_discarded.txt");
        return success;
    }

    void
    THzTransmissionSimulator::SimulateTransmission ()
    {
        Simulator::Stop (MilliSeconds (10));
        Simulator::Run ();
        Simulator::Destroy ();
    }

    void
    THzTransmissionSimulator::SetupNodes ()
    {
        serverNodes.Create (1);
        clientNodes.Create (1);
        allNodes.Add (serverNodes);
        allNodes.Add (clientNodes);
    }

    void
    THzTransmissionSimulator::SetupEnergyParameters ()
    {
        THzEnergyModelHelper energyModelHelper;
        energyModelHelper.SetEnergyModelAttribute ("THzEnergyModelInitialEnergy", StringValue ("0.0"));
        energyModelHelper.SetEnergyModelAttribute ("DataCallbackEnergy", DoubleValue (65));
        energyModelHelper.Install (allNodes);
    }

    void
    THzTransmissionSimulator::SetupChannel ()
    {
        Ptr<THzChannel> channel = CreateObject<THzChannel>();
        THzMacNanoHelper macNanoHelper = THzMacNanoHelper::Default();
        macNanoHelper.Set ("FrameLength", UintegerValue (frameLength));
        macNanoHelper.Set ("EnableRts", StringValue ("0"));

        Config::SetDefault ("ns3::THzSpectrumValueFactory::NumSample", DoubleValue (10));
        THzPhyNanoHelper phyNanoHelper = THzPhyNanoHelper::Default();
        phyNanoHelper.SetPhyAttribute ("PulseDuration", TimeValue (FemtoSeconds (100)));
        phyNanoHelper.SetPhyAttribute ("Beta", DoubleValue (100));

        THzDirectionalAntennaHelper thzDirAntenna = THzDirectionalAntennaHelper::Default ();
        THzHelper thz;

        devices = thz.Install (allNodes, channel, phyNanoHelper, macNanoHelper, thzDirAntenna);
    }

    void
    THzTransmissionSimulator::SetupMobility (double speed, double diameter, double vesselLength)
    {
        MobilityHelper mobilityHelper;
        Ptr<ListPositionAllocator> positionAllocator = CreateObject<ListPositionAllocator>();
        positionAllocator->Add (Vector (0.0, 0.0, 0.0));
        mobilityHelper.SetPositionAllocator (positionAllocator);
        mobilityHelper.SetMobilityModel ("ns3::ConstantPositionMobilityModel");
        mobilityHelper.Install (serverNodes);

        double radius = diameter / 2;
        mobilityHelper.SetPositionAllocator ("ns3::UniformDiscPositionAllocator",
                                             "X", DoubleValue (radius),
                                             "Y", DoubleValue (0),
                                             "Z", DoubleValue (-vesselLength/2),
                                             "rho", DoubleValue (radius));
        mobilityHelper.SetMobilityModel ("ns3::ConstantVelocityMobilityModel");
        mobilityHelper.Install (clientNodes);

        for (uint i=0; i<clientNodes.GetN(); i++)
        {
            Ptr<ConstantVelocityMobilityModel> model = clientNodes.Get(i)->GetObject<ConstantVelocityMobilityModel>();
            model->SetVelocity (Vector (0.0, 0.0, speed));
        }
    }

    void
    THzTransmissionSimulator::SetupIPLayer ()
    {
        InternetStackHelper internetStackHelper;
        internetStackHelper.Install (allNodes);
        Ipv4AddressHelper ipv4AddressHelper;
        ipv4AddressHelper.SetBase ("10.16.1.0", "255.255.255.0");
        interfaces = ipv4AddressHelper.Assign (devices);
    }

    void
    THzTransmissionSimulator::SetupTraffic (int timeInMilliseconds)
    {
        int port = 8050;
        THzUdpServerHelper serverHelper (port);
        ApplicationContainer apps = serverHelper.Install (serverNodes);
        apps.Start (MicroSeconds (10));
        apps.Stop (MilliSeconds (timeInMilliseconds + 10));
        std::cout << "Setting up simulation time for " << timeInMilliseconds << " ms" << std::endl;

        THzUdpClientHelper clientHelper (interfaces.GetAddress (0), port);
        clientHelper.SetAttribute ("PacketSize", UintegerValue (packetLength));
        apps = clientHelper.Install (clientNodes);

        apps.Start (MicroSeconds (10));
        apps.Stop (MilliSeconds (timeInMilliseconds + 10));
    }
}
