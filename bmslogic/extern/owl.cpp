/**
 * @file owl.cpp
 * @author Moin Ahmed (moinahmed100@gmail.com)
 * @brief The OWL package is obtained from : https://github.com/m0in92/OWL which is also created by Moin Ahmed on 7/4/2023.
 * This header file was added to BMSLogic on May 3, 2024 and will be modified as seem fit.
 * @version 0.1
 * @date 2024-05-03
 *
 * @copyright Copyright (c) 2024
 *
 */

#include "owl.h"

namespace OWL
{
    /*
     * ------------------------------------------------------------------
     * methods for ArrayXD class below
     * -------------------------------------------------------------------
     */

    /**
     * ArrayXD
     *
     * Default Constructor. Sets array attribute to an empty array.
     *
     * Parameters:
     *     None
     *
     * Returns:
     *     None
     */
    ArrayXD::ArrayXD()
    {
        array = std::vector<double>();
        arrayLength = size();
    }

    /**
     * ArrayXD
     *
     * Overload constructor. Sets the attribute array to a std::vector and sets the arrayLength.
     *
     * Parameters:
     *    vec: std::vector type
     *
     * Returns:
     *     None
     *
     * Throws:
     *     None
     */
    ArrayXD::ArrayXD(std::vector<double> &vec)
    {
        array = vec;
        arrayLength = vec.size();
    }

    /**
     * setArray
     *
     * sets existing std::vector to the ArrayXD instance by setting the array attribute.
     *
     * Parameters:
     *     newArray: std::vector
     *
     * Returns:
     *     void
     *
     * Throws:
     *     None
     */
    void ArrayXD::setArray(std::vector<double> &newArray)
    {
        array = newArray;
        arrayLength = newArray.size();
    }

    /**
     * display
     *
     * Displays the array on the console.
     *
     * Parameters:
     *     None
     *
     * Throws:
     *     None
     */
    void ArrayXD::display()
    {
        std::cout << std::endl;
        for (const auto element : array)
        {
            std::cout << element << std::endl;
        }
        std::cout << std::endl;
    }

    /**
     * sum
     *
     * finds the sum of the elemets in the array
     *
     * Parameters:
     *     None
     *
     * Returns:
     *     (double) sum of all the elements in the array
     *
     * Throws:
     *     None
     */
    double ArrayXD::sum()
    {
        double currentSum = 0;
        for (size_t i = 0; i < arrayLength; i++)
        {
            currentSum += array[i];
        }
        return currentSum;
    }

    /*
     * compareArrayLength
     *
     * compares the length of this instance OWL::ArrayXD with another OWL::ArrayXD instance.
     *
     * Parameters:
     *     otherArray: OWL::ArrayXD object.
     *
     * Return:
     *     (bool) true if the lengths match.
     *
     * Throws:
     *     std::invalidargument: thrown when the array lengths do not match.
     */
    bool ArrayXD::compareArrayLength(ArrayXD &otherArray)
    {
        bool flag = false;
        if (arrayLength == otherArray.getArrayLength())
        {
            flag = true;
        }
        else
        {
            throw std::invalid_argument("array lengths do not match.");
        }
        return flag;
    }

    /**
     * isEqual
     *
     * checks if the array is equal to the inputted array.
     *
     * Parameters:
     *     otherArray: (OWL::ArrayXD) input array
     *
     * Returns:
     *     (bool) true if arrays are equal, false if they are not.
     *
     * Throws:
     *     None
     */
    double ArrayXD::isEqual(ArrayXD &otherArray)
    {
        try
        {
            if (!compareArrayLength(otherArray))
            {
                return false;
            }
            else
            {
                bool flag = false;
                for (size_t i = 0; i < arrayLength; i++)
                {
                    if (array[i] == otherArray[i])
                    {
                        flag = true;
                    }
                    else
                    {
                        flag = false;
                        return flag;
                    }
                }
                return flag;
            }
        }
        catch (std::invalid_argument &e)
        {
            return false;
        }
    }

    /**
     * isApproxEqual
     *
     * checks if the array is equal to the inputted array.
     *
     * Parameters:
     *     otherArray: (OWL::ArrayXD) input array
     *     tol: (double) acceptable error range
     *
     * Returns:
     *     (bool) true if arrays are equal, false if they are not.
     *
     * Throws:
     *     None
     */
    double ArrayXD::isApproxEqual(ArrayXD &otherArray, double tol)
    {
        try
        {
            if (!compareArrayLength(otherArray))
            {
                return false;
            }
            else
            {
                bool flag = false;
                for (size_t i = 0; i < arrayLength; i++)
                {
                    if ((array[i] >= (otherArray[i] - tol)) && (array[i] <= (otherArray[i] + tol)))
                    {
                        flag = true;
                    }
                    else
                    {
                        flag = false;
                        return flag;
                    }
                }
                return flag;
            }
        }
        catch (std::invalid_argument)
        {
            return false;
        }
    }

    /**
     * findMinElement
     *
     * finds the minimum element present in the array.
     *
     * Parameters:
     *     None
     *
     * Returns:
     *     (double) minimum element present in the array.
     *
     * Throws:
     *     EmptyArrayException: thrown when the array is empty
     */
    double ArrayXD::findMinElement()
    {
        // check if the array is empty
        if (arrayLength == 0)
        {
            throw EmptyArrayException();
        }
        // initialize the current min value as the highest value possible
        double currentMinValue = std::numeric_limits<double>::max();
        for (int i = 0; i < arrayLength; i++)
        {
            if (array[i] < currentMinValue)
            {
                currentMinValue = array[i];
            }
        }
        return currentMinValue;
    }

    /**
     * findMaxElement
     *
     * finds the maximum element present in the array.
     *
     * Parameters:
     *     None
     *
     * Returns:
     *     (double) maximum element present in the array.
     *
     * Throws:
     *     EmptyArrayException: thrown when the array is empty
     */
    double ArrayXD::findMaxELement()
    {
        // check if the array is empty
        if (arrayLength == 0)
        {
            throw EmptyArrayException();
        }
        // initialize the current min value as the lowest value possible
        double currentMaxValue = -std::numeric_limits<double>::max();
        for (int i = 0; i < arrayLength; i++)
        {
            if (array[i] > currentMaxValue)
            {
                currentMaxValue = array[i];
            }
        }
        return currentMaxValue;
    }

    /**
     * findClosedElementLHS
     *
     * finds the closet element in OWL::ArrayXD to the input element by iterating through the array
     * and comparing the (absolute) distance of the value from the inputted value.
     *
     * Parameters:
     *     inputElement: (double) input value
     *
     * Returns:
     *     (double) closest element present in the array.
     *
     * Throws:
     *     None
     */
    double ArrayXD::findClosestElement(double &inputValue)
    {
        // initiate the distance by calculating for the first array element.
        double dist = std::abs(inputValue - array[0]);
        double closestElement = array[0];
        for (size_t i = 1; i < arrayLength; i++)
        {
            double latestDist = std::abs(inputValue - array[i]);
            if (latestDist <= dist)
            {
                dist = latestDist;
                closestElement = array[i];
            }
        }
        return closestElement;
    }

