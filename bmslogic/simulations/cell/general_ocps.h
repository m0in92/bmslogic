/**
 * @file general_ocps.h
 * @author Moin Ahmed (moinahmed100@gmail.com)
 * @brief 
 * @version 0.1
 * @date 2024-05-08
 * 
 * @copyright Copyright (c) 2024
 * 
 */

#ifndef BMSLOGIC_PROJECT_GENERAL_OCP_FUNCTIONS_H
#define BMSLOGIC_PROJECT_GENERAL_OCP_FUNCTIONS_H

#include <cmath>
#include <vector>

#include "calc_helpers/constants.h"

namespace positive_electrode_ocps
{
    double calc_ocp_schmit(std::vector<double> &A_list, double &K, double &U0, double &SOC)
    {
        double R = Constants.R;
        double F = Constants.F;
        double temp = 298.15; // [K]

        double sec_term = (R * temp / F) * std::log((1 - SOC) / SOC); // second term

        // the following defines the third term
        double pre_term = 1 / (std::pow(K * (2 * SOC - 1) + 1, 2));
        double post_term = 0;
        for (int i = 0; i < A_list.size(); i++)
        {
            post_term += (A_list[i] / F) * (std::pow(2 * SOC - 1, i + 1) - 2 * i * SOC * (1 - SOC) / std::pow(2 * SOC - 1, 1 - i));
        }
        double third_term = pre_term * post_term;

        // the following defines the fourth term
        post_term = 0;
        for (int i = 0; i < A_list.size(); i++)
            post_term += (A_list[i] / F) * (std::pow(2 * SOC - 1, i) * (2 * (i + 1) * (std::pow(SOC, 2)) - 2 * (i + 1) * SOC + 1));
        double fou_term = K * post_term;

        return U0 + sec_term + third_term + fou_term;
    }

    double LCO(double &SOC)
    {
        std::vector<double> A_list = {5166082.0, -5191279.0, 5232986.0, -5257083.0, 5010583.0, -4520614.0, 7306952.0, -14634260.0, 6705611.0,
                                      33894160.0, -63528110.0, 30487930.0, 21440020.0, -27731990.0, 8206452.0};
        double K = -2.369020e-04;
        double U0 = -2.276828e+01;

        return calc_ocp_schmit(A_list, K, U0, SOC);
    }

    std::vector<double> LCO(std::vector<double> &vector_SOC)
    {
        std::vector<double> result_vector;
        double SOC;
        for (int j = 0; j < vector_SOC.size(); j++)
        {
            SOC = vector_SOC[j];

            result_vector.push_back(LCO(SOC));
        }
        return result_vector;
    }

    double NMC(double &SOC)
    {
        std::vector<double> A_list = {
            -1306.411,
            -57995.21,
            128590.6,
            -141860.5,
            128196.9,
            -328128.3,
            817.6398,
            1373879,
            651141.4,
            -7315831,
            4983891,
            6925178,
            -6123714,
            -3595215,
            3340694};
        double K = -0.635961;
        double U0 = 3.755472;

        return calc_ocp_schmit(A_list, K, U0, SOC);
    }

    std::vector<double> NMC(std::vector<double> &vector_SOC)
    {
        std::vector<double> result_vector;
        double SOC;
        for (int j = 0; j < vector_SOC.size(); j++)
        {
            SOC = vector_SOC[j];

            result_vector.push_back(NMC(SOC));
        }
        return result_vector;
    }

    double LFP(double &SOC)
    {
        std::vector<double> A_list = {
            -2244.923,
            -2090.675,
            -6045.274,
            -6046.354,
            -13952.1,
            49285.95,
            57688.95,
            -270619.6,
            -262397.3,
            695491.2,
            480539,
            -881803.7,
            -450067.5,
            425577.8,
            127814.6};
        double K = 0.03932999;
        double U0 = 3.407141;

        return calc_ocp_schmit(A_list, K, U0, SOC);
    }

    std::vector<double> LFP(std::vector<double> &vector_SOC)
    {
        std::vector<double> result_vector;
        double SOC;
        for (int j = 0; j < vector_SOC.size(); j++)
        {
            SOC = vector_SOC[j];

            result_vector.push_back(LFP(SOC));
        }
        return result_vector;
    }

    double LMO(double &SOC)
    {
        std::vector<double> A_list = {
            28.88073,
            -19289.65,
            27516.93,
            25997.59,
            47959.29,
            -277348.8,
            -321162.5,
            998439.1,
            1227530,
            -2722189,
            -1973511,
            4613775,
            818839.4,
            -4157314,
            1709075};
        double K = -0.9996536;
        double U0 = 4.004463;

        return calc_ocp_schmit(A_list, K, U0, SOC);
    }

    std::vector<double> LMO(std::vector<double> &vector_SOC)
    {
        std::vector<double> result_vector;
        double SOC;
        for (int j = 0; j < vector_SOC.size(); j++)
        {
            SOC = vector_SOC[j];

            result_vector.push_back(LMO(SOC));
        }
        return result_vector;
    }

    double NCA(double &SOC)
    {
        std::vector<double> A_list = {
            1545979,
            -1598187,
            1595170,
            -1605545,
            1521194,
            -1645695,
            1809373,
            -1578053,
            2032672,
            -2281842,
            -1678912,
            2858489,
            5443521,
            -9459781,
            3600413};
        double K = 0.000104664;
        double U0 = -4.419803;

        return calc_ocp_schmit(A_list, K, U0, SOC);
    }

    std::vector<double> NCA(std::vector<double> &vector_SOC)
    {
        std::vector<double> result_vector;
        double SOC;
        for (int j = 0; j < vector_SOC.size(); j++)
        {
            SOC = vector_SOC[j];

            result_vector.push_back(NCA(SOC));
        }
        return result_vector;
    }
}

namespace negative_electrode_ocps
{
    double graphite(double &SOC)
    {
        return 0.13966 + 0.68920 * std::exp(-49.20361 * SOC) + 0.41903 * std::exp(-254.40067 * SOC) - std::exp(49.97886 * SOC - 43.37888) - 0.028221 * std::atan(22.52300 * SOC - 3.65328) - 0.01308 * std::atan(28.34801 * SOC - 13.43960);
    }

    std::vector<double> graphite(std::vector<double> &vector_SOC)
    {
        std::vector<double> res_vector;

        double SOC;
        for (int i = 0; i < vector_SOC.size(); i++)
        {
            SOC = vector_SOC[i];
            res_vector.push_back(graphite(SOC));
        }
        return res_vector;
    }
}

#endif // BMSLOGIC_PROJECT_GENERAL_OCP_FUNCTIONS_H