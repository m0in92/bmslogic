/**
 * @file hummingbird.cpp
 * @author Moin Ahmed (moinahmed100@gmail.com)
 * @brief contains the functionality to read csv files and extract data.
 * @version 0.1
 * @date 2024-05-15
 * 
 * @copyright Copyright (c) 2024
 * 
 */

#include "HummingBird.h"


namespace HB {
    /**
    * getData
    *
    * Getter function to get the data body.
    *
    * Parameters:
    *     None
    *
    * Returns:
    *     (std::vector<std::vector<std::string>>) DataFrame's data body. It is a vector within a vector.
    *                                             Can be indexed as data[row no.][col no.]
    *
    * Throws:
    *     None
    */
    std::vector<std::vector<std::string>> DataFrames::getData() {
        return data;
    }

    /**
    * getColIndex
    *
    * Obtain the index of the column from all the column names by inputting the column name.
    *
    * Parameters:
    *     inputColName: (std::string) the desired column name.
    *
    * Throws:
    *     std::invalid_argument: throws when the inputted column name is not present in the data's column names.
    */
    int DataFrames::getColIndex(std::string inputColName) {
        int colIndex = -1;
        for (int i = 0; i < colName.size(); i++) {
            if (colName[i].compare(inputColName) == 0) {
                colIndex = i;
            }
        }
        if (colIndex == -1)
            throw std::invalid_argument("Invalid column name.");
        return colIndex;
    }

    /**
    * getIndexIndex
    *
    * Obtains the index of the DataFrame's index using in inputted index name.
    *
    * Parameters:
    *     inputIndexName: (std::string) input index name.
    *
    * Returns:
    *     (int) index
    *
    * Throws:
    *     std::invalid_argument: thrown when invalid index name is inputted.
    */
    int DataFrames::getIndexIndex(std::string inputIndexName) {
        int rowIndex = -1;
        for (int i = 0; i < index.size(); i++) {
            if (index[i].compare(inputIndexName) == 0) {
                rowIndex = i;
            }
        }
        if (rowIndex == -1)
            throw std::invalid_argument("Invalid index name.");
        return rowIndex;
    }

    /**
    * getColVgetColValues
    *
    * Obtain the values contained within a column of the HB::DataFrame.
    *
    * Parameters:
    *     inputColName: (std::string) the input column name
    *
    * Return:
    *     (HB::DataFrames) DataFrame containing only the column
    *
    * Throws:
    *     std::invalid_argument: thrown when invalid col name is inputted.
    *                            Thrown when DataFrames::getColName() is called within this function.
    */
    DataFrames DataFrames::getColValues(std::string inputColName) {
        try {
            int colIndex = DataFrames::getColIndex(inputColName);
            std::vector<std::vector<std::string>> rowTemp;
            //        std::vector<std::string> colTemp;
            for (int i = 0; i < data.size(); i++) {
                std::vector<std::string> colTemp;
                colTemp.push_back(data[i][colIndex]);
                rowTemp.push_back(colTemp);
            }
            DataFrames dfTemp;
            dfTemp.set_data(rowTemp);
            dfTemp.set_index(index);
            std::vector<std::string> colNameTemp;
            colNameTemp.push_back(inputColName);
            dfTemp.set_colname(colNameTemp);
            return dfTemp;
        }
        catch (std::invalid_argument& e) {
            std::cout << e.what() << std::endl;
            return create_empty_DataFrames();
        }
    }

    /**
    * getindexValues
    *
    * Returns the DataFrame with values on the inputted row name:
    *
    * Parameters:
    *     inputIndexName: (std::string) index name.
    *
    * Returns:
    *     (HB::DataFrames) the index is the column names of the orignal DataFrame and the column name is the index name.
    *
    * Throws:
    *     std::invalid_argument: thrown when inputted name is not present in the DataFrames.
    */
    DataFrames DataFrames::getIndexValues(std::string inputIndexName) {
        try {
            int indexIndex = getIndexIndex(inputIndexName);
            // initiate dataframes
            DataFrames DB;
            // create and set col
            std::vector<std::string> colNameTemp;
            colNameTemp.push_back(inputIndexName);
            DB.set_colname(colNameTemp);
            // create and set index
            DB.set_index(colName);
            // create and set data
            std::vector<std::vector<std::string>> dataTemp;
            for (size_t i = 0; i < data[indexIndex].size(); i++) {
                std::vector <std::string> dataVec;
                dataVec.push_back(data[indexIndex][i]);
                dataTemp.push_back(dataVec);
            }
            DB.set_data(dataTemp);
            return DB;
        }
        catch (std::invalid_argument& e) {
            // Ouput the error message and return an empty DataFrames.
            std::cout << e.what() << std::endl;
            DataFrames DB;
            return DB;
        }
    }