    /**
     * findClosestelementIndex
     *
     * returns the index of the element closest in value to the inputted value.
     *
     * Parameters:
     *     inputVal: (double) input value.
     *
     * Returns:
     *     (size_t) the index of the element cloest in value to the inputted value.
     *
     * Throws:
     *     None
     */
    size_t ArrayXD::findClosestElementIndex(double &inputVal)
    {
        // initiate the distance by calculating for the first array element.
        double dist = std::abs(inputVal - array[0]);
        size_t closestElementIndex = 0;
        for (size_t i = 1; i < arrayLength; i++)
        {
            double latestDist = std::abs(inputVal - array[i]);
            if (latestDist <= dist)
            {
                dist = latestDist;
                closestElementIndex = i;
            }
        }
        return closestElementIndex;
    }

    /**
     * findClosedElementLessThan
     *
     * finds the closet element in OWL::ArrayXD to the (less than) input element by iterating through the array
     * and comparing the distance of the value from the inputted value.
     *
     * Parameters:
     *     inputElement: (double) input value
     *
     * Returns:
     *     (double) closest element present in the array.
     *
     * Throws:
     *     std::invalid_argument: thrown when no element in the array is less than the inputted value.
     */
    double ArrayXD::findCLosestElementLessThan(double &inputVal)
    {
        // initiate dist with a negative number
        double dist = -std::numeric_limits<double>::max();
        double closestElement = NULL;
        for (size_t i = 0; i < arrayLength; i++)
        {
            double latestDist = inputVal - array[i];
            if ((std::abs(latestDist) <= std::abs(dist)) && (latestDist > 0))
            {
                dist = latestDist;
                closestElement = array[i];
            }
        }
        if (dist < 0)
        {
            throw std::invalid_argument("No element is less than the inputted value.");
        }
        return closestElement;
    }

    /**
     * findClosedElementLessThanIndex
     *
     * finds the index of the closet element in OWL::ArrayXD to the (less than) input element by iterating through the array
     * and comparing the distance of the value from the inputted value.
     *
     * Parameters:
     *     inputElement: (double) input value
     *
     * Returns:
     *     (double) index of the closest element whose value is less than inputted array.
     *
     * Throws:
     *     EmptyArrayException: thrown when the array is empty.
     *     std::invalid_argument: thrown when no element in the array is less than the inputted value.
     */
    size_t ArrayXD::findCLosestElementLessThanIndex(double &inputVal)
    {
        // check if the array is empty.
        if (arrayLength == 0)
        {
            throw EmptyArrayException();
        }
        // initiate dist with a negative number
        double dist = -std::numeric_limits<double>::max();
        size_t closestElementIndex = NULL;
        for (size_t i = 0; i < arrayLength; i++)
        {
            double latestDist = inputVal - array[i];
            if ((std::abs(latestDist) <= std::abs(dist)) && (latestDist > 0))
            {
                dist = latestDist;
                closestElementIndex = i;
            }
        }
        // check if there was actually an less than value.
        if (dist < 0)
        {
            throw std::invalid_argument("No element is less than the inputted value.");
        }
        return closestElementIndex;
    }

    /**
     * findClosedElementGreaterThan
     *
     * finds the closet element in OWL::ArrayXD to the (greater than) input element by iterating through the array
     * and comparing the distance of the value from the inputted value.
     *
     * Parameters:
     *     inputElement: (double) input value
     *
     * Returns:
     *     (double) closest element present in the array.
     *
     * Throws:
     *     std::invalid_argument: thrown when no element in the array is greater than the inputted value.
     */
    double ArrayXD::findCLosestElementGreaterThan(double &inputVal)
    {
        // initiate dist with a positive number
        double dist = std::numeric_limits<double>::max();
        double closestElement = NULL;
        for (size_t i = 0; i < arrayLength; i++)
        {
            double latestDist = inputVal - array[i];
            if ((std::abs(latestDist) <= std::abs(dist)) && (latestDist < 0))
            {
                dist = latestDist;
                closestElement = array[i];
            }
        }
        if (dist > 0)
        {
            throw std::invalid_argument("No element is greater than the inputted value.");
        }
        return closestElement;
    }

    /**
     * findClosedElementGreaterThanIndex
     *
     * finds the index of the closet element in OWL::ArrayXD to the (greater than) input element by iterating through the array
     * and comparing the distance of the value from the inputted value.
     *
     * Parameters:
     *     inputElement: (double) input value
     *
     * Returns:
     *     (double) index of the closest element whose value is less than inputted array.
     *
     * Throws:
     *     EmptyArrayException: thrown when the array is empty.
     *     std::invalid_argument: thrown when no element in the array is less than the inputted value.
     */
    // check if the array is empty.
    size_t ArrayXD::findCLosestElementGreaterThanIndex(double &inputVal)
    {
        if (arrayLength == 0)
        {
            throw EmptyArrayException();
        }
        // initiate dist with a negative number
        double dist = std::numeric_limits<double>::max();
        size_t closestElementIndex = NULL;
        for (size_t i = 0; i < arrayLength; i++)
        {
            double latestDist = inputVal - array[i];
            if ((std::abs(latestDist) <= std::abs(dist)) && (latestDist < 0))
            {
                dist = latestDist;
                closestElementIndex = i;
            }
        }
        // check if there was actually an less than value.
        if (dist > 0)
        {
            throw std::invalid_argument("No element is greater than the inputted value.");
        }
        return closestElementIndex;
    }

    /**
     * checkEmpty array
     *
     * checks if the OWL::ArrayXD is empty.
     *
     * Parameters:
     *     None
     *
     * Return:
     *     bool value is true if the array is empty, false otherwise.
     *
     * Throws:
     *     std_invalid_argument: thrown when the array is empty.
     */
    bool ArrayXD::checkEmptyArray()
    {
        bool flag = false;
        if (arrayLength == 0)
        {
            flag = true;
            throw std::invalid_argument("Empty array.");
        }
        return flag;
    }

    /**
     * add
     *
     * Element by Element addition of OWL arrays
     *
     * Parameters:
     *    otherArray: OWL array type
     *
     * Returns:
     *    OWL Array object with added arrays
     *
     * Throws:
     *     invalid_argument: the lengths of the arrays have to match.
     */
    ArrayXD ArrayXD::add(ArrayXD &otherArray)
    {

        // Check if the size of the otherArray is equal to that of the array in question (below).
        if (otherArray.getArrayLength() != arrayLength)
        {
            throw std::invalid_argument("the sizes of the arrays have to match.");
        }

        // element by element addition.
        std::vector<double> resultVec;
        ArrayXD resultArray;
        for (int index = 0; index < arrayLength; index++)
        {
            resultVec.push_back(array[index] + otherArray.array[index]);
        }
        resultArray.setArray(resultVec);
        return resultArray;
    }

    /**
     * subtract
     *
     * Element by element subtraction
     *
     * Parameters:
     *     inputArray: another ArrayXD array to subtract from
     *
     * Return:
     *     ouputArray: resultant ArrayXD object.
     *
     * Throws:
     *     OWL::SizeMismatchException: thrown when the length of the otherArray doesnot match with the instance's length.
     */
    ArrayXD ArrayXD::subtract(ArrayXD &otherArray)
    {
        // check if the array lengths are the same
        try
        {
            bool flag = compareArrayLength(otherArray);
            // initialize std::vector
            std::vector<double> interVec;
            for (size_t i = 0; i < arrayLength; i++)
            {
                interVec.push_back(array[i] - otherArray[i]);
            }
            // intialize ArrayXD and set it to the vector
            ArrayXD resultArray = ArrayXD(interVec);
            return resultArray;
        }
        catch (std::invalid_argument &e)
        {
            std::cout << e.what() << std::endl;
            ArrayXD resultArray = ArrayXD();
            return resultArray;
        }
    }

