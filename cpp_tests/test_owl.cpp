//
// Created by moina on 7/10/2023.
//

#include <vector>
#include <cmath>

#include "gtest/gtest.h"

#include "extern/OWL.h"

TEST(TestArrayXDConstructor, EmptyArray)
{
    OWL::ArrayXD sampleArray = OWL::ArrayXD();
    EXPECT_EQ(0, sampleArray.getArrayLength());
}

TEST(TestArrayXDConstructor, stdVector)
{
    std::vector<double> vec = {0, 1, 2, 3, 4, 5};
    OWL::ArrayXD sampleArray = OWL::ArrayXD(vec);
    // test array size
    EXPECT_EQ(6, sampleArray.getArrayLength());
    // test array contents
    EXPECT_EQ(0, sampleArray[0]);
    EXPECT_EQ(1, sampleArray[1]);
    EXPECT_EQ(2, sampleArray[2]);
    EXPECT_EQ(3, sampleArray[3]);
    EXPECT_EQ(4, sampleArray[4]);
    EXPECT_EQ(5, sampleArray[5]);
}

TEST(TestSetters, TestGetArray)
{
    std::vector<double> vecInit = {0, 1, 2, 3, 4, 5};
    std::vector<double> vecNew = {6, 7, 8, 9, 10, 11, 12};
    OWL::ArrayXD sampleArray = OWL::ArrayXD(vecInit);
    sampleArray.setArray(vecNew);
    // test array size
    EXPECT_EQ(7, sampleArray.getArrayLength());
    // test array contents
    EXPECT_EQ(6, sampleArray[0]);
    EXPECT_EQ(7, sampleArray[1]);
    EXPECT_EQ(8, sampleArray[2]);
    EXPECT_EQ(9, sampleArray[3]);
    EXPECT_EQ(10, sampleArray[4]);
    EXPECT_EQ(11, sampleArray[5]);
    EXPECT_EQ(12, sampleArray[6]);
}

TEST(TestAuxilaries, TestcompareArrayLengths)
{
    std::vector<double> vec1 = {0, 1, 2, 3, 4, 5};
    std::vector<double> vec2 = {6, 7, 8, 9, 10, 11};
    OWL::ArrayXD sampleArray1 = OWL::ArrayXD(vec1);
    OWL::ArrayXD sampleArray2 = OWL::ArrayXD(vec2);
    EXPECT_TRUE(sampleArray1.compareArrayLength(sampleArray2));
}

TEST(TestAuxilaries, TestSum)
{
    std::vector<double> vec1 = {0, 1, 2, 3, 4, 5};
    OWL::ArrayXD sampleArray1 = OWL::ArrayXD(vec1);
    EXPECT_EQ(15, sampleArray1.sum());
}
TEST(TestAuxilaries, TestcompareArrayLengthsException)
{
    std::vector<double> vec1 = {0, 1, 2, 3, 4, 5};
    std::vector<double> vec2 = {6, 7, 8, 9, 10};
    OWL::ArrayXD sampleArray1 = OWL::ArrayXD(vec1);
    OWL::ArrayXD sampleArray2 = OWL::ArrayXD(vec2);
    EXPECT_THROW(sampleArray1.compareArrayLength(sampleArray2), std::invalid_argument);
}
TEST(TestAuxilaries, TestcheckEmptyArray)
{
    std::vector<double> vecInit = {0, 1, 2, 3, 4, 5};
    OWL::ArrayXD sampleArray = OWL::ArrayXD(vecInit);
    EXPECT_FALSE(sampleArray.checkEmptyArray());
}

TEST(TestAuxilaries, TestcheckEmptyArrayException)
{
    OWL::ArrayXD sampleArray = OWL::ArrayXD();
    EXPECT_THROW(sampleArray.checkEmptyArray(), std::invalid_argument);
}

TEST(TestAuxilaries, TestIsEqual)
{
    std::vector<double> vecInit1 = {0, 1, 2, 3, 4, 5};
    std::vector<double> vecInit2 = {0, 1, 2, 3, 4, 5};
    std::vector<double> vecInit3 = {0, 1, 2, 3, 6, 5};
    std::vector<double> vecInit4 = {0, 1, 2, 3};
    OWL::ArrayXD sampleArray1 = OWL::ArrayXD(vecInit1);
    OWL::ArrayXD sampleArray2 = OWL::ArrayXD(vecInit2);
    OWL::ArrayXD sampleArray3 = OWL::ArrayXD(vecInit3);
    OWL::ArrayXD sampleArray4 = OWL::ArrayXD(vecInit4);
    EXPECT_TRUE(sampleArray1.isEqual(sampleArray2));
    EXPECT_FALSE(sampleArray1.isEqual(sampleArray3));
    EXPECT_FALSE(sampleArray1.isEqual(sampleArray4));
}