    /**
    * getValue
    *
    * Obtain the value (in std::string) in the dataFrame using index and column names.
    *
    * Parameters:
    *     inputcolName: (std::string) input column name.
    *     inputIndexName: (std::string) input index name.
    *
    * Return:
    *     (std::string) a string cotaining the value
    *
    * Throws:
    *     std::invalid_argument: thrown when invalid column name is inputted.
    *     std::invalid_argument: thrown when invalid index name is inputted.
    */
    std::string DataFrames::getValue(const std::string inputcolName, const std::string inputIndexName) {
        try {
            DataFrames df = DataFrames::getColValues(inputcolName);
            int indexIndex = DataFrames::getIndexIndex(inputIndexName);
            const int colIndex = 0;
            return df.getData()[indexIndex][colIndex];
        }
        catch (const std::invalid_argument& e) {
            std::cout << "Invalid index name: " << inputIndexName << " " << e.what() << std::endl;
            std::string InvalidReturnValue = "None";
            return InvalidReturnValue;
        }
    }

    /**
    * display_colnames()
    *
    * Displays all the columns in the DataFrames.
    *
    * Parameters:
    *     None
    *
    * Returns:
    *    None
    *
    * Throws:
    *     None
    */
    void DataFrames::display_colnames() {
        std::cout << " "; // initial delimiters
        for (int i = 0; i < colName.size(); i++) {
            std::cout << colName[i] << " ";
        }
        std::cout << std::endl;
    }

    void DataFrames::display_dataframes() {
        // Header
        DataFrames::display_colnames();
        for (int rowIndex = 0; rowIndex < data.size(); rowIndex++) {
            // on a single line.
            std::cout << index[rowIndex] << " ";
            for (int colIndex = 0; colIndex < data[rowIndex].size(); colIndex++) {
                std::cout << data[rowIndex][colIndex] << " ";
            }
            std::cout << std::endl;
        }
    }

    /**
    * operator[]
    *
    * operator overload for indexing
    *
    * Parameters:
    *     colName:(std::string) colName
    *
    * Returns:
    *     DataFrame with the column name.
    *
    * Throws:
    *     std::invalid_argument: Thrown when invalid index name is inputted.
    *                            Thrown when DataFrames::getColValues() is called within this function.
    */
    DataFrames DataFrames::operator[](std::string colName) {
        return getColValues(colName);
    }

    std::vector<std::string> DataFrames::colValueEqualTo(std::string colName, std::string inputValue) {
        try {
            std::vector<std::string> indexcontainingValues;
            DataFrames colValues = getColValues(colName);
            for (size_t i = 0; colValues.getIndex().size(); i++) {
                if (colValues.getData()[i][0] == inputValue) {
                    indexcontainingValues.push_back(colValues.getIndex()[i]);
                }
            }
            return indexcontainingValues;
        }
        catch (std::invalid_argument& e) {
            std::cout << e.what() << std::endl;
            std::vector<std::string> indexcontainingValues;
            return indexcontainingValues;
        }
    }

    /*
    * create_empty_DataFrames
    *
    * returns an empty DataFrame
    *
    * Parameters:
    *     None
    *
    *
    * Returns:
    *     (DataFrames) an empty DataFrames
    *
    * Throws:
    *     None
    */
    DataFrames DataFrames::create_empty_DataFrames() {
        std::vector<std::string> emptyIndex;
        std::vector<std::string> emptyCol;
        std::vector<std::vector<std::string>> emptyData;
        DataFrames resDataFrames;
        resDataFrames.set_data(emptyData);
        resDataFrames.set_colname(emptyCol);
        resDataFrames.set_index(emptyIndex);
        return resDataFrames;
    }

    /**
    * read_csv
    *
    * function to parse through the csv file and create HummingBird DataFrame.
    *
    * Parameters:
    *     filePath: std::string of the filepath of the csv file.
    *     colNameIndex: int representing the index column in the csv file. Default is set to 0.
    *     indexRow: int representing the index row of the csv file. Default is set to 0.
    *
    * Return:
    *     HummingBird DataFrame structure
    *
    * Throws:
    *     None
    */
    DataFrames read_csv(std::string filePath, int colNameIndex, int indexRow) {
        std::ifstream inputFile;
        inputFile.open(filePath);

        // initialize the dataframe and line
        std::string line = "";
        std::vector<std::vector<std::string>> dataFrameTemp;
        std::vector<std::string> colNameTemp;
        std::vector<std::string> indexTemp;

        int index = 0;
        while (std::getline(inputFile, line)) {
            // initialize row entry (single entry within a row, rowInput(entire row), and rowVector (vector containing all
            // row entries.)
            std::string  rowEntry = "";
            std::stringstream rowInput(line);
            std::vector<std::string> rowVector;
            int colIndex = 0;
            while (std::getline(rowInput, rowEntry, ',')) {
                if (colIndex == indexRow) {
                    if (index > 0)
                        indexTemp.push_back(rowEntry);
                }
                else
                    rowVector.push_back(rowEntry);
                colIndex++;
            }
            if (index == colNameIndex) {
                colNameTemp = rowVector; // add colname
            }
            else {
                dataFrameTemp.push_back(rowVector); // add rowVector to the dataframe vector.
                //            indexTemp.push_back(std::to_string(index-1));
            }
            index++;
            line = "";
        }
        DataFrames dataFrame;
        dataFrame.set_index(indexTemp);
        dataFrame.set_colname(colNameTemp);
        dataFrame.set_data(dataFrameTemp);
        return dataFrame;
    }
}