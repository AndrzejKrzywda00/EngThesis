/*
 * Class representing simulator of THz transmission with usage of Tera Sim module
 */

#include <iostream>
#include <fstream>
#include <string>
#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/mobility-module.h"
#include "ns3/internet-module.h"
#include "ns3/applications-module.h"
#include "ns3/thz-mac-nano.h"
#include "ns3/thz-channel.h"
#include "ns3/thz-udp-client-server-helper.h"
#include "ns3/thz-mac-nano-helper.h"
#include "ns3/thz-phy-nano-helper.h"
#include "ns3/thz-directional-antenna-helper.h"
#include "ns3/traffic-generator-helper.h"
#include "ns3/thz-energy-model-helper.h"
#include "NanobotRecord.h"

#ifndef THZ_TRANSMISSION_SIMULATOR_H
#define THZ_TRANSMISSION_SIMULATOR_H

namespace ns3 {

    class THzTransmissionSimulator {

    private:

        NodeContainer serverNodes;
        NodeContainer clientNodes;
        NodeContainer allNodes;
        NetDeviceContainer devices;
        Ipv4InterfaceContainer interfaces;
        uint8_t packetLength;
        uint8_t frameLength;
        int timeInMilliseconds;
        bool success = false;

        /***
         * Create node container for all nodes
         */
        void SetupNodes ();

        /***
         * Setup energy layer of parameters
         */
        void SetupEnergyParameters ();

        /***
         * Setup channel and MAC layer parameters
         */
        void SetupChannel ();

        /***
         * Setup mobility
         */
        void SetupMobility (double speed, double diameter, double vesselLength);

        /***
         * Setup IP layer network addresses
         */
        void SetupIPLayer ();

        /***
         * Setup traffic parameters
         */
        void SetupTraffic ();

    public:

        /***
         * Constructor
         */
        THzTransmissionSimulator ();

        /***
         * Destructor
         */
        ~THzTransmissionSimulator ();

        /***
         * Setup all default transmission parameters
         */
        void SetTransmissionParameters (double bloodVelocity, double vesselLength);

        /***
         * Simulate transmission with saved parameters
         */
        void SimulateTransmission ();

        /***
         * Get back result of transmission
         * @return true if successful, false otherwise
         */
        bool Success ();
    };
}
#endif