TEST(TestAuxilaries, TestIsApproxEqual)
{
    std::vector<double> vecInit1 = {0, 0.95, 2, 3.1, 4.05, 5.03};
    std::vector<double> vecInit2 = {0, 1, 2, 3, 4, 5};
    std::vector<double> vecInit3 = {0, 1, 2, 3, 6, 5};
    std::vector<double> vecInit4 = {0, 1, 2, 3};
    OWL::ArrayXD sampleArray1 = OWL::ArrayXD(vecInit1);
    OWL::ArrayXD sampleArray2 = OWL::ArrayXD(vecInit2);
    OWL::ArrayXD sampleArray3 = OWL::ArrayXD(vecInit3);
    OWL::ArrayXD sampleArray4 = OWL::ArrayXD(vecInit4);
    EXPECT_TRUE(sampleArray1.isApproxEqual(sampleArray2, 0.1));
}

TEST(TestAuxilaries, TestFindMinValue)
{
    std::vector<double> vecInit = {0, 5, 10, 225, 20, 25};
    OWL::ArrayXD sampleArray = OWL::ArrayXD(vecInit);
    OWL::ArrayXD EmptyArray = OWL::ArrayXD();
    EXPECT_EQ(0, sampleArray.findMinElement());
    EXPECT_THROW(EmptyArray.findMinElement(), OWL::EmptyArrayException);
}

TEST(TestAuxilaries, TestFindMaxValue)
{
    std::vector<double> vecInit = {0, 5, 10, 225, 20, 25};
    OWL::ArrayXD sampleArray = OWL::ArrayXD(vecInit);
    OWL::ArrayXD EmptyArray = OWL::ArrayXD();
    EXPECT_EQ(225, sampleArray.findMaxELement());
    EXPECT_THROW(EmptyArray.findMaxELement(), OWL::EmptyArrayException);
}

TEST(TestAuxilaries, TestFindClosestElement)
{
    std::vector<double> vecInit = {0, 1, 2, 3, 4, 5};
    OWL::ArrayXD sampleArray = OWL::ArrayXD(vecInit);
    double inputValue = 2.25;
    EXPECT_EQ(2, sampleArray.findClosestElement(inputValue));
}

TEST(TestAuxilaries, TestFindClosestElementIndex)
{
    std::vector<double> vecInit = {0, 1, 2, 3, 4, 5};
    OWL::ArrayXD sampleArray = OWL::ArrayXD(vecInit);
    double inputValue1 = 1.25;
    double inputValue2 = 2.25;
    double inputValue3 = 3.75;
    double inputValue4 = 10;
    EXPECT_EQ(1, sampleArray.findClosestElementIndex(inputValue1));
    EXPECT_EQ(2, sampleArray.findClosestElementIndex(inputValue2));
    EXPECT_EQ(4, sampleArray.findClosestElementIndex(inputValue3));
    EXPECT_EQ(5, sampleArray.findClosestElementIndex(inputValue4));
}

TEST(TestAuxilaries, TestFindClosestElementLessThan1)
{
    std::vector<double> vecInit = {0, 1, 2, 3, 4, 5};
    OWL::ArrayXD sampleArray = OWL::ArrayXD(vecInit);
    double inputValue = 2.25;
    EXPECT_EQ(2, sampleArray.findCLosestElementLessThan(inputValue));
}

TEST(TestAuxilaries, TestFindClosestElementLessThan2)
{
    std::vector<double> vecInit = {0, 5, 10, 15, 20, 25};
    OWL::ArrayXD sampleArray = OWL::ArrayXD(vecInit);
    double inputValue = 7.25;
    EXPECT_EQ(5, sampleArray.findCLosestElementLessThan(inputValue));
}

TEST(TestAuxilaries, TestFindClosestElementLessThan3)
{
    std::vector<double> vecInit = {0, 5, 10, 15, 20, 25};
    OWL::ArrayXD sampleArray = OWL::ArrayXD(vecInit);
    double inputValue = -0.5;
    EXPECT_THROW(sampleArray.findCLosestElementLessThan(inputValue), std::invalid_argument);
}

TEST(TestAuxilaries, TestFindClosestElementLessThanIndex)
{
    std::vector<double> vecInit = {0, 5, 10, 15, 20, 25};
    OWL::ArrayXD sampleArray = OWL::ArrayXD(vecInit);
    OWL::ArrayXD EmptyArray = OWL::ArrayXD();
    double inputValue1 = 5.5;
    double inputValue2 = 12.5;
    double inputValue3 = 50;
    double inputValue4 = -1;
    EXPECT_EQ(1, sampleArray.findCLosestElementLessThanIndex(inputValue1));
    EXPECT_EQ(2, sampleArray.findCLosestElementLessThanIndex(inputValue2));
    EXPECT_EQ(5, sampleArray.findCLosestElementLessThanIndex(inputValue3));
    EXPECT_THROW(sampleArray.findCLosestElementLessThanIndex(inputValue4), std::invalid_argument);
    EXPECT_THROW(EmptyArray.findCLosestElementLessThanIndex(inputValue1), OWL::EmptyArrayException);
}

TEST(TestAuxilaries, TestFindClosestElementGreaterThan1)
{
    std::vector<double> vecInit = {0, 5, 10, 15, 20, 25};
    OWL::ArrayXD sampleArray = OWL::ArrayXD(vecInit);
    double inputValue = 7.25;
    EXPECT_EQ(10, sampleArray.findCLosestElementGreaterThan(inputValue));
}

