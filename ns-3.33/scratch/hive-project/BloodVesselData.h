/*
 * Class to track parameter information of every blood vessel
 */

#include <map>
#include <vector>
#include "ns3/core-module.h"

#ifndef BLOOD_VESSEL_DATA_H
#define BLOOD_VESSEL_DATA_H

namespace ns3 {

    class BloodVesselData {

    private:

        // data scheme is key: id, values[0]: speed class, values[1]: length
        std::map<int, std::vector<double>> data;

        /***
         * Save data from opened file to map instance
         */
        void PutDataToMap (std::string line);

        /***
         * Get blood velocity in m/s
         */
        double GetBloodVelocityByVesselId (int vesselType);

        /***
         * Create length of vector of difference between start and end
         * @param start is starting vector
         * @param end is ending vector
         * @return length in meters
         */
        double CreateBloodVesselLength (Vector start, Vector end);

    public:

        /***
         * Empty constructor
         */
        BloodVesselData ();

        /***
         * Create instance of class from file
         * @return blood vessels data class with data saved
         */
        void AddAll (std::string filePath);

        /***
         * No params destructor
         */
        ~BloodVesselData ();

        /***
         * Get speed of blood in vessel by id
         * @param vesselId is the id to extract data by
         * @return double speed value
         */
        double GetSpeedOfBloodInVessel (int vesselId);

        /***
         * Get length of the vessel in m
         * @param vesselId is the id to extract dat by
         * @return double length value
         */
        double GetLengthOfVessel (int vesselId);
    };
}

#endif