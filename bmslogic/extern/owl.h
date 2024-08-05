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
#include <algorithm>
#include <functional>

namespace OWL
{

    /**
     * @brief Custom Exception class to handle situations when OWL::ArrayXd array lengths/sizes do not match up.
     *
     */
    class SizeMismatchException : public std::exception
    {
    public:
        const char *what() { return "ArrayXD lengths do not match."; };
    };

    /**
     * @brief Custom Exception class to handle situations when operations are required but the array is empty.
     *
     */
    class EmptyArrayException : public std::exception
    {
    public:
        const char *what() { return "Empty Array!"; }
    };

    /**
     *
     * @brief Provides functionality for the array operations. It uses the C++ vectors from the C++ standard Library
     * (std::vector) to create, store, and index element values.
     *
     */
    class ArrayXD
    {
    public:
        ArrayXD();
        ArrayXD(std::vector<double> &vec);
        ~ArrayXD() {};
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
     * @brief Exception when the arrays have different lengths.
     * 
     */
    class DiffArrayLengthsException : public std::exception
    {
    public:
        const char *what() { return "Empty Array"; }
    };

    /**
     * @brief Exception when the index called is greater than the matrix row size.
     * 
     */
    class RowIndexExceedRowSizeException : public std::exception
    {
    public:
        const char *what() { return "Empty Array"; }
    };


    /**
     * @brief Class to handle matrix with elements of type double and size m*n. 
     * 
     * It uses C++ standard vectors for creating, storing, and indexing matrix element values.
     * 
     */
    class MatrixXD
    {
    public:
        // Constructors
        MatrixXD();
        MatrixXD(std::vector<ArrayXD> inputElements);
        MatrixXD(const int, const int);
        ~MatrixXD() {};
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
        double operator()(int idx_row, int idx_col)
        {
            if ((idx_row > m) || (idx_col > n))
                throw std::exception();
            return elements[idx_row][idx_col];
        }
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

    /**
     * @brief Returns a matrix with all elements equal to zero.
     *
     * @param n_row number of desired rows.
     * @param n_col number of desired columns.
     *
     * @return MatrixXD
     */
    MatrixXD Zeros(int, int);

    /**
     * @brief Return an instance of OWL::MatrixXD with all elements equal to one.
     *
     * @param n_row desired row length.
     * @param n_col desired column length
     *
     * @return OWL::MatrixXD instance with all elements equal to one.
     */
    MatrixXD Ones(int n_row, int n_col);

    /**
     * @brief Returns a diagnal matrix, where the diagonal elements are equal to 1.
     *
     * @param len_row integeter containing the length of the square matrix
     *
     * @return a MatrixXD instance containing the diagonal elements as 1.
     */
    MatrixXD Diag(int len_row);
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
         * @brief Class to handle exceptions when the interpolation limts are exceeded.
         *
         */
        class ExceedInterpolateLimit : public std::exception
        {
        public:
            const char *what();
        };

        [[nodiscard]] double slope(double &y2, double &y1, double &x2, double &x1);
        [[nodiscard]] std::function<double(double)> line(double &slope, double &x, double &y);
        [[nodiscard]] double interp(OWL::ArrayXD xArray, OWL::ArrayXD yArray, double x);
        [[nodiscard]] std::function<double(double)> interpFunc(OWL::ArrayXD xArray, OWL::ArrayXD yArray);
        [[nodiscard]] double linear_interpolation(double x, std::vector<double> vec_x, std::vector<double> vec_y);
        [[nodiscard]] long double linear_interpolation(long double x, std::vector<long double> vec_x, std::vector<long double> vec_y);
        [[nodiscard]] std::vector<double> linear_interpolation(std::vector<double> target_vec_x, std::vector<double> vec_x, std::vector<double> vec_y);
        [[nodiscard]] std::vector<long double> linear_interpolation(std::vector<long double> target_vec_x, std::vector<long double> vec_x, std::vector<long double> vec_y);
    }

    namespace ODESolver
    {
        [[nodiscard]] double Euler(const double x_prev, const double y_prev, const double step_size, double (*func)(double, double));
        [[nodiscard]] double Euler(const double y_prev, const double step_size, double func_value);
        [[nodiscard]] OWL::ArrayXD Euler(OWL::ArrayXD xArray, double yInit, double (*func)(double, double));
        [[nodiscard]]

        [[nodiscard]] double
        rk4(const double x_prev, const double y_prev, const double step_size, double (*func)(double x, double y));
        [[nodiscard]] double rk4(const double x_prev, const double y_prev, const double step_size, std::function<double(double, double)> func);
        [[nodiscard]] OWL::ArrayXD rk4(OWL::ArrayXD xArray, double yInit, double (*func)(double, double));
    }

    namespace roots
    {
        /**
         * @brief Finds the roots using Brent's method. Code from the internet.
         *
         * @param func
         * @param lower_bound lower bound of the bracket
         * @param upper_bound upper bound of the bracket
         * @param TOL tolerance
         * @param MAX_ITER maximum allowed iterations
         *
         * @return double containing the root.
         */
        [[nodiscard]] double Brent(std::function<double(double)> func, double lower_bound, double upper_bound, double TOL, double MAX_ITER);
    }

    namespace MatrixSolvers
    {
        /**
         * @brief Thomas Algorithm for solving system of equtions that contain diagonally dominant tridiagonal matrix.
         *
         * The matrix is assumed to be square with the size of N x N.
         * code source from https://www.quantstart.com/articles/Tridiagonal-Matrix-Algorithm-Thomas-Algorithm-in-C/
         *
         * @param l_diag C++ vector containing the lower diagonal elements of length N-1
         * @param diag C++ vector containing the diagonal elements of length N
         * @param u_diag C++ vector containing the upper diagonal elements of length N+1
         * @param col_vec C++ vector containing the RHS column vector.
         *
         * @return a C++ vector containing the solution of size N
         */
        [[nodiscard]] std::vector<double> TDMASolver(std::vector<double> l_diag, std::vector<double> diag, std::vector<double> u_diag, std::vector<double> col_vec);
    }
}

#endif // BMSLOGIC_OWL_H