TEST(TestAuxilaries, TestFindClosestElementGreaterThan2)
{
    std::vector<double> vecInit = {0, 5, 10, 15, 20, 25};
    OWL::ArrayXD sampleArray = OWL::ArrayXD(vecInit);
    double inputValue = 50;
    EXPECT_THROW(sampleArray.findCLosestElementGreaterThan(inputValue), std::invalid_argument);
}

TEST(TestAuxilaries, TestFindClosestElementGreaterThanIndex)
{
    std::vector<double> vecInit = {0, 5, 10, 15, 20, 25};
    OWL::ArrayXD sampleArray = OWL::ArrayXD(vecInit);
    OWL::ArrayXD EmptyArray = OWL::ArrayXD();
    double inputValue1 = 5.5;
    double inputValue2 = 12.5;
    double inputValue3 = -1;
    double inputValue4 = 50;
    EXPECT_EQ(2, sampleArray.findCLosestElementGreaterThanIndex(inputValue1));
    EXPECT_EQ(3, sampleArray.findCLosestElementGreaterThanIndex(inputValue2));
    EXPECT_EQ(0, sampleArray.findCLosestElementGreaterThanIndex(inputValue3));
    EXPECT_THROW(sampleArray.findCLosestElementGreaterThanIndex(inputValue4), std::invalid_argument);
    EXPECT_THROW(EmptyArray.findCLosestElementGreaterThanIndex(inputValue1), OWL::EmptyArrayException);
}

TEST(TestIndexOverloads, TestIndexAccess)
{
    std::vector<double> vec1 = {0, 1, 2, 3, 4, 5};
    OWL::ArrayXD sampleArray1 = OWL::ArrayXD(vec1);
    EXPECT_EQ(0, sampleArray1[0]);
    EXPECT_EQ(1, sampleArray1[1]);
    EXPECT_EQ(2, sampleArray1[2]);
    EXPECT_EQ(3, sampleArray1[3]);
    EXPECT_EQ(4, sampleArray1[4]);
    EXPECT_EQ(5, sampleArray1[5]);
    EXPECT_THROW(sampleArray1[6], std::invalid_argument);
}

TEST(TestOperatorOverloads, TestIndexManu)
{
    // initialize OWL::ArrayXD
    std::vector<double> vec1 = {0, 1, 2, 3, 4, 5};
    OWL::ArrayXD sampleArray1 = OWL::ArrayXD(vec1);
    // Change the values of all elements of the OWL::ArrayxXD
    sampleArray1[0] = 100;
    sampleArray1[1] = 200;
    sampleArray1[2] = 300;
    sampleArray1[3] = 400;
    sampleArray1[4] = 500;
    sampleArray1[5] = 600;
    // Google Tests on all the elements.
    EXPECT_EQ(100, sampleArray1[0]);
    EXPECT_EQ(200, sampleArray1[1]);
    EXPECT_EQ(300, sampleArray1[2]);
    EXPECT_EQ(400, sampleArray1[3]);
    EXPECT_EQ(500, sampleArray1[4]);
    EXPECT_EQ(600, sampleArray1[5]);
}

// Arithmetic overloads

/**
 * Test for scalar  addition is the scalar is on the rhs of the addition.
 */
TEST(TestArithmeticOperators, TestAddScalarRHS)
{
    std::vector<double> vec1 = {0, 1, 2, 3, 4, 5};
    double scalar = 1;
    OWL::ArrayXD sampleArray1 = OWL::ArrayXD(vec1);
    OWL::ArrayXD resultArray = sampleArray1 + scalar;
    EXPECT_EQ(1, resultArray[0]);
    EXPECT_EQ(2, resultArray[1]);
    EXPECT_EQ(3, resultArray[2]);
    EXPECT_EQ(4, resultArray[3]);
    EXPECT_EQ(5, resultArray[4]);
    EXPECT_EQ(6, resultArray[5]);
}

/**
 * Test for scalar  addition is the scalar is on the lhs of the addition.
 */
TEST(TestArithmeticOperators, TestAddScalarLHS)
{
    std::vector<double> vec1 = {0, 1, 2, 3, 4, 5};
    double scalar = 1;
    OWL::ArrayXD sampleArray1 = OWL::ArrayXD(vec1);
    OWL::ArrayXD resultArray = scalar + sampleArray1;
    EXPECT_EQ(1, resultArray[0]);
    EXPECT_EQ(2, resultArray[1]);
    EXPECT_EQ(3, resultArray[2]);
    EXPECT_EQ(4, resultArray[3]);
    EXPECT_EQ(5, resultArray[4]);
    EXPECT_EQ(6, resultArray[5]);
}