    /**
     * muliply
     *
     * muliplication of OWL::ArrayXD with a scalar value
     *
     * Parameters:
     *     scalarValue: double scalar value
     *
     * Return:
     *     OWL::ArrayXD result after sclar multiplication
     *
     * Throws:
     *     None
     */
    ArrayXD ArrayXD::multiply(const double &scalarValue)
    {
        for (size_t i = 0; i < arrayLength; i++)
        {
            array[i] = scalarValue * array[i];
        }
        ArrayXD resultArray(array);
        return resultArray;
    }

    /**
     * muliply
     *
     * muliplication of OWL::ArrayXD with another OWL::ArrayXD via element-by-element multiplication.
     *
     * Parameters:
     *     otherArray: OWL::ArrayXD
     *
     * Return:
     *     OWL::ArrayXD result after element-by-element multiplication.
     *
     * Throws:
     *     None
     */
    ArrayXD ArrayXD::multiply(ArrayXD &otherArray)
    {
        try
        {
            bool flag = compareArrayLength(otherArray);
            for (size_t i = 0; i < arrayLength; i++)
            {
                array[i] = otherArray[i] * array[i];
            }
        }
        catch (std::invalid_argument &exception)
        {
            std::cout << exception.what() << std::endl;
        }
        ArrayXD resultArray(array);
        return resultArray;
    }

    /**
     * operator overload for indexing
     *
     * Parameters:
     *     index: size_t representing the desired index.
     *
     * Return:
     *     double value of the OWL::ArrayXD corresponding to the desired index.
     *
     * Throws:
     *     invalid_argument: thrown when the inputted index exceeds the array length.
     */
    double &ArrayXD::operator[](size_t index)
    {
        if (index > (arrayLength - 1))
        {
            throw std::invalid_argument("index exceeds the maximum array length.");
        }
        return array[index];
    }

    /**
     * operator overload for addition with another double
     *
     * Parameters:
     *     otherDouble: scalar of double type.
     *
     * Return:
     *     OWL::ArrayXD
     *
     * Throw:
     *     None
     */
    ArrayXD ArrayXD::operator+(double &scalar)
    {
        std::vector<double> interVec;
        for (size_t i = 0; i < arrayLength; i++)
        {
            interVec.push_back(array[i] + scalar);
        }
        ArrayXD resultArray(interVec);
        return resultArray;
    }

    /**
     * operator overload for addition with another OWL::Array
     *
     * Parameters:
     *     otherArray: OWL::ArrayXD
     *
     * Return:
     *     OWL::ArrayXD corresponding to element-by-element additions.
     *
     * Throws:
     *     None
     */
    ArrayXD ArrayXD::operator+(ArrayXD &otherArray)
    {
        try
        {
            ArrayXD resultArray = add(otherArray);
            return resultArray;
        }
        catch (const std::exception &exception)
        {
            std::cout << exception.what() << std::endl;
            ArrayXD NULLArray;
            return NULLArray;
        }
    }

    /**
     * operator overload for subtraction.
     *
     * Parameters:
     *     otherArray: OWL::ArrayXD
     *
     * Return:
     *     OWL::ArrayXD corresponding to element-by-element subtractions.
     *
     * Throws:
     *     std::invalid_argument: thrown when the sizes do not match up.
     */
    ArrayXD ArrayXD::operator-(ArrayXD &otherArray)
    {
        try
        {
            ArrayXD resultArray = subtract(otherArray);
            return resultArray;
        }
        catch (const std::exception &exception)
        {
            std::cout << exception.what() << std::endl;
            ArrayXD NULLArray = ArrayXD();
            return NULLArray;
        }
    }

    /**
     * operator overload for scalar multiplication
     *
     * Parameters:
     *     scalarValue: double scalar value.
     *
     * Return:
     *     double value of the OWL::ArrayXD after scalar multiplication.
     *
     * Throws:
     *     None
     */
    ArrayXD ArrayXD::operator*(const double scalarValue)
    {
        ArrayXD resultVec = multiply(scalarValue);
        return resultVec;
    }

    /**
     * operator overload for element-by-element multiplication
     *
     * Parameters:
     *     otherArray: other OWL::ArrayXD
     *
     * Return:
     *     double value of the OWL::ArrayXD after element-by-element multiplication.
     *
     * Throws:
     *     std::invalid_argument: if arrays lengths do not match.
     */
    ArrayXD ArrayXD::operator*(ArrayXD &otherArray)
    {
        ArrayXD resultVec = multiply(otherArray);
        return resultVec;
    }

    /**
     * -----------------------------------------------------------------------------------------
     * The functions below pertains to creating a custom OWL::ArrayXD
     * -----------------------------------------------------------------------------------------
     */

    ///@{
    /**
     * Zeros
     *
     * Creates an OWL array with all elements having zero value.
     *
     * Parameters:
     *     len: an int representing length of the array. Default value is set to 50.
     *
     * Throws:
     *     None
     */
    ArrayXD Zeros(int len)
    {
        double currentDouble = 0.0;
        std::vector<double> interVec;
        for (int i = 0; i < len; i++)
        {
            interVec.push_back(currentDouble);
        }
        ArrayXD resultArray(interVec);
        return resultArray;
    }

    /**
     * Ones
     *
     * Creates an OWL array with all elements having one value.
     *
     * Parameters:
     *     len: an int representing length of the array. Default value is set to 50.
     *
     * Throws:
     *     None
     */
    ArrayXD Ones(int len)
    {
        double currentDouble = 1.0;
        std::vector<double> interVec;
        for (int i = 0; i < len; i++)
        {
            interVec.push_back(currentDouble);
        }
        ArrayXD resultArray(interVec);
        return resultArray;
    }

    /**
     * aRange
     *
     * create an array with a range.
     *
     * Paramaters:
     *     start: int representing the begin range.
     *     end: int representing the end range.
     *
     * Return:
     *     OWL::ArrayXD
     *
     * Throws:
     *     std::invalid_argument: thrown when the begin is equal to to greater than the end input parameter.
     */
    ArrayXD aRange(double start, double end, double dx)
    {
        // throw exception if start is equal to greater than end.
        if (start >= end)
        {
            throw std::invalid_argument("start equal to or greater than end.");
        }
        std::vector<double> interVec;
        double current_double = start;
        while (current_double < end)
        {
            interVec.push_back(current_double);
            current_double += dx;
        }
        return ArrayXD(interVec);
    }

    /**
     * LinSpaced
     *
     * Creates an OWL array with linearly spaced elements.
     *
     * Parameters:
     *     startDouble: a double value representing first element.
     *     endDouble: a double value representing the last element.
     *     length: an int representing length of the array. Default value is set to 50.
     *
     * Throws:
     *     Exception: startDouble should be less than endDouble
     */
    ArrayXD LinSpaced(double startDouble, double endDouble, int length)
    {
        if (startDouble > endDouble)
        {
            throw std::invalid_argument("startDouble value should be less than endDouble.");
        }
        double difference = (endDouble - startDouble) / (length - 1);
        double currentDouble = startDouble;
        std::vector<double> interVec;
        for (int i = 0; i < length; i++)
        {
            interVec.push_back(currentDouble);
            currentDouble += difference;
        }
        ArrayXD resultArray(interVec);
        return resultArray;
    }
    ///@}

