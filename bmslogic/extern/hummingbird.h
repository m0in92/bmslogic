/**
 * @file hummingbird.h
 * @author Moin Ahmed (moinahmed100@gmail.com)
 * @brief contains the functionality to read csv files and extract data.
 * @version 0.1
 * @date 2024-05-15
 * 
 * @copyright Copyright (c) 2024
 * 
 */



#ifndef BMSLOGIC_HUMMINGBIRD_H
#define BMSLOGIC_HUMMINGBIRD_H

#include <vector>
#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <stdexcept>
#include <algorithm>

namespace HB {
    /**
    * DataFrames
    *
    * Class for storing, accessing, and modifying dataframes.
    */
    class DataFrames {
    public:
        // Accessor Functions
        std::vector<std::string> getIndex() { return index; }
        std::vector<std::string> getColNames() { return colName; }
        std::vector<std::vector<std::string>> getData();
        int getColIndex(std::string);
        int getIndexIndex(std::string);
        DataFrames getColValues(std::string);
        DataFrames getIndexValues(std::string);
        std::string getValue(const std::string inputColName, const std::string inputIndexName);
        // Modifier Functions
        void set_index(std::vector<std::string> inputIndex) { index = inputIndex; }
        void set_colname(std::vector<std::string> inputColName) { colName = inputColName; }
        void set_data(std::vector<std::vector<std::string>> inputData) { data = inputData; }
        // Display functions
        void display_colnames();
        void display_dataframes();
        // operator overloads
        DataFrames operator[](std::string colName);
        // Search functions
        std::vector<std::string> colValueEqualTo(std::string colName,std::string inputValue);
        // Helper functions
        DataFrames create_empty_DataFrames();
    private:
        std::vector<std::string> index;
        std::vector<std::string> colName;
        // vector containing string vectors. Each string vector is a row or a data entry.
        std::vector<std::vector<std::string>> data;
    };

    DataFrames read_csv(std::string, int colNameIndex = 0, int indexRow = 0);
}

#endif //BMSLOGIC_HUMMINGBIRD_H