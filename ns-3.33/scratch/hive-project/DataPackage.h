/*
 * Class declaration for Data Package class holding virtual package of data for simulator
 */

#include "/home/andrzej/ns-allinone-3.33/ns-3.33/src/core/model/nstime.h"

#ifndef DATA_PACKAGE_H
#define DATA_PACKAGE_H

namespace ns3 {

    enum Status {
        SENT, RECEIVED, EMPTY
    };

    class DataPackage {

    private:

        Status status;
        Time sentTime;
        Time receivedTime;
        int nanobotId;
        std::string data;

    public:

        /***
         * Empty constructor
         */
        DataPackage ();

        /***
         * Constructor, taking in all fields
         */
        DataPackage (Time sentTime, int nanobotId, std::string data);

        /***
         * Destructor
         */
        ~DataPackage();

        /***
         * Get data delivery duration
         */
        Time GetDataDeliveryDuration ();

        /***
         * Get exact data emitted by data source
         * @return data string
         */
        std::string GetData ();

        /***
         * Getting status of package
         * @return status enum object
         */
        Status GetStatus ();

        /***
         * Set the time of reception of data and finish handling of this packet
         * @param time is the time of reception
         */
        void ReceiveData (Time receptionTime);
    };
}

#endif