    /*
     * ----------------------------------------------------------------------------------------------
     * The functions below pertains to performing element-by-element math operatons on OWL::ArrayXD
     * -----------------------------------------------------------------------------------------------
     */

    /**
     * abs
     *
     * returns a OWL::ArrayXD with absolute element values
     *
     * Parameters:
     *     inputArray: (OWL::ArrayXD)
     *
     * Returns:
     *     (OWL::ArrayXD)
     *
     * Throws:
     *     None
     */
    ArrayXD abs(ArrayXD &inputArray)
    {
        std::vector<double> interVec;
        for (size_t i = 0; i < inputArray.getArrayLength(); i++)
        {
            interVec.push_back(std::abs(inputArray[i]));
        }
        return OWL::ArrayXD(interVec);
    }

    /**
     * sin
     *
     * Element-by-element sin operation on OWL::ArrayXD.
     *
     * Parameters:
     *     OWL::ArrayXD containing the angles in radians.
     *
     * Return:
     *     OWL::ArrayXD result from the element-by-element sin operation.
     *
     * Throw:
     *     std_invalid_argument: thrown when the array is empty.
     */
    ArrayXD sin(ArrayXD &inputOWLArray)
    {
        // handle empty array using try/catch
        try
        {
            bool flag = inputOWLArray.checkEmptyArray();
            // element-by-element operation
            std::vector<double> interVec = inputOWLArray.getArray();
            for (size_t i = 0; i < inputOWLArray.getArrayLength(); i++)
            {
                interVec[i] = std::sin(interVec[i]);
            }
            ArrayXD resultArray(interVec);
            return resultArray;
        }
        catch (std::invalid_argument &e)
        {
            // incase of empty array, print exception and return an empty array
            std::cout << e.what() << std::endl;
            std::cout << "Attempted operation on an empty array." << std::endl;
            ArrayXD resultArray;
            return resultArray;
        }
    }

    /**
     * cos
     *
     * Element-by-element cos operation on OWL::ArrayXD.
     *
     * Parameters:
     *     OWL::ArrayXD containing the angles in radians.
     *
     * Return:
     *     OWL::ArrayXD result from the element-by-element cos operation.
     *
     * Throw:
     *     std_invalid_argument: thrown when the array is empty.
     */
    ArrayXD cos(ArrayXD &inputOWLArray)
    {
        // handle empty array using try/catch
        try
        {
            bool flag = inputOWLArray.checkEmptyArray();
            // element-by-element operation
            std::vector<double> interVec = inputOWLArray.getArray();
            for (size_t i = 0; i < inputOWLArray.getArrayLength(); i++)
            {
                interVec[i] = std::cos(interVec[i]);
            }
            ArrayXD resultArray(interVec);
            return resultArray;
        }
        catch (std::invalid_argument &e)
        {
            // incase of empty array, print exception and return an empty array
            std::cout << e.what() << std::endl;
            std::cout << "Attempted operation on an empty array." << std::endl;
            ArrayXD resultArray;
            return resultArray;
        }
    }

    /**
     * tan
     *
     * Element-by-element tan operation on OWL::ArrayXD.
     *
     * Parameters:
     *     OWL::ArrayXD containing the angles in radians.
     *
     * Return:
     *     OWL::ArrayXD result from the element-by-element tan operation.
     *
     * Throw:
     *     std_invalid_argument: thrown when the array is empty.
     */
    ArrayXD tan(ArrayXD &inputOWLArray)
    {
        // handle empty array using try/catch
        try
        {
            bool flag = inputOWLArray.checkEmptyArray();
            // element-by-element operation
            std::vector<double> interVec = inputOWLArray.getArray();
            for (size_t i = 0; i < inputOWLArray.getArrayLength(); i++)
            {
                interVec[i] = std::tan(interVec[i]);
            }
            ArrayXD resultArray(interVec);
            return resultArray;
        }
        catch (std::invalid_argument &e)
        {
            // incase of empty array, print exception and return an empty array
            std::cout << e.what() << std::endl;
            std::cout << "Attempted operation on an empty array." << std::endl;
            ArrayXD resultArray;
            return resultArray;
        }
    }

    /**
     * asin
     *
     * Element-by-element asin operation on OWL::ArrayXD.
     *
     * Parameters:
     *     OWL::ArrayXD containing the angles in radians.
     *
     * Return:
     *     OWL::ArrayXD result from the element-by-element asin operation.
     *
     * Throw:
     *     std_invalid_argument: thrown when the array is empty.
     */
    ArrayXD asin(ArrayXD &inputOWLArray)
    {
        // handle empty array using try/catch
        try
        {
            bool flag = inputOWLArray.checkEmptyArray();
            // element-by-element operation
            std::vector<double> interVec = inputOWLArray.getArray();
            for (size_t i = 0; i < inputOWLArray.getArrayLength(); i++)
            {
                interVec[i] = std::asin(interVec[i]);
            }
            ArrayXD resultArray(interVec);
            return resultArray;
        }
        catch (std::invalid_argument &e)
        {
            // incase of empty array, print exception and return an empty array
            std::cout << e.what() << std::endl;
            std::cout << "Attempted operation on an empty array." << std::endl;
            ArrayXD resultArray;
            return resultArray;
        }
    }

    /**
     * acos
     *
     * Element-by-element acos operation on OWL::ArrayXD.
     *
     * Parameters:
     *     OWL::ArrayXD containing the angles in radians.
     *
     * Return:
     *     OWL::ArrayXD result from the element-by-element acos operation.
     *
     * Throw:
     *     std_invalid_argument: thrown when the array is empty.
     */
    ArrayXD acos(ArrayXD &inputOWLArray)
    {
        // handle empty array using try/catch
        try
        {
            bool flag = inputOWLArray.checkEmptyArray();
            // element-by-element operation
            std::vector<double> interVec = inputOWLArray.getArray();
            for (size_t i = 0; i < inputOWLArray.getArrayLength(); i++)
            {
                interVec[i] = std::acos(interVec[i]);
            }
            ArrayXD resultArray(interVec);
            return resultArray;
        }
        catch (std::invalid_argument &e)
        {
            // incase of empty array, print exception and return an empty array
            std::cout << e.what() << std::endl;
            std::cout << "Attempted operation on an empty array." << std::endl;
            ArrayXD resultArray;
            return resultArray;
        }
    }

    /**
     * atan
     *
     * Element-by-element atan operation on OWL::ArrayXD.
     *
     * Parameters:
     *     OWL::ArrayXD containing the angles in radians.
     *
     * Return:
     *     OWL::ArrayXD result from the element-by-element atan operation.
     *
     * Throw:
     *     std_invalid_argument: thrown when the array is empty.
     */
    ArrayXD atan(ArrayXD &inputOWLArray)
    {
        // handle empty array using try/catch
        try
        {
            bool flag = inputOWLArray.checkEmptyArray();
            // element-by-element operation
            std::vector<double> interVec = inputOWLArray.getArray();
            for (size_t i = 0; i < inputOWLArray.getArrayLength(); i++)
            {
                interVec[i] = std::atan(interVec[i]);
            }
            ArrayXD resultArray(interVec);
            return resultArray;
        }
        catch (std::invalid_argument &e)
        {
            // incase of empty array, print exception and return an empty array
            std::cout << e.what() << std::endl;
            std::cout << "Attempted operation on an empty array." << std::endl;
            ArrayXD resultArray;
            return resultArray;
        }
    }