TEST(TestArithmeticOperators, TestAdd)
{
    std::vector<double> vec1 = {0, 1, 2, 3, 4, 5};
    std::vector<double> vec2 = {6, 7, 8, 9, 10, 11};
    OWL::ArrayXD sampleArray1 = OWL::ArrayXD(vec1);
    OWL::ArrayXD sampleArray2 = OWL::ArrayXD(vec2);
    OWL::ArrayXD resultArray = sampleArray1 + sampleArray2;
    EXPECT_EQ(6, resultArray[0]);
    EXPECT_EQ(8, resultArray[1]);
    EXPECT_EQ(10, resultArray[2]);
    EXPECT_EQ(12, resultArray[3]);
    EXPECT_EQ(14, resultArray[4]);
    EXPECT_EQ(16, resultArray[5]);
}

TEST(TestArithmeticOperators, TestSubtract)
{
    std::vector<double> vec1 = {0, 1, 2, 3, 4, 5};
    std::vector<double> vec2 = {6, 7, 8, 9, 10, 11};
    OWL::ArrayXD sampleArray1 = OWL::ArrayXD(vec1);
    OWL::ArrayXD sampleArray2 = OWL::ArrayXD(vec2);
    OWL::ArrayXD resultArray = sampleArray1 - sampleArray2;
    EXPECT_EQ(-6, resultArray[0]);
    EXPECT_EQ(-6, resultArray[1]);
    EXPECT_EQ(-6, resultArray[2]);
    EXPECT_EQ(-6, resultArray[3]);
    EXPECT_EQ(-6, resultArray[4]);
    EXPECT_EQ(-6, resultArray[5]);
}

TEST(TestArithmeticOperators, TestScalarMultiply)
{
    std::vector<double> vecInit = {0, 1, 2, 3, 4, 5};
    OWL::ArrayXD sampleArray = OWL::ArrayXD(vecInit);
    OWL::ArrayXD resultArray = sampleArray * 10;
    EXPECT_EQ(0, resultArray[0]);
    EXPECT_EQ(10, resultArray[1]);
    EXPECT_EQ(20, resultArray[2]);
    EXPECT_EQ(30, resultArray[3]);
    EXPECT_EQ(40, resultArray[4]);
    EXPECT_EQ(50, resultArray[5]);
}

TEST(TestArithmeticOperators, TestElementMultiply)
{
    std::vector<double> vec1 = {0, 1, 2, 3, 4, 5};
    std::vector<double> vec2 = {6, 7, 8, 9, 10, 11};
    OWL::ArrayXD sampleArray1 = OWL::ArrayXD(vec1);
    OWL::ArrayXD sampleArray2 = OWL::ArrayXD(vec2);
    OWL::ArrayXD resultArray = sampleArray1 * sampleArray2;
    EXPECT_EQ(0, resultArray[0]);
    EXPECT_EQ(7, resultArray[1]);
    EXPECT_EQ(16, resultArray[2]);
    EXPECT_EQ(27, resultArray[3]);
    EXPECT_EQ(40, resultArray[4]);
    EXPECT_EQ(55, resultArray[5]);
}

TEST(TestArithmeticOperators, TestScalarMultiplyRHS)
{
    std::vector<double> vec1 = {0, 1, 2, 3, 4, 5};
    double scalar = 10;
    OWL::ArrayXD resultArray = scalar * vec1;
    EXPECT_EQ(0, resultArray[0]);
    EXPECT_EQ(10, resultArray[1]);
    EXPECT_EQ(20, resultArray[2]);
    EXPECT_EQ(30, resultArray[3]);
    EXPECT_EQ(40, resultArray[4]);
    EXPECT_EQ(50, resultArray[5]);
}

// input operators
TEST(TestInputOutputOperator, TestInputOperator)
{
    OWL::ArrayXD sampleArray;
    sampleArray << 0.0;
    sampleArray << 1.0;
    EXPECT_EQ(0, sampleArray[0]);
    EXPECT_EQ(1, sampleArray[1]);
    EXPECT_EQ(2, sampleArray.getArrayLength());
}

TEST(TestFunctions, TestAbs)
{
    std::vector<double> vec = {-1, -2, -3, -4};
    // check input array values
    OWL::ArrayXD array = OWL::ArrayXD(vec);
    EXPECT_EQ(-1, array[0]);
    EXPECT_EQ(-2, array[1]);
    EXPECT_EQ(-3, array[2]);
    EXPECT_EQ(-4, array[3]);
    // check output array values
    OWL::ArrayXD absArray = OWL::abs(array);
    EXPECT_EQ(1, absArray[0]);
    EXPECT_EQ(2, absArray[1]);
    EXPECT_EQ(3, absArray[2]);
    EXPECT_EQ(4, absArray[3]);
}

// Trig functions
TEST(TestTrigFunctions, TestSin)
{
    std::vector<double> angleVec = {0, 1.57, 2.36, 3.14};
    OWL::ArrayXD angleArray = OWL::ArrayXD(angleVec);
    OWL::ArrayXD resultArray = OWL::sin(angleArray);
    EXPECT_EQ(std::sin(angleVec[0]), resultArray[0]);
    EXPECT_EQ(std::sin(angleVec[1]), resultArray[1]);
    EXPECT_EQ(std::sin(angleVec[2]), resultArray[2]);
    EXPECT_EQ(std::sin(angleVec[3]), resultArray[3]);
}

