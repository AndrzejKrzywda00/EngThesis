/*
 * Implementation of class DataBaseReader
 */

#include <iostream>
#include <fstream>
#include <vector>
#include "DataBaseReader.h"

namespace std {

    DataBaseReader::DataBaseReader (vector<string> dataVector)
    {
        data = dataVector;
    }

    DataBaseReader*
    DataBaseReader::CreateFromFile (string fileName)
    {
        fstream file;
        file.open (fileName, ios::in);
        vector<string> lines;

        if (file.is_open())
        {
            string line;
            while (getline (file, line))
            {
                lines.push_back (line);
            }
        }
        else
        {
            std::cout << "File could not be opened" << std::endl;
        }

        return new DataBaseReader (lines);
    }

    vector<string>
    DataBaseReader::GetAll ()
    {
        return data;
    }
}