    /**
     * exp
     *
     * Element-by-element exp operation on OWL::ArrayXD.
     *
     * Parameters:
     *     OWL::ArrayXD
     *
     * Return:
     *     OWL::ArrayXD result from the element-by-element exponential operation.
     *
     * Throw:
     *     std_invalid_argument: thrown when the array is empty.
     */
    ArrayXD exp(ArrayXD &inputOWLArray)
    {
        // handle empty array using try/catch
        try
        {
            bool flag = inputOWLArray.checkEmptyArray();
            // element-by-element operation
            std::vector<double> interVec = inputOWLArray.getArray();
            for (size_t i = 0; i < inputOWLArray.getArrayLength(); i++)
            {
                interVec[i] = std::exp(interVec[i]);
            }
            ArrayXD resultArray(interVec);
            return resultArray;
        }
        catch (std::invalid_argument &e)
        {
            // incase of empty array, print exception and return an empty array
            std::cout << e.what() << std::endl;
            std::cout << "Attempted operation on an empty array." << std::endl;
            ArrayXD resultArray;
            return resultArray;
        }
    }

    /**
     * log10
     *
     * Element-by-element log10 operation on OWL::ArrayXD.
     *
     * Parameters:
     *     OWL::ArrayXD
     *
     * Return:
     *     OWL::ArrayXD result from the element-by-element log10 operation.
     *
     * Throw:
     *     std_invalid_argument: thrown when the array is empty.
     */
    ArrayXD log10(ArrayXD &inputOWLArray)
    {
        // handle empty array using try/catch
        try
        {
            bool flag = inputOWLArray.checkEmptyArray();
            // element-by-element operation
            std::vector<double> interVec = inputOWLArray.getArray();
            for (size_t i = 0; i < inputOWLArray.getArrayLength(); i++)
            {
                // check for any entry with 0
                if (interVec[i] == 0)
                {
                    throw std::invalid_argument("cannot find log10 for a 0 value.");
                }
                interVec[i] = std::log10(interVec[i]);
            }
            ArrayXD resultArray(interVec);
            return resultArray;
        }
        catch (std::invalid_argument &e)
        {
            // incase of empty array, print exception and return an empty array
            std::cout << e.what() << std::endl;
            std::cout << "Attempted operation on an empty array." << std::endl;
            ArrayXD resultArray;
            return resultArray;
        }
    }

    /**
     * ln
     *
     * Element-by-element ln operation on OWL::ArrayXD.
     *
     * Parameters:
     *     OWL::ArrayXD
     *
     * Return:
     *     OWL::ArrayXD result from the element-by-element ln operation.
     *
     * Throw:
     *     std_invalid_argument: thrown when the array is empty.
     */
    ArrayXD ln(ArrayXD &inputOWLArray)
    {
        // handle empty array using try/catch
        try
        {
            bool flag = inputOWLArray.checkEmptyArray();
            // element-by-element operation
            std::vector<double> interVec = inputOWLArray.getArray();
            for (size_t i = 0; i < inputOWLArray.getArrayLength(); i++)
            {
                // check for any entry with 0
                if (interVec[i] == 0)
                {
                    throw std::invalid_argument("cannot find log10 for a 0 value.");
                }
                interVec[i] = std::log(interVec[i]);
            }
            ArrayXD resultArray(interVec);
            return resultArray;
        }
        catch (std::invalid_argument &e)
        {
            // incase of empty array, print exception and return an empty array
            std::cout << e.what() << std::endl;
            std::cout << "Attempted operation on an empty array." << std::endl;
            ArrayXD resultArray;
            return resultArray;
        }
    }

    /**
     * append
     *
     * Appends two OWL::ArrayXD arrays.
     *
     * Parameters:
     *   OWL::ArrayXD
     *   OWL::ArrayXD
     *
     * Returns:
     *   OWL::ArrayXD an array from appending the input arrays
     */
    ArrayXD append(ArrayXD &array1, ArrayXD &array2)
    {
        std::vector<double> res_array = array1.getArray();
        for (int i = 0; i < array2.size(); i++)
        {
            res_array.push_back(array2.getArray()[i]);
        }
        return ArrayXD(res_array);
    }

    /*
     * ------------------------------------------------------------------
     * methods for MatrixXD class below
     * -------------------------------------------------------------------
     */

    /**
     * MatrixXD
     *
     * Default constructor. Creates a empty matrix. It is the only time when the std::vector can be empty.
     *
     * Parameters:
     *     None
     *
     * Return:
     *     None
     *
     * Throws:
     *     None
     */
    MatrixXD::MatrixXD()
    {
        // std::vector<double> vecTemp;
        // vecTemp.push_back(0);
        // ArrayXD row = ArrayXD(vecTemp);
        // std::vector<ArrayXD> matrixTemp;
        // matrixTemp.push_back(row);
        // elements = matrixTemp;
        //// set row size
        // m = findRowSize();
        //// set col size
        // n = findColSize();
        m = 0;
        n = 0;
    }

    /**
     * MatrixXD
     *
     * Overload contructor.
     *
     * Parameters:
     *     inputElements: (std::vector<ArrayXD>) input Elements
     *
     * Return:
     *     None
     *
     * Throws:
     *     None
     */
    MatrixXD::MatrixXD(std::vector<ArrayXD> inputElements) : elements(inputElements), m(findRowSize()),
                                                             n(findColSize()) {}

    /**
     * MatrixXD
     *
     * Overload contructor that returns a zero matrix based on the required size.
     *
     * Parameters:
     *     rowSize: (int) row size
     *     colSize: (int) col size
     *
     * Return:
     *     None
     *
     * Throws:
     *     None
     */
    MatrixXD::MatrixXD(const int rowSize, const int colSize)
    {
        // create a row until colSize is met
        ArrayXD row = ArrayXD();
        for (int i = 0; i < colSize; i++)
        {
            row << 0;
        }
        //
        // initiate a matrix
        MatrixXD resMatrix = MatrixXD();
        // add rows to the matrix until row size is met
        for (int i = 0; i < rowSize; i++)
        {
            resMatrix << row;
        }
        elements = resMatrix.getElements();
        m = findRowSize();
        n = findColSize();
    }

    /**
     * findRowSize
     *
     * finds the row size of the matrix
     *
     * Parameters:
     *     None
     *
     * Returns:
     *     (int) row size
     *
     * Throws:
     *     None
     */
    int MatrixXD::findRowSize()
    {
        bool emptyArrays = checkEmptyArrays();
        if (emptyArrays)
        {
            return 0;
        }
        return (int)elements.size();
    }

    /**
     * findColSize
     *
     * finds the column size of the matrix
     *
     * Parameters:
     *     None
     *
     * Return:
     *     (int) column size
     *
     * Throws:
     *     DiffArraySizeException: thrown when the element size are different in a same matrix
     */
    int MatrixXD::findColSize()
    {
        bool emptyArrays = checkEmptyArrays();
        if (emptyArrays)
        {
            return 0;
        }
        return (int)elements[0].size();
    }