TEST(TestTrigFunctions, TestCos)
{
    std::vector<double> angleVec = {0, 1.57, 2.36, 3.14};
    OWL::ArrayXD angleArray = OWL::ArrayXD(angleVec);
    OWL::ArrayXD resultArray = OWL::cos(angleArray);
    EXPECT_EQ(std::cos(angleVec[0]), resultArray[0]);
    EXPECT_EQ(std::cos(angleVec[1]), resultArray[1]);
    EXPECT_EQ(std::cos(angleVec[2]), resultArray[2]);
    EXPECT_EQ(std::cos(angleVec[3]), resultArray[3]);
}

TEST(TestTrigFunctions, TestTan)
{
    std::vector<double> angleVec = {0, 1.57, 2.36, 3.14};
    OWL::ArrayXD angleArray = OWL::ArrayXD(angleVec);
    OWL::ArrayXD resultArray = OWL::tan(angleArray);
    EXPECT_EQ(std::tan(angleVec[0]), resultArray[0]);
    EXPECT_EQ(std::tan(angleVec[1]), resultArray[1]);
    EXPECT_EQ(std::tan(angleVec[2]), resultArray[2]);
    EXPECT_EQ(std::tan(angleVec[3]), resultArray[3]);
}

TEST(TestTrigFunctions, TestArcSin)
{
    std::vector<double> angleVec = {0, 0.25, 0.5, 0.75};
    OWL::ArrayXD angleArray = OWL::ArrayXD(angleVec);
    OWL::ArrayXD resultArray = OWL::asin(angleArray);
    EXPECT_EQ(std::asin(angleVec[0]), resultArray[0]);
    EXPECT_EQ(std::asin(angleVec[1]), resultArray[1]);
    EXPECT_EQ(std::asin(angleVec[2]), resultArray[2]);
    EXPECT_EQ(std::asin(angleVec[3]), resultArray[3]);
}

TEST(TestTrigFunctions, TestArcCos)
{
    std::vector<double> angleVec = {0, 0.25, 0.5, 0.75};
    OWL::ArrayXD angleArray = OWL::ArrayXD(angleVec);
    OWL::ArrayXD resultArray = OWL::acos(angleArray);
    EXPECT_EQ(std::acos(angleVec[0]), resultArray[0]);
    EXPECT_EQ(std::acos(angleVec[1]), resultArray[1]);
    EXPECT_EQ(std::acos(angleVec[2]), resultArray[2]);
    EXPECT_EQ(std::acos(angleVec[3]), resultArray[3]);
}

TEST(TestTrigFunctions, TestArcTan)
{
    std::vector<double> angleVec = {0, 0.25, 0.5, 0.75};
    OWL::ArrayXD angleArray = OWL::ArrayXD(angleVec);
    OWL::ArrayXD resultArray = OWL::atan(angleArray);
    EXPECT_EQ(std::atan(angleVec[0]), resultArray[0]);
    EXPECT_EQ(std::atan(angleVec[1]), resultArray[1]);
    EXPECT_EQ(std::atan(angleVec[2]), resultArray[2]);
    EXPECT_EQ(std::atan(angleVec[3]), resultArray[3]);
}

// exponential and log functions
TEST(TestExpLogFunctions, TestExp)
{
    int length = 10;
    OWL::ArrayXD inputArray = OWL::LinSpaced(0, 10, 11);
    OWL::ArrayXD resultArray = OWL::exp(inputArray);
    for (size_t i = 0; i < inputArray.getArrayLength(); i++)
    {
        EXPECT_EQ(std::exp(i), resultArray[i]);
    }
}

TEST(TestExpLogFunctions, TestLog10)
{
    OWL::ArrayXD inputArray = OWL::LinSpaced(1, 10, 10);
    OWL::ArrayXD resultArray = OWL::log10(inputArray);
    for (size_t i = 0; i < inputArray.getArrayLength(); i++)
    {
        EXPECT_EQ(std::log10(i + 1), resultArray[i]);
    }
}

TEST(TestExpLogFunctions, TestLn)
{
    OWL::ArrayXD inputArray = OWL::LinSpaced(1, 10, 10);
    OWL::ArrayXD resultArray = OWL::ln(inputArray);
    for (size_t i = 0; i < inputArray.getArrayLength(); i++)
    {
        EXPECT_EQ(std::log(i + 1), resultArray[i]);
    }
}

TEST(TestMatrixXDConstructor, TestDefaultConstructor)
{
    OWL::MatrixXD sampleMatrix = OWL::MatrixXD();
    EXPECT_EQ(0, sampleMatrix.getRowSize());
    EXPECT_EQ(0, sampleMatrix.getColSize());
}

