/*
 * Data Package class implementation
 */

#include "DataPackage.h"

namespace ns3 {

    DataPackage::~DataPackage () {}

    DataPackage::DataPackage ()
    {
        this->status = ns3::EMPTY;
    }

    DataPackage::DataPackage (ns3::Time sentTime, int nanobotId, std::string data)
    {
        this->sentTime = sentTime;
        this->nanobotId = nanobotId;
        this->data = data;
        this->status = ns3::SENT;
    }

    std::string
    DataPackage::GetData ()
    {
        return data;
    }

    Time
    DataPackage::GetDataDeliveryDuration ()
    {
        return receivedTime - sentTime;
    }

    void
    DataPackage::ReceiveData (ns3::Time receptionTime)
    {
        status = ns3::RECEIVED;
        this->receivedTime = receptionTime;
    }

    ns3::Status
    DataPackage::GetStatus ()
    {
        return status;
    }
}