    /**
     * checkEmptyArrays
     *
     * checks to see if the arrays in the matrix are empty. It iterates over the sizes of all the arrays.
     *
     * Parameters:
     *     None
     *
     * Returns:
     *     (bool) true if the arrays are empty
     *
     * Throws:
     *    DiffArrayLengthsException: thrown when the arrays have different sizes.
     */
    bool MatrixXD::checkEmptyArrays()
    {
        // check for empty element with no arrays
        if (elements.empty())
        {
            throw std::invalid_argument("input vector had no OWL::ArrayXD inside of it.");
        }
        bool flag = false;
        size_t arrayLength = elements[0].getArrayLength();
        for (size_t i = 1; i < elements.size(); i++)
        {
            if (elements[i].getArrayLength() != arrayLength)
            {
                throw DiffArrayLengthsException();
            }
            arrayLength = elements[i].getArrayLength();
        }
        if (arrayLength == 0)
        {
            flag = true;
        }
        return flag;
    }

    /*
     * getCol
     *
     * returns an OWL::ArrayXD containing the values from a column in the matrix.
     *
     * Parameters:
     *     inputMatrix: (OWL::MatrixXD) input matrix
     *     colIndex: (int) column index
     *
     * Return:
     *     (OWL::ArrayXD) array
     *
     * Throws:
     *     None
     */
    OWL::ArrayXD MatrixXD::getCol(int colIndex)
    {
        ArrayXD resArray = ArrayXD();
        for (int rowIndex = 0; rowIndex < m; rowIndex++)
        {
            resArray << elements[rowIndex][colIndex];
        }
        return resArray;
    }

    /**
     * Operator overload for addition to have matrix addition
     *
     * Parameters:
     *     inputMatrix: (OWL::MatrixXD) inputMatrix
     *
     * Return:
     *     (OWL::MatrixXD) result matrix
     *
     * Throws:
     *     std::invalid_argument: thrown if there is a size mismatch
     */
    MatrixXD MatrixXD::operator+(MatrixXD &inputMatrix)
    {
        // check for the sizes
        if (!compareSize(inputMatrix))
        {
            throw std::invalid_argument("Size mismatch");
        }
        MatrixXD resMatrix;
        for (int rowIndex = 0; rowIndex < m; rowIndex++)
        {
            resMatrix << elements[rowIndex] + inputMatrix.getElements()[rowIndex];
        }
        return resMatrix;
    }

    /**
     * Operator overload for addition to have matrix subtraction
     *
     * Parameters:
     *     inputMatrix: (OWL::MatrixXD) inputMatrix
     *
     * Return:
     *     (OWL::MatrixXD) result matrix
     *
     * Throws:
     *     std::invalid_argument: thrown if there is a size mismatch
     */
    MatrixXD MatrixXD::operator-(MatrixXD &inputMatrix)
    {
        // check for the sizes
        if (!compareSize(inputMatrix))
        {
            throw std::invalid_argument("Size mismatch");
        }
        MatrixXD resMatrix;
        for (int rowIndex = 0; rowIndex < m; rowIndex++)
        {
            resMatrix << elements[rowIndex] - inputMatrix.getElements()[rowIndex];
        }
        return resMatrix;
    }

    MatrixXD MatrixXD::operator*(MatrixXD &inputMatrix)
    {
        // check if the col size of the current matrix matches the row size of the input matrix
        if (n != inputMatrix.getRowSize())
        {
            throw std::invalid_argument("Sizes of the matrix not suitable for matrix multiplication.");
        }
        MatrixXD resMatrix = MatrixXD(m, inputMatrix.getColSize());
        for (int rowIndex = 0; rowIndex < m; rowIndex++)
        {
            for (int colIndex = 0; colIndex < inputMatrix.getColSize(); colIndex++)
            {
                // create an array for col of input array
                ArrayXD colArray = inputMatrix.getCol(colIndex);
                // multiply the row of the current and col of the other and sum them
                ArrayXD multArray = elements[rowIndex] * colArray;
                // update the entries of the result matrix
                resMatrix[rowIndex][colIndex] = multArray.sum();
            }
        }
        return resMatrix;
    }

    /**
     * compareSize
     *
     * compares the row and col sizes with another matrix.
     *
     * Parameters:
     *     inputMatrix: (OWL::MatrixXD) input matrix
     *
     * Return:
     *     (bool) true if the row and col sizes match
     *
     * Throws:
     *     None
     */
    bool MatrixXD::compareSize(MatrixXD &inputMatrix)
    {
        bool flag = false;
        if ((m == inputMatrix.getRowSize()) && (n == inputMatrix.getColSize()))
        {
            flag = true;
        }
        return flag;
    }

    /**
     * T
     *
     * Tranpose of the matrix
     *
     * Parameters:
     *     None
     *
     * Return:
     *     None
     *
     * Throws:
     *     None
     */
    void MatrixXD::T()
    {
        MatrixXD resMatrix = Zeros(n, m);
        for (int i = 0; i < n; i++)
        {
            for (int j = 0; j < m; j++)
            {
                resMatrix[i][j] = elements[j][i];
            }
        }
        elements = resMatrix.getElements();
        int nTemp = n;
        m = n;
        n = m;
    }

    /**
     * submatrix
     *
     * finds the submatrix
     *
     * Parameters:
     *     inputRowIndex: (double) input row index to exclude
     *     inputColIndex: (double) input col index to exclude
     *
     * Return:
     *    (OWL::MatrixXD) sub matrix
     *
     * Throws:
     *     std::invalid_argument: thrown when the input index exceeds matrix size.
     */
    MatrixXD MatrixXD::submatrix(int inputRowIndex, int inputColIndex)
    {
        if ((inputRowIndex > (m - 1)) || (inputColIndex > (n - 1)))
        {
            throw std::invalid_argument("input index exceeds the matrix size.");
        }
        MatrixXD resMatrix = MatrixXD();
        for (int rowIndex = 0; rowIndex < n; rowIndex++)
        {
            if (rowIndex == inputRowIndex)
                continue;
            else
            {
                ArrayXD row = ArrayXD();
                for (int colIndex = 0; colIndex < m; colIndex++)
                {
                    if (colIndex == inputColIndex)
                        continue;
                    row << elements[rowIndex][colIndex];
                }
                resMatrix << row;
            }
        }
        return resMatrix;
    }

    /**
     * det
     *
     * finds the determinant of the matrix.
     *
     * Parameters:
     *     None
     *
     * Return:
     *     (double) determinant
     *
     * Throws:
     *     std::invalid_argument: thrown when the matrix is not square.
     */
    double MatrixXD::det()
    {
        // check if the matrix is square
        if (!isSquare())
        {
            std::invalid_argument("Cannot find the detetminant of a non-square matrix.");
        }
        double detVal = 0;
        if (n == 1)
        {
            return elements[0][0];
        }
        else if (n == 2)
        {
            return elements[0][0] * elements[1][1] - elements[0][1] * elements[1][0];
        }
        else
        {
            for (int firstRowIndex = 0; firstRowIndex < m; firstRowIndex++)
            {
                MatrixXD subMat = submatrix(0, firstRowIndex);
                detVal += std::pow(-1, firstRowIndex) * elements[0][firstRowIndex] * subMat.det();
            }
            return detVal;
        }
    }

