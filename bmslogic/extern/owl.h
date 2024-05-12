/**
 * @file owl.h
 * @author Moin Ahmed (moinahmed100@gmail.com)
 * @brief The OWL package is obtained from : https://github.com/m0in92/OWL which is also created by Moin Ahmed on 7/4/2023.
 * This header file was added to BMSLogic on May 3, 2024 and will be modified as seem fit.
 * @version 0.1
 * @date 2024-05-03
 *
 * @copyright Copyright (c) 2024
 *
 */

#ifndef BMSLOGIC_OWL_H
#define BMSLOGIC_OWL_H

#include <iostream>
#include <vector>
#include <cmath>
#include <stdexcept>
#include <exception>
#include <limits>
#include <functional>

/**
 * @class OWL
 *
 * @brief allows for the functionality for the array operations using std::vector
 */
namespace OWL
{
    /*
     * Inherited exception class to handle situations when the array lengths/sizes do not match up.
     */
    class SizeMismatchException : public std::exception
    {
    public:
        const char *what();
    };

    /*
     * Inherited exception class to handle situations when operations are required but the array is empty.
     */
    class EmptyArrayException : public std::exception
    {
    public:
        const char *what();
    };

    /**
     * Class to handle arrays containing elements of type double of any length (or size).
     */
    class ArrayXD
    {
    public:
        ArrayXD();
        ArrayXD(std::vector<double> &vec);
        ~ArrayXD(){};
        // Getters
        const size_t getArrayLength() { return arrayLength; };
        const std::vector<double> getArray() { return array; };
        // Setters
        void setArray(std::vector<double> &newArray);
        // Auxialaries
        void append(double new_element) { array.push_back(new_element); }
        size_t size() { return array.size(); };
        void display();
        double isEqual(ArrayXD &);
        double isApproxEqual(ArrayXD &, double);
        double sum();
        bool compareArrayLength(ArrayXD &);
        bool checkEmptyArray();
        double findMinElement();
        double findMaxELement();
        double findClosestElement(double &);
        size_t findClosestElementIndex(double &);
        double findCLosestElementLessThan(double &);
        size_t findCLosestElementLessThanIndex(double &);
        double findCLosestElementGreaterThan(double &);
        size_t findCLosestElementGreaterThanIndex(double &);
        // operator overloads
        double &operator[](size_t);
        ArrayXD operator+(double &);
        ArrayXD operator+(ArrayXD &);
        ArrayXD operator-(ArrayXD &);
        ArrayXD operator*(const double);
        ArrayXD operator*(ArrayXD &);
        void operator<<(double inputValue)
        {
            array.push_back(inputValue);
            arrayLength += 1;
        }

    private:
        size_t arrayLength;
        std::vector<double> array;
        // arithmetic operations
        ArrayXD add(ArrayXD &);
        ArrayXD subtract(ArrayXD &);
        ArrayXD multiply(const double &);
        ArrayXD multiply(ArrayXD &);
    };

    /*
     * The functions below pertains to creating a custom OWL::ArrayXD
     */
    ArrayXD Zeros(int len = 50);
    ArrayXD Ones(int len = 50);
    ArrayXD aRange(double start, double end, double dx);
    ArrayXD LinSpaced(double startDouble, double endDouble, int length = 50);

    /*
     * The functions below pertains to performing element-by-element math operatons on OWL::ArrayXD
     */

    ArrayXD abs(ArrayXD &);

    // trig functions
    ArrayXD sin(ArrayXD &);
    ArrayXD cos(ArrayXD &);
    ArrayXD tan(ArrayXD &);
    ArrayXD asin(ArrayXD &);
    ArrayXD acos(ArrayXD &);
    ArrayXD atan(ArrayXD &);

    // exponential and log functions
    ArrayXD exp(ArrayXD &);
    ArrayXD log10(ArrayXD &);
    ArrayXD ln(ArrayXD &);

    /*
    Functions below pertains to operations on two OWL::ArrayXD
    */
    ArrayXD append(ArrayXD &, ArrayXD &);

    /*
     * Classes to handle exceptions for OWL::MatrixXD
     */

    /**
     * DiffArrayLengthsException
     *
     * Exception when the arrays have different lengths.
     */
    class DiffArrayLengthsException : public std::exception
    {
    public:
        const char *what() { return "Empty Array"; }
    };

    /**
     * RowIndexExceedRowSizeException
     *
     * Exception when the index called is greater than the matrix row size.
     */
    class RowIndexExceedRowSizeException : public std::exception
    {
    public:
        const char *what() { return "Empty Array"; }
    };

