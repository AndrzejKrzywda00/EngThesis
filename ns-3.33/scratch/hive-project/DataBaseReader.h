/*
 * Class for reading the .csv file with predefined structure - a result of running BloodVoyagerS
 */

#include <vector>
#include <string>

#ifndef DATA_BASE_READER_H
#define DATA_BASE_READER_H

namespace std {

    class DataBaseReader {

    private:
        vector<string> data;

        /***
         * Private constructor for the class
         * @param dataVector is the data passed
         */
        DataBaseReader (vector<string> dataVector);

    public:

        /***
         * Create Database reader instance with data loaded from .csv file
         * @param fileName is the filename class will try to access
         * @return instance with data saved
         */
        static DataBaseReader* CreateFromFile (string fileName);

        /***
         * Get data extracted from file
         */
        vector<string> GetAll ();

        /***
         * Destructor
         */
        ~DataBaseReader ();
    };
}
#endif