    /*
     * The functions below pertains to creating a custom OWL::MatrixXD
     */
    MatrixXD Zeros(int rowLen, int colLen)
    {
        MatrixXD resMatrix = MatrixXD();
        for (int i = 0; i < rowLen; i++)
        {
            ArrayXD row = ArrayXD();
            for (int j = 0; j < colLen; j++)
            {
                row << 0;
            }
            resMatrix << row;
        }
        return resMatrix;
    }

    MatrixXD Ones(int rowLen, int colLen)
    {
        MatrixXD resMatrix = MatrixXD();
        for (int i = 0; i < rowLen; i++)
        {
            ArrayXD row = ArrayXD();
            for (int j = 0; j < colLen; j++)
            {
                row << 1;
            }
            resMatrix << row;
        }
        return resMatrix;
    }

    MatrixXD Diag(int len)
    {
        MatrixXD resMatrix = MatrixXD();
        for (int i = 0; i < len; i++)
        {
            ArrayXD row = ArrayXD();
            for (int j = 0; j < len; j++)
            {
                if (j == i)
                    row << 1;
                else
                    row << 0;
            }
            resMatrix << row;
        }
        return resMatrix;
    }
}

OWL::ArrayXD operator+(double lhsScalar, OWL::ArrayXD rhsArray)
{
    std::vector<double> interVec;
    for (size_t i = 0; i < rhsArray.getArrayLength(); i++)
    {
        interVec.push_back(rhsArray[i] + lhsScalar);
    }
    OWL::ArrayXD resultArray = OWL::ArrayXD(interVec);
    return resultArray;
}

OWL::ArrayXD operator*(double lhsScalar, OWL::ArrayXD rhsArray)
{
    // initiate a std::vector
    std::vector<double> interVec;
    // element-by-element scalar multiplication
    for (size_t i = 0; i < rhsArray.getArrayLength(); i++)
    {
        interVec.push_back(lhsScalar * rhsArray[i]);
    }
    // Create a new OWL::ArrayXD instance and return it
    OWL::ArrayXD resultVec = OWL::ArrayXD(interVec);
    return resultVec;
}

namespace Newton
{
    namespace interp
    {
        const char *ExceedInterpolateLimit::what()
        {
            return "Interpolation Limits Exceeded.";
        }

        double slope(double &y2, double &y1, double &x2, double &x1)
        {
            return (y2 - y1) / (x2 - x1);
        }

        std::function<double(double)> line(double &slope, double &x, double &y)
        {
            double y_intercept = y - (slope * x);
            return [y_intercept, slope](double x_value)
            { return slope * x_value + y_intercept; };
        }

        double interp(OWL::ArrayXD xArray, OWL::ArrayXD yArray, double x)
        {
            // check if the xvalue is within the desired interpolation region.
            if ((x > xArray.findMaxELement()) || (x < xArray.findMinElement()))
            {
                throw ExceedInterpolateLimit();
            }
            // find the interpolating interval and the y values
            double x1 = xArray.findCLosestElementLessThan(x), x2 = xArray.findCLosestElementGreaterThan(x);
            size_t x1Index = xArray.findCLosestElementLessThanIndex(x), x2Index = xArray.findCLosestElementGreaterThanIndex(x);
            double y1 = yArray[x1Index], y2 = yArray[x2Index];
            // find the slope and the y-intercept
            double s = slope(y2, y1, x2, x1);
            std::function<double(double)> lineEquation = line(s, x1, y1);
            return lineEquation(x);
        }

        std::function<double(double)> interpFunc(OWL::ArrayXD xArray, OWL::ArrayXD yArray)
        {
            return [xArray, yArray](double x)
            { return interp(xArray, yArray, x); };
        }

        double linear_interpolation(double x, std::vector<double> vec_x, std::vector<double> vec_y)
        {
            if (vec_x.size() != vec_y.size())
                throw std::invalid_argument("vector x and y need to be of same size.");

            // combine the two vectors into one
            std::vector<std::pair<double, double>> combined_vec;
            for (int i = 0; i < vec_x.size(); i++)
            {
                combined_vec.push_back(std::make_pair(vec_x[i], vec_y[i]));
            }

            // sort the combined vector based on the first element of the pair
            std::sort(combined_vec.begin(), combined_vec.end(), [&](auto a, auto b)
                      { return a.first < b.first; });

            // unzip the combined vector
            std::vector<double> sorted_x, sorted_y;
            for (int i = 0; i < vec_x.size(); i++)
            {
                sorted_x.push_back(combined_vec[i].first);
                sorted_y.push_back(combined_vec[i].second);
            }

            // find the lower and upper bound index for the elements with value just lower and higher than x
            auto i = lower_bound(sorted_x.begin(), sorted_x.end(), x);
            auto k = i - sorted_x.begin(); // upper element
            if (k == 0)
                return sorted_y[0]; // lower bound extrapolation
            auto l = k ? k - 1 : 1; // lower element
            if (i == sorted_x.end())
                return sorted_y[sorted_y.size() - 1]; // extrapolate to the y value at the last element

            // linear regression
            double result = sorted_y[l] + (x - sorted_x[l]) * (sorted_y[k] - sorted_y[l]) / (sorted_x[k] - sorted_x[l]);

            return result;
        }

        long double linear_interpolation(long double x, std::vector<long double> vec_x, std::vector<long double> vec_y)
        {
            if (vec_x.size() != vec_y.size())
                throw std::invalid_argument("vector x and y need to be of same size.");

            // combine the two vectors into one
            std::vector<std::pair<long double, long double>> combined_vec;
            for (int i = 0; i < vec_x.size(); i++)
            {
                combined_vec.push_back(std::make_pair(vec_x[i], vec_y[i]));
            }

            // sort the combined vector based on the first element of the pair
            std::sort(combined_vec.begin(), combined_vec.end(), [&](auto a, auto b)
                      { return a.first < b.first; });

            // unzip the combined vector
            std::vector<long double> sorted_x, sorted_y;
            for (int i = 0; i < vec_x.size(); i++)
            {
                sorted_x.push_back(combined_vec[i].first);
                sorted_y.push_back(combined_vec[i].second);
            }

            // find the lower and upper bound index for the elements with value just lower and higher than x
            auto i = lower_bound(sorted_x.begin(), sorted_x.end(), x);
            int k = i - sorted_x.begin(); // upper element
            if (k == 0)
                return sorted_y[0]; // lower bound extrapolation
            int l = k ? k - 1 : 1;  // lower element
            if (i == sorted_x.end())
                return sorted_y[sorted_y.size() - 1]; // extrapolate to the y value at the last element

            // linear regression
            long double result = sorted_y[l] + (x - sorted_x[l]) * (sorted_y[k] - sorted_y[l]) / (sorted_x[k] - sorted_x[l]);

            return result;
        }

        std::vector<double> linear_interpolation(std::vector<double> target_vec_x, std::vector<double> vec_x, std::vector<double> vec_y)
        {
            std::vector<double> result_vector;
            for (int i = 0; i < target_vec_x.size(); i++)
            {
                result_vector.push_back(linear_interpolation(target_vec_x[i], vec_x, vec_y));
            }
            return result_vector;
        }