    /**
     * class to handle matrix with elements of type double and size m*n
     */
    class MatrixXD
    {
    public:
        // Constructors
        MatrixXD();
        MatrixXD(std::vector<ArrayXD> inputElements);
        MatrixXD(const int, const int);
        // Getter functions
        int getRowSize() { return m; };
        int getColSize() { return n; };
        std::vector<ArrayXD> getElements() { return elements; };
        // operator overloads
        OWL::ArrayXD &operator[](int rowIndex)
        {
            if (rowIndex > (m - 1))
            {
                throw RowIndexExceedRowSizeException();
            }
            return elements[rowIndex];
        }
        void operator<<(OWL::ArrayXD inputRow)
        {
            elements.push_back(inputRow);
            m = findRowSize();
            n = findColSize();
        }
        MatrixXD operator+(MatrixXD &);
        MatrixXD operator-(MatrixXD &);
        MatrixXD operator*(MatrixXD &);
        // Auxiliary Functions
        bool compareSize(MatrixXD &);
        OWL::ArrayXD getCol(int);
        bool isSquare()
        {
            bool flag = false;
            if (n == m)
            {
                flag = true;
            }
            return flag;
        }
        bool isSingular()
        {
            double detVal = det();
            if (detVal == 0.0)
            {
                return true;
            }
            else
            {
                return false;
            }
        }
        // Matrix operations
        void T();
        MatrixXD submatrix(int, int);
        double det();

    private:
        std::vector<ArrayXD> elements; // a vector of columns containing a OWL::ArrayXD as rows.
        int m;                         /**< number of rows */
        int n;                         /**< number of columns */
        int findRowSize();
        int findColSize();
        bool checkEmptyArrays();
    };

    /*
     * The functions below pertains to creating a custom OWL::MatrixXD
     */

    /**
     * Zeros
     *
     * Returns a matrix with all elements equal to zero.
     *
     * Parameters:
     *     rowLen: (int) row length
     *     colLen: (int) row length
     *
     * Return:
     *     (OWL::MatrixXD) Matrix with all elements equal to zero.
     *
     * Throws:
     *     None
     */
    MatrixXD Zeros(int, int);

    /**
     * Ones
     *
     * Returns a matrix with all elements equal to one.
     *
     * Parameters:
     *     rowLen: (int) row length
     *     colLen: (int) row length
     *
     * Return:
     *     (OWL::MatrixXD) Matrix with all elements equal to one.
     *
     * Throws:
     *     None
     */
    MatrixXD Ones(int, int);

    /**
     * Diagnal
     *
     * Returns a diagnal matrix.
     *
     * Parameters:
     *     len: (int) length of the matrix
     *
     * Return:
     *     (OWL::MatrixXD) Squre diagnal matrix.
     *
     * Throws:
     *     None
     */
    MatrixXD Diag(int);
}

/*
 * Functions below pertains to operator overloads free functions
 */
OWL::ArrayXD operator+(double, OWL::ArrayXD);
OWL::ArrayXD operator*(double lhsScalar, OWL::ArrayXD rhsArray);

namespace Newton
{
    namespace interp
    {
        /**
         * Class to handle exceptions when the interpolation limts are exceeded.
         */
        class ExceedInterpolateLimit : public std::exception
        {
        public:
            const char *what();
        };

        double slope(double &y2, double &y1, double &x2, double &x1);
        std::function<double(double)> line(double &slope, double &x, double &y);
        double interp(OWL::ArrayXD xArray, OWL::ArrayXD yArray, double x);
        std::function<double(double)> interpFunc(OWL::ArrayXD xArray, OWL::ArrayXD yArray);
    }

    namespace ODESolver
    {
        double Euler(const double x_prev, const double y_prev, const double step_size, double (*func)(double, double));
        double Euler(const double y_prev, const double step_size, double func_value);
        OWL::ArrayXD Euler(OWL::ArrayXD xArray, double yInit, double (*func)(double, double));

        double rk4(const double x_prev, const double y_prev, const double step_size, double (*func)(double x, double y));
        double rk4(const double x_prev, const double y_prev, const double step_size, std::function<double(double, double)> func);
        OWL::ArrayXD rk4(OWL::ArrayXD xArray, double yInit, double (*func)(double, double));
    }

    namespace roots
    {
        // double Brent(double (*func)(double), double lower_bound, double upper_bound, double TOL, double MAX_ITER);
        double Brent(std::function<double(double)> func, double lower_bound, double upper_bound, double TOL, double MAX_ITER);
    }

    namespace MatrixSolvers
    {
        /**
         * @brief Thomas Algorithm source https://www.quantstart.com/articles/Tridiagonal-Matrix-Algorithm-Thomas-Algorithm-in-C/
         *
         * @param l_diag
         * @param diag
         * @param u_diag
         * @param col_vec
         * @return std::vector<double>
         */
        std::vector<double> TDMASolver(std::vector<double> l_diag, std::vector<double> diag, std::vector<double> u_diag, std::vector<double> col_vec);
    }
}

#endif // BMSLOGIC_OWL_H