TEST(TestMatrixXDConstructor, TestOverloadConstructor)
{
    // Check if exception is thrown in case of inputting an empty std::vector.
    std::vector<OWL::ArrayXD> emptyVec;
    EXPECT_THROW(OWL::MatrixXD(emptyVec).getColSize(), std::invalid_argument);
    // Check overload constructor
    std::vector<OWL::ArrayXD> sampleVec;
    OWL::ArrayXD sampleArray = OWL::ArrayXD();
    sampleVec.push_back(sampleArray);
    OWL::MatrixXD sampleMatrix = OWL::MatrixXD(sampleVec);
    EXPECT_EQ(0, sampleMatrix.getRowSize());
    EXPECT_EQ(0, sampleMatrix.getColSize());
    sampleVec.push_back(sampleArray);
    OWL::MatrixXD sampleMatrix2 = OWL::MatrixXD(sampleVec);
    EXPECT_EQ(0, sampleMatrix2.getRowSize());
    EXPECT_EQ(0, sampleMatrix2.getColSize());
    // test with a non-empty array
    std::vector<double> sampleVec1;
    sampleVec1.push_back(1);
    OWL::ArrayXD sampleArray1 = OWL::ArrayXD(sampleVec1);
    std::vector<OWL::ArrayXD> sampleArrayMat;
    sampleArrayMat.push_back(sampleArray1);
    sampleArrayMat.push_back(sampleArray1);
    sampleArrayMat.push_back(sampleArray1);
    OWL::MatrixXD sampleMatrix3 = OWL::MatrixXD(sampleArrayMat);
    EXPECT_EQ(1, sampleMatrix3[0][0]);
    EXPECT_EQ(1, sampleMatrix3[1][0]);
    EXPECT_EQ(1, sampleMatrix3[2][0]);
    EXPECT_EQ(3, sampleMatrix3.getRowSize());
    EXPECT_EQ(1, sampleMatrix3.getColSize());
}

TEST(TestMatrixXDConstructor, TestOverloadConstructor2)
{
    OWL::MatrixXD sampleMatrix = OWL::MatrixXD(2, 3);
    // check size
    EXPECT_EQ(2, sampleMatrix.getRowSize());
    EXPECT_EQ(3, sampleMatrix.getColSize());
    // check elements
    EXPECT_EQ(0, sampleMatrix[0][0]);
    EXPECT_EQ(0, sampleMatrix[0][1]);
    EXPECT_EQ(0, sampleMatrix[0][2]);
    EXPECT_EQ(0, sampleMatrix[1][0]);
    EXPECT_EQ(0, sampleMatrix[1][1]);
    EXPECT_EQ(0, sampleMatrix[1][2]);
}

TEST(TestMatrixXDFunctions, TestCompareSize)
{
    OWL::ArrayXD row1;
    OWL::ArrayXD row2;
    OWL::ArrayXD row3;
    row1 << 0;
    row1 << 1;
    row1 << 2;
    row2 << 3;
    row2 << 4;
    row2 << 5;
    row3 << 6;
    row3 << 7;
    row3 << 8;

    OWL::MatrixXD sampleMatrix1 = OWL::MatrixXD();
    sampleMatrix1 << row1;
    sampleMatrix1 << row2;
    sampleMatrix1 << row3;

    OWL::MatrixXD sampleMatrix2 = OWL::MatrixXD();
    sampleMatrix2 << row1;

    EXPECT_FALSE(sampleMatrix1.compareSize(sampleMatrix2));
    EXPECT_TRUE(sampleMatrix1.compareSize(sampleMatrix1));
}

TEST(TestMatrixXDFunctions, TestGetCol)
{
    OWL::ArrayXD row1;
    OWL::ArrayXD row2;
    OWL::ArrayXD row3;
    row1 << 0;
    row1 << 1;
    row1 << 2;
    row2 << 3;
    row2 << 4;
    row2 << 5;
    row3 << 6;
    row3 << 7;
    row3 << 8;

    OWL::MatrixXD sampleMatrix1 = OWL::MatrixXD();
    sampleMatrix1 << row1;
    sampleMatrix1 << row2;
    sampleMatrix1 << row3;

    OWL::ArrayXD sampleArray = sampleMatrix1.getCol(0);

    EXPECT_EQ(0, sampleArray[0]);
    EXPECT_EQ(3, sampleArray[1]);
    EXPECT_EQ(6, sampleArray[2]);
}

TEST(TestMatrixXDFunctions, TestisSquare)
{
    OWL::ArrayXD row1;
    OWL::ArrayXD row2;
    OWL::ArrayXD row3;
    row1 << 0;
    row1 << 1;
    row1 << 2;
    row2 << 3;
    row2 << 4;
    row2 << 5;
    row3 << 6;
    row3 << 7;
    row3 << 8;

    OWL::MatrixXD sampleMatrix1 = OWL::MatrixXD();
    sampleMatrix1 << row1;
    sampleMatrix1 << row2;
    sampleMatrix1 << row3;

    OWL::MatrixXD sampleMatrix2 = OWL::MatrixXD();
    sampleMatrix2 << row1;

    EXPECT_TRUE(sampleMatrix1.isSquare());
    EXPECT_FALSE(sampleMatrix2.isSquare());
}