        std::vector<long double> linear_interpolation(std::vector<long double> target_vec_x, std::vector<long double> vec_x, std::vector<long double> vec_y)
        {
            std::vector<long double> result_vector;
            for (int i = 0; i < target_vec_x.size(); i++)
            {
                result_vector.push_back(linear_interpolation(target_vec_x[i], vec_x, vec_y));
            }
            return result_vector;
        }
    }

    namespace ODESolver
    {
        double Euler(const double x_prev, const double y_prev, const double step_size, double (*func)(double x, double y))
        {
            return y_prev + func(x_prev, y_prev) * step_size;
        }

        double Euler(const double y_prev, const double step_size, double func_value)
        {
            return y_prev + func_value * step_size;
        }

        OWL::ArrayXD Euler(OWL::ArrayXD xArray, double yInit, double (*func)(double, double))
        {
            // initialize the results vector to zeros.
            OWL::ArrayXD resArray = OWL::Zeros(static_cast<int>(xArray.getArrayLength()));
            resArray[0] = yInit;
            for (size_t i = 1; i < xArray.getArrayLength(); i++)
            {
                double stepSize = xArray[i] - xArray[i - 1];
                resArray[i] = Euler(xArray[i - 1], resArray[i - 1], stepSize, func);
            }
            return resArray;
        }

        double rk4(const double x_prev, const double y_prev, const double step_size, double (*func)(double x, double y))
        {
            double k1 = func(x_prev, y_prev);
            double k2 = func(x_prev + 0.5 * step_size, y_prev + 0.5 * k1 * step_size);
            double k3 = func(x_prev + 0.5 * step_size, y_prev + 0.5 * k2 * step_size);
            double k4 = func(x_prev + step_size, y_prev + k3 * step_size);
            return y_prev + (k1 + 2 * k2 + 2 * k3 + k4) * (step_size / 6.0);
        }

        double rk4(const double x_prev, const double y_prev, const double step_size, std::function<double(double, double)> func)
        {
            double k1 = func(x_prev, y_prev);
            double k2 = func(x_prev + 0.5 * step_size, y_prev + 0.5 * k1 * step_size);
            double k3 = func(x_prev + 0.5 * step_size, y_prev + 0.5 * k2 * step_size);
            double k4 = func(x_prev + step_size, y_prev + k3 * step_size);
            return y_prev + (k1 + 2.0 * k2 + 2.0 * k3 + k4) * (step_size / 6.0);
        }

        OWL::ArrayXD rk4(OWL::ArrayXD xArray, double yInit, double (*func)(double, double))
        {
            OWL::ArrayXD res = OWL::Zeros(static_cast<int>(xArray.getArrayLength()));
            res[0] = yInit;
            for (size_t i = 1; i < res.getArrayLength(); i++)
            {
                double stepSize = xArray[i] - xArray[i - 1];
                res[i] = rk4(xArray[i - 1], res[i - 1], stepSize, func);
            }
            return res;
        }
    }

    namespace roots
    {
        double Brent(std::function<double(double)> f, double lower_bound, double upper_bound, double TOL, double MAX_ITER)
        {
            double a = lower_bound;
            double b = upper_bound;
            double fa = f(a); // calculated now to save function calls
            double fb = f(b); // calculated now to save function calls
            double fs = 0;    // initialize
            double s = b;

            if (!(fa * fb < 0))
            {
                std::cout << "Signs of f(lower_bound) and f(upper_bound) must be opposites" << std::endl; // throws exception if root isn't bracketed
                return s;
            }

            if (std::abs(fa) < std::abs(b)) // if magnitude of f(lower_bound) is less than magnitude of f(upper_bound)
            {
                std::swap(a, b);
                std::swap(fa, fb);
            }

            double c = a;      // c now equals the largest magnitude of the lower and upper bounds
            double fc = fa;    // precompute function evalutation for point c by assigning it the same value as fa
            bool mflag = true; // boolean flag used to evaluate if statement later on
            //    double s = 0;           // Our Root that will be returned
            double d = 0; // Only used if mflag is unset (mflag == false)

            for (unsigned int iter = 1; iter < MAX_ITER; ++iter)
            {
                // stop if converged on root or error is less than tolerance
                if (std::abs(b - a) < TOL)
                {
                    return s;
                } // end if

                if (fa != fc && fb != fc)
                {
                    // use inverse quadratic interopolation
                    s = (a * fb * fc / ((fa - fb) * (fa - fc))) + (b * fa * fc / ((fb - fa) * (fb - fc))) + (c * fa * fb / ((fc - fa) * (fc - fb)));
                }
                else
                {
                    // secant method
                    s = b - fb * (b - a) / (fb - fa);
                }

                /*
                    Crazy condition statement!:
                    -------------------------------------------------------
                    (condition 1) s is not between  (3a+b)/4  and b or
                    (condition 2) (mflag is true and |s?b| ? |b?c|/2) or
                    (condition 3) (mflag is false and |s?b| ? |c?d|/2) or
                    (condition 4) (mflag is set and |b?c| < |TOL|) or
                    (condition 5) (mflag is false and |c?d| < |TOL|)
                */
                if (((s < (3 * a + b) * 0.25) || (s > b)) ||
                    (mflag && (std::abs(s - b) >= (std::abs(b - c) * 0.5))) ||
                    (!mflag && (std::abs(s - b) >= (std::abs(c - d) * 0.5))) ||
                    (mflag && (std::abs(b - c) < TOL)) ||
                    (!mflag && (std::abs(c - d) < TOL)))
                {
                    // bisection method
                    s = (a + b) * 0.5;

                    mflag = true;
                }
                else
                {
                    mflag = false;
                }

                fs = f(s); // calculate fs
                d = c;     // first time d is being used (wasnt used on first iteration because mflag was set)
                c = b;     // set c equal to upper bound
                fc = fb;   // set f(c) = f(b)

                if (fa * fs < 0) // fa and fs have opposite signs
                {
                    b = s;
                    fb = fs; // set f(b) = f(s)
                }
                else
                {
                    a = s;
                    fa = fs; // set f(a) = f(s)
                }

                if (std::abs(fa) < std::abs(fb)) // if magnitude of fa is less than magnitude of fb
                {
                    std::swap(a, b);   // swap a and b
                    std::swap(fa, fb); // make sure f(a) and f(b) are correct after swap
                }

            } // end for

            return s;
        }

    }

    namespace MatrixSolvers
    {
        std::vector<double> TDMASolver(std::vector<double> l_diag, std::vector<double> diag, std::vector<double> u_diag, std::vector<double> col_vec)
        {
            int N = static_cast<int>(col_vec.size());

            std::vector<double> c_l_diag = l_diag;
            std::vector<double> c_diag = diag;
            std::vector<double> c_u_diag = u_diag;
            std::vector<double> c_col_vec = col_vec;

            for (int i = 1; i < N; i++)
            {
                double m = c_l_diag[i - 1] / c_diag[i - 1];
                c_diag[i] = c_diag[i] - m * c_u_diag[i - 1];
                c_col_vec[i] = c_col_vec[i] - m * c_col_vec[i - 1];
            }

            std::vector<double> xc = c_diag;
            xc.back() = c_col_vec.back() / c_diag.back();

            for (int il = N - 2; il > -1; il--)
            {
                xc[il] = (c_col_vec[il] - c_u_diag[il] * xc[il + 1]) / c_diag[il];
            }

            return xc;
        }
    }
}
