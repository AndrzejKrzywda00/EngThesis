/*
 * Data Flow Analyzer class implementation
 * The class takes in csv file in format described as:
 * id, x, y, z,
 */

#include <vector>
#include <string>
#include <map>
#include <algorithm>
#include "DataFlowAnalyzer.h"
#include "NanobotRecord.h"
#include "THzTransmissionSimulator.h"
#include "DataPackage.h"

namespace std {

    DataFlowAnalyzer::DataFlowAnalyzer (vector<string> rawData)
    {
        vector<ns3::NanobotRecord> records;
        for (long unsigned int i=0; i<rawData.size(); i++)
        {
            try
            {
                ns3::NanobotRecord record (rawData.at (i));
                records.push_back (record);
            }
            catch (const invalid_argument &e) {} // just ignore and don't create object
        }
        data = records;
    }

    DataFlowAnalyzer::~DataFlowAnalyzer () {}

    void
    DataFlowAnalyzer::SetNumberOfNanobots (int numberOfNanobots)
    {
        this->numberOfNanobots = numberOfNanobots;
    }

    void
    DataFlowAnalyzer::SetBloodVesselData (ns3::BloodVesselData data)
    {
        this->bloodVesselData = data;
    }

    void
    DataFlowAnalyzer::SetAccessPointVessel (int vesselId)
    {
        accessPointVesselId = vesselId;
        criticalVessels.push_back (vesselId);
    }

    void
    DataFlowAnalyzer::SetDataSourceVessels (vector<int> vesselIds)
    {
        dataSourceVesselIds = vesselIds;
        for (unsigned long int i=0; i<vesselIds.size(); i++)
        {
            criticalVessels.push_back (vesselIds.at (i));
        }
    }

    void
    DataFlowAnalyzer::Simulate ()
    {
        this->FilterNonCriticalVesselsData();
        map<int, vector<ns3::NanobotRecord>> nanobotsMap = this->SplitDatasetByNanobotId ();
        map<int, vector<ns3::NanobotRecord>> filteredNanobotsMap = this->FilterRepeatingRecordsInSingleVessel (nanobotsMap);
        this->SimulateDataFlow (filteredNanobotsMap);
    }

    map<int, vector<ns3::NanobotRecord>>
    DataFlowAnalyzer::FilterRepeatingRecordsInSingleVessel (map<int, vector<ns3::NanobotRecord>> vectorMap)
    {
        map<int, vector<ns3::NanobotRecord>> filteredMap;
        for (int i=1; i<=numberOfNanobots; i++)
        {
            pair<int, vector<ns3::NanobotRecord>> pair;
            pair.first = i;
            pair.second = this->FilterRepeatingRecordsInSingleVesselForNanobot (vectorMap.at (i));
            filteredMap.insert (pair);
        }
        return filteredMap;
    }

    vector<ns3::NanobotRecord>
    DataFlowAnalyzer::FilterRepeatingRecordsInSingleVesselForNanobot (vector<ns3::NanobotRecord> records)
    {
        vector<ns3::NanobotRecord> filteredRecords;
        const double timeStep = 0.5;
        for (unsigned long int i=0; i<records.size()-1; i++)
        {
            ns3::NanobotRecord thisRecord = records.at (i);
            ns3::NanobotRecord nextRecord = records.at (i+1);
            filteredRecords.push_back (thisRecord);
            while (nextRecord.GetNanobotId() == thisRecord.GetNanobotId()
            and nextRecord.GetBloodVesselId() == thisRecord.GetBloodVesselId()
            and nextRecord.GetTimestamp().GetSeconds()-thisRecord.GetTimestamp().GetSeconds() <= timeStep
            and i < records.size()-2)
            {
                i++;
                thisRecord = records.at (i);
                nextRecord = records.at (i+1);
            }
        }
        return filteredRecords;
    }

    void
    DataFlowAnalyzer::SimulateDataFlow (map<int, vector<ns3::NanobotRecord>> map)
    {
        for (int i=1; i<=numberOfNanobots; i++)
        {
            vector<ns3::NanobotRecord> dataRecords = map.at (i);
            this->SimulateForNanobot (dataRecords);
        }
    }

    void
    DataFlowAnalyzer::FilterNonCriticalVesselsData ()
    {
        vector<ns3::NanobotRecord> filteredData;
        for (unsigned long int i=0; i<data.size(); i++)
        {
            int bloodVesselId = data.at (i).GetBloodVesselId();
            if (find (criticalVessels.begin(), criticalVessels.end(), bloodVesselId) != criticalVessels.end())
            {
                filteredData.push_back (data.at (i));
            }
        }
        data = filteredData;
    }

    void
    DataFlowAnalyzer::SimulateForNanobot (vector<ns3::NanobotRecord> records)
    {
        ns3::DataPackage lastPackage;
        for (unsigned long int i=0; i<records.size(); i++)
        {
            ns3::NanobotRecord record = records.at (i);
            ns3::THzTransmissionSimulator simulator;
            if (find (dataSourceVesselIds.begin(), dataSourceVesselIds.end(), record.GetBloodVesselId()) != dataSourceVesselIds.end())
            {
                ns3::DataPackage package (record.GetTimestamp(), record.GetNanobotId(), "");

                simulator.SetTransmissionParameters (
                        bloodVesselData.GetSpeedOfBloodInVessel (record.GetBloodVesselId()),
                        bloodVesselData.GetLengthOfVessel (record.GetBloodVesselId())
                        );
                simulator.SimulateTransmission ();

                if (simulator.Success())
                {
                    cout << "Success" << endl;
                    lastPackage = package;
                }
                else
                {
                    cout << "Failed transmission" << endl;
                }
                cout << "Transmitting from data source to nanobot " << record.GetNanobotId() << " in vessel " << record.GetBloodVesselId() << " at time " << record.GetTimestamp().GetSeconds() << endl;
            }
            else
            {
                simulator.SetTransmissionParameters (
                        bloodVesselData.GetSpeedOfBloodInVessel (record.GetBloodVesselId()),
                        bloodVesselData.GetLengthOfVessel (record.GetBloodVesselId())
                        );
                simulator.SimulateTransmission ();
                if (simulator.Success() && lastPackage.GetStatus() != ns3::EMPTY)
                {
                    cout << "Success" << endl;
                    lastPackage.ReceiveData (record.GetTimestamp());
                    packages.push_back (lastPackage);
                }
                else
                {
                    cout << "Failed transmission" << endl;
                }
                cout << "Transmitting to access point from nanobot " << record.GetNanobotId() << " in vessel " << record.GetBloodVesselId() << " at time " << record.GetTimestamp().GetSeconds() << endl;
            }
        }
    }

    map<int, vector<ns3::NanobotRecord>>
    DataFlowAnalyzer::SplitDatasetByNanobotId ()
    {
        map<int, vector<ns3::NanobotRecord>> map;
        for (unsigned long int i=0; i<data.size(); i++)
        {
            ns3::NanobotRecord record = data.at (i);
            int nanobotId = record.GetNanobotId ();
            if (map.count (nanobotId) > 0)
            {
                map.at (nanobotId).push_back (record);
            }
            else
            {
                vector<ns3::NanobotRecord> singleElementRecord;
                singleElementRecord.push_back (record);

                pair<int, vector<ns3::NanobotRecord>> pair;
                pair.first = nanobotId;
                pair.second = singleElementRecord;
                map.insert (pair);
            }
        }
        return map;
    }

    vector<ns3::DataPackage>
    DataFlowAnalyzer::GetDataPackages ()
    {
        return packages;
    }
}