/*
 * Implementation of data holder class Nanobot Record
 */

#include <string>
#include <vector>
#include "NanobotRecord.h"
#include "/home/andrzej/ns-allinone-3.33/ns-3.33/src/core/model/nstime.h"

namespace ns3 {

    NanobotRecord::NanobotRecord (std::string record)
    {
        std::vector<std::string> segment;
        const char separator = ',';
        std::stringstream stream (record);
        std::string element;

        while (std::getline (stream, element, separator))
        {
            segment.push_back (element);
        }

        if (segment.size () != 7) throw std::invalid_argument ("Line is incomplete or too long");

        // setting up data
        nanobotId = std::stoi (segment.at (0));
        x = std::stod (segment.at (1));
        y = std::stod (segment.at (2));
        z = std::stod (segment.at (3));
        bloodVesselId = std::stoi (segment.at (4));
        streamId = std::stoi (segment.at (5));
        timestamp = Time (segment.at (6));
        direction = 0;
    }

    void
    NanobotRecord::SetDirection (int direction)
    {
        this->direction = direction;
    }

    int
    NanobotRecord::GetDirection ()
    {
        return direction;
    }

    int
    NanobotRecord::GetStreamId ()
    {
        return streamId;
    }

    NanobotRecord::~NanobotRecord () {}

    int
    NanobotRecord::GetBloodVesselId ()
    {
        return bloodVesselId;
    }

    int
    NanobotRecord::GetNanobotId ()
    {
        return nanobotId;
    }

    Time
    NanobotRecord::GetTimestamp () {
        return timestamp;
    }

    double
    NanobotRecord::GetX ()
    {
        return x;
    }

    double
    NanobotRecord::GetY ()
    {
        return y;
    }

    double
    NanobotRecord::GetZ ()
    {
        return z;
    }
}