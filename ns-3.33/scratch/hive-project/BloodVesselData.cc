/*
 * Implementation of static holder of data of blood vessels
 */

#include "BloodVesselData.h"
#include "ns3/core-module.h"

namespace ns3 {

    BloodVesselData::BloodVesselData () {}

    BloodVesselData::~BloodVesselData () {}

    double
    BloodVesselData::GetLengthOfVessel (int vesselId)
    {
        return data.at (vesselId).at (1);
    }

    void
    BloodVesselData::SaveToCsv ()
    {
        std::ofstream bvFile;
        bvFile.open ("vasculature-data.csv", std::ofstream::out | std::ios::app);
        for (unsigned long int i=1; i<=94; i++)
        {
            double radius = 0.0025;
            std::vector<double> dataVector = data.at (i);
            bvFile <<
            i << "," <<
            dataVector.at (0) << "," <<
            dataVector.at (1) << "," <<
            radius << "," <<
            std::endl;
        }
        bvFile.close();
    }

    double
    BloodVesselData::GetSpeedOfBloodInVessel (int vesselId)
    {
        return data.at (vesselId).at (0);
    }

    void
    BloodVesselData::PutDataToMap (std::string line)
    {
        std::vector<std::string> segment;
        const char separator = ',';
        std::stringstream stream (line);
        std::string element;

        while (std::getline (stream, element, separator))
        {
            segment.push_back (element);
        }

        int vesselId = std::stoi (segment.at (0));
        double bloodSpeed = GetBloodVelocityByVesselId (std::stoi (segment.at (1)));
        Vector startVector = Vector (
                std::stoi (segment.at (2)),
                std::stoi (segment.at (3)),
                std::stoi (segment.at (4))
                );
        Vector endVector = Vector (
                std::stoi (segment.at (5)),
                std::stoi (segment.at (6)),
                std::stoi (segment.at (7))
                );
        double vesselLength = this->CreateBloodVesselLength (startVector, endVector);

        std::pair<int, std::vector<double>> pair;
        pair.first = vesselId;
        std::vector<double> dataVector;
        dataVector.push_back (bloodSpeed);
        dataVector.push_back (vesselLength);
        pair.second = dataVector;

        data.insert (pair);
    }

    double
    BloodVesselData::GetBloodVelocityByVesselId (int vesselType)
    {
        double bloodFlowVelocity = 0;
        double normalization = 100;

        // ARTERY
        if (vesselType == 0) bloodFlowVelocity = 10.0;

        // VEIN
        if (vesselType == 1) bloodFlowVelocity = 3.7;

        // ORGAN
        if (vesselType == 2) bloodFlowVelocity = 1.0;
        return bloodFlowVelocity / normalization;
    }

    double
    BloodVesselData::CreateBloodVesselLength (Vector start, Vector end)
    {
        Vector absoluteVector = Vector (end.x - start.x, end.y - start.y, end.z - start.z);
        return absoluteVector.GetLength() / 100;
    }

    void
    BloodVesselData::AddAll (std::string filePath)
    {
        std::ifstream file {filePath};
        if (file.is_open())
        {
            std::string line;
            while (std::getline (file, line))
            {
                PutDataToMap (line);
            }
        }
        else
        {
            std::cout << "File could not be opened" << std::endl;
        }
    }
}