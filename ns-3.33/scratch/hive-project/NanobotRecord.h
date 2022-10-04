/*
 * Class representation of single record in csv file describing data sample produced by Blood-Voyager-S
 */
#include "/home/andrzej/ns-allinone-3.33/ns-3.33/src/core/model/nstime.h"
#include <string>

#ifndef NANOBOT_RECORD_H
#define NANOBOT_RECORD_H

namespace ns3 {

    class NanobotRecord {
    private:
        int nanobotId;
        double x;
        double y;
        double z;
        int bloodVesselId;
        int streamId;
        Time timestamp;
        int direction;          // 1 from data source to nanobot, -1 otherwise

    public:

        /***
         * Constructor for record class
         * @param record is the raw string record which will be parsed to data
         */
         NanobotRecord (std::string record);

         /***
          * Destructor
          */
         ~NanobotRecord ();

         /***
          * Get Nanobot ID
          */
         int GetNanobotId ();

         /***
          * Get Blood Vessel ID
          */
         int GetBloodVesselId ();

         /***
          * Get stream ID
          */
         int GetStreamId ();

         /***
          * return direction of transmission
          */
         int GetDirection ();

         /***
          * Get timestamp
          */
         Time GetTimestamp ();

         /***
          * Get X position of nanobot
          */
         double GetX ();

         /***
          * Get Y position of nanobot
          */
         double GetY ();

         /***
          * Get X position of nanobot
          */
         double GetZ ();

         /***
          * Setting direction of transmission
          */
         void SetDirection(int direction);
    };

}
#endif
