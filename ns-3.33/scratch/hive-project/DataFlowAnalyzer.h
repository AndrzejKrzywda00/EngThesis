/*
 * Data Flow Analyzer class description
 */

#include <string>
#include <vector>
#include <map>
#include "NanobotRecord.h"
#include "DataPackage.h"
#include "BloodVesselData.h"

#ifndef DATA_FLOW_ANALYZER_H
#define DATA_FLOW_ANALYZER_H

namespace std {

    class DataFlowAnalyzer {

    private:

        vector<int> dataSourceVesselIds;
        int accessPointVesselId;
        vector<ns3::NanobotRecord> data;
        vector<int> criticalVessels;
        int numberOfNanobots;
        vector<ns3::DataPackage> packages;
        ns3::BloodVesselData bloodVesselData;

        /***
         * Filters out measurement points in non-critical vessels
         */
        void FilterNonCriticalVesselsData ();

        /***
         * Conduct the simulation for single nanobot
         * @param nanobotId is the selected nanobot
         */
        void SimulateForNanobot (vector<ns3::NanobotRecord> records);

        /***
         * Splits dataset by nanobot into map int (key) nanobotId : vector<ns3::NanobotRecord> (value) records
         */
        map<int, vector<ns3::NanobotRecord>> SplitDatasetByNanobotId ();

        /***
         * Simulate data flow for all filtered records
         * @param map is the mapping nanobotId -> vector of records of data
         */
        void SimulateDataFlow (map<int, vector<ns3::NanobotRecord>> map);

        /***
         * Removes excessive records for single vessel
         */
        map<int, vector<ns3::NanobotRecord>> FilterRepeatingRecordsInSingleVessel (map<int, vector<ns3::NanobotRecord>> map);

        /***
         * Removes excessive records for single vessel for single nanobot
         */
        vector<ns3::NanobotRecord> FilterRepeatingRecordsInSingleVesselForNanobot (vector<ns3::NanobotRecord> records);

    public:

        /***
         * Creates instance with loaded data to perform more operations on
         * @param data are the rows of .csv file
         */
        DataFlowAnalyzer (vector<string> data);

        ~DataFlowAnalyzer ();

        /***
         * Setting vessel ids in which will be data sources
         * @param vesselIds vector of unique values in range (1, 94)
         */
        void SetDataSourceVessels (vector<int> vesselIds);

        /***
         * Setting vessel id for access point where data fill flow
         * @param vesselId integer with vessel id in range (1, 94)
         */
        void SetAccessPointVessel (int vesselId);

        /***
         * Setting number of nanobots in simulation
         * @param numberOfNanobots is the number to be set (must be grater than 2)
         */
        void SetNumberOfNanobots (int numberOfNanobots);

        /***
         * Simulate data flow in provided nanobot movement scheme
         */
        void Simulate ();

        /***
         * Get result of simulation - vector of successful data packages
         * @return vector of ns3::DataPackage
         */
        vector<ns3::DataPackage> GetDataPackages ();

        /***
         * Setter for blood vessel data util class
         */
        void SetBloodVesselData(ns3::BloodVesselData data);
    };
}
#endif