TEST(TestMatrixXDFunctions, TestSubMatrix)
{
    OWL::ArrayXD row1;
    OWL::ArrayXD row2;
    OWL::ArrayXD row3;
    row1 << 7;
    row1 << 1;
    row1 << 3;
    row2 << 2;
    row2 << 4;
    row2 << 1;
    row3 << 1;
    row3 << 5;
    row3 << 1;

    OWL::MatrixXD sampleMatrix1 = OWL::MatrixXD();
    sampleMatrix1 << row1;
    sampleMatrix1 << row2;
    sampleMatrix1 << row3;

    OWL::MatrixXD sampleMatrix2 = sampleMatrix1.submatrix(0, 0);

    // test size
    EXPECT_EQ(2, sampleMatrix2.getRowSize());
    EXPECT_EQ(2, sampleMatrix2.getColSize());
    // test element values
    EXPECT_EQ(4, sampleMatrix2[0][0]);
    EXPECT_EQ(1, sampleMatrix2[0][1]);
    EXPECT_EQ(5, sampleMatrix2[1][0]);
    EXPECT_EQ(1, sampleMatrix2[1][1]);
}
TEST(TestMatrixXDFunctions, TestDet)
{
    OWL::ArrayXD row10;
    OWL::ArrayXD row20;
    row10 << 1;
    row10 << 7;
    row20 << 5;
    row20 << 2;

    OWL::MatrixXD sampleMatrix10 = OWL::MatrixXD();
    sampleMatrix10 << row10;
    sampleMatrix10 << row20;

    OWL::ArrayXD row1;
    OWL::ArrayXD row2;
    OWL::ArrayXD row3;
    row1 << 7;
    row1 << 1;
    row1 << 3;
    row2 << 2;
    row2 << 4;
    row2 << 1;
    row3 << 1;
    row3 << 5;
    row3 << 1;

    OWL::MatrixXD sampleMatrix1 = OWL::MatrixXD();
    sampleMatrix1 << row1;
    sampleMatrix1 << row2;
    sampleMatrix1 << row3;

    EXPECT_EQ(-33, sampleMatrix10.det());
    EXPECT_EQ(10, sampleMatrix1.det());
}

TEST(TestMatrixXDFunctions, TestisSingular)
{
    OWL::ArrayXD row10;
    OWL::ArrayXD row20;
    row10 << 1;
    row10 << 7;
    row20 << 5;
    row20 << 2;

    OWL::MatrixXD sampleMatrix10 = OWL::MatrixXD();
    sampleMatrix10 << row10;
    sampleMatrix10 << row20;

    OWL::ArrayXD row1;
    OWL::ArrayXD row2;
    OWL::ArrayXD row3;
    row1 << 1;
    row1 << -2;
    row1 << -1;
    row2 << -3;
    row2 << 3;
    row2 << 0;
    row3 << 2;
    row3 << 2;
    row3 << 4;

    OWL::MatrixXD sampleMatrix1 = OWL::MatrixXD();
    sampleMatrix1 << row1;
    sampleMatrix1 << row2;
    sampleMatrix1 << row3;

    EXPECT_FALSE(sampleMatrix10.isSingular());
    EXPECT_TRUE(sampleMatrix1.isSingular());
}

TEST(TestMatrixXDOperatorOverload, TestInputOperator)
{
    OWL::MatrixXD sampleMatrix = OWL::MatrixXD();
    OWL::ArrayXD sampleArray = OWL::ArrayXD();
    sampleArray << 0;
    sampleArray << 1;
    sampleArray << 2;
    sampleMatrix << sampleArray;
    EXPECT_EQ(1, sampleMatrix.getRowSize());
    EXPECT_EQ(3, sampleMatrix.getColSize());
}

TEST(TestMatrixXDOperatorOverload, TestIndexOperator)
{
    OWL::MatrixXD sampleMatrix = OWL::MatrixXD();
    OWL::ArrayXD sampleArray = OWL::ArrayXD();
    sampleArray << 0;
    sampleArray << 1;
    sampleArray << 2;
    sampleMatrix << sampleArray;
    EXPECT_EQ(0, sampleMatrix[0][0]);
    EXPECT_EQ(1, sampleMatrix[0][1]);
    EXPECT_EQ(2, sampleMatrix[0][2]);
    EXPECT_EQ(3, sampleMatrix.getColSize());
    EXPECT_THROW(sampleMatrix[1], OWL::RowIndexExceedRowSizeException);
}

TEST(TestMatrixXDOperatorOverload, TestMatrixAddition)
{
    OWL::ArrayXD row1;
    OWL::ArrayXD row2;
    OWL::ArrayXD row3;
    row1 << 0;
    row1 << 1;
    row1 << 2;
    row2 << 3;
    row2 << 4;
    row2 << 5;
    row3 << 6;
    row3 << 7;
    row3 << 8;

    OWL::MatrixXD sampleMatrix1 = OWL::MatrixXD();
    sampleMatrix1 << row1;
    sampleMatrix1 << row2;
    sampleMatrix1 << row3;

    OWL::MatrixXD sampleMatrix2 = sampleMatrix1;
    OWL::MatrixXD sampleMatrix3 = sampleMatrix1 + sampleMatrix2;

    EXPECT_EQ(0, sampleMatrix3[0][0]);
    EXPECT_EQ(2, sampleMatrix3[0][1]);
    EXPECT_EQ(4, sampleMatrix3[0][2]);
    EXPECT_EQ(6, sampleMatrix3[1][0]);
    EXPECT_EQ(8, sampleMatrix3[1][1]);
    EXPECT_EQ(10, sampleMatrix3[1][2]);
    EXPECT_EQ(12, sampleMatrix3[2][0]);
    EXPECT_EQ(14, sampleMatrix3[2][1]);
    EXPECT_EQ(16, sampleMatrix3[2][2]);
}

TEST(TestMatrixXDOperatorOverload, TestMatrixSubtraction)
{
    OWL::ArrayXD row1;
    OWL::ArrayXD row2;
    OWL::ArrayXD row3;
    row1 << 0;
    row1 << 1;
    row1 << 2;
    row2 << 3;
    row2 << 4;
    row2 << 5;
    row3 << 6;
    row3 << 7;
    row3 << 8;

    OWL::MatrixXD sampleMatrix1 = OWL::MatrixXD();
    sampleMatrix1 << row1;
    sampleMatrix1 << row2;
    sampleMatrix1 << row3;

    OWL::MatrixXD sampleMatrix2 = sampleMatrix1;
    OWL::MatrixXD sampleMatrix3 = sampleMatrix1 - sampleMatrix2;

    EXPECT_EQ(0, sampleMatrix3[0][0]);
    EXPECT_EQ(0, sampleMatrix3[0][1]);
    EXPECT_EQ(0, sampleMatrix3[0][2]);
    EXPECT_EQ(0, sampleMatrix3[1][0]);
    EXPECT_EQ(0, sampleMatrix3[1][1]);
    EXPECT_EQ(0, sampleMatrix3[1][2]);
    EXPECT_EQ(0, sampleMatrix3[2][0]);
    EXPECT_EQ(0, sampleMatrix3[2][1]);
    EXPECT_EQ(0, sampleMatrix3[2][2]);
}

TEST(TestMatrixXDOperatorOverload, TestMatrixMultiplication)
{
    OWL::ArrayXD row1;
    OWL::ArrayXD row2;
    row1 << 0;
    row1 << 1;
    row2 << 2;
    row2 << 3;
    OWL::MatrixXD sampleMatrix1 = OWL::MatrixXD();
    sampleMatrix1 << row1;
    sampleMatrix1 << row2;

    OWL::ArrayXD row11;
    OWL::ArrayXD row22;
    row11 << 0;
    row22 << 1;
    OWL::MatrixXD sampleMatrix2 = OWL::MatrixXD();
    sampleMatrix2 << row11;
    sampleMatrix2 << row22;

    OWL::MatrixXD sampleMatrix3 = sampleMatrix1 * sampleMatrix2;

    EXPECT_EQ(1, sampleMatrix3[0][0]);
    EXPECT_EQ(3, sampleMatrix3[1][0]);
    EXPECT_EQ(2, sampleMatrix3.getRowSize());
    EXPECT_EQ(1, sampleMatrix3.getColSize());
}

TEST(TestMatrixXDOperatorOverload, TestMatrixAccessor)
{
    OWL::ArrayXD row1;
    OWL::ArrayXD row2;
    OWL::ArrayXD row3;
    row1 << 1;
    row2 << 2;
    row3 << 3;
    OWL::MatrixXD sampleMatrix1 = OWL::MatrixXD();
    sampleMatrix1 << row1;
    sampleMatrix1 << row2;
    sampleMatrix1 << row3;

    // EXPECT_EQ(sampleMatrix1(0, 0), 1);
    // EXPECT_EQ(sampleMatrix1(1, 0), 2);
    // EXPECT_EQ(sampleMatrix1(2, 0), 3);

    // EXPECT_THROW(sampleMatrix1(0,1), std::exception);
}

/**
 * @brief Construct a new TEST object.  Example obtained from https://www.quantstart.com/articles/Tridiagonal-Matrix-Algorithm-Thomas-Algorithm-in-C/
 *
 */
TEST(MatrixSolversTest, TDMASolver)
{
    const size_t N = 4;
    double delta_x = 1.0 / static_cast<double>(N);
    double delta_t = 0.001;
    double r = delta_t / (delta_x * delta_x);

    std::vector<double> l_diag(N - 1, 1);
    std::vector<double> diag(N, -2.6);
    std::vector<double> u_diag(N - 1, 1);
    std::vector<double> b(N, 0.0);
    // std::vector<double> f(N, 0.0);

    b[0] = -240;
    b.back() = -150;

    std::vector<double> result = Newton::MatrixSolvers::TDMASolver(l_diag, diag, u_diag, b);

    EXPECT_NEAR(result[0], 118.0, 1);
    EXPECT_NEAR(result[1], 67.0, 1);
    EXPECT_NEAR(result[2], 56.0, 1);
    EXPECT_NEAR(result[3], 79.35619, 0.001);
}
