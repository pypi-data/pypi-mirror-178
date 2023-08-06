// SPDX-FileCopyrightText: 2022 Peter Urban, Sven Schorge, GEOMAR Helmholtz Centre for Ocean
// Research Kiel
// SPDX-FileCopyrightText: 2022 Peter Urban, Ghent University
//
// SPDX-License-Identifier: MPL-2.0

/**
 * @brief some convenience functions to create eigen quaternions from yaw pitch
 * roll values using eigen rotations Note: Rotations are created in the
 * following order: 1. yaw, 2. pitch, 3. roll
 *
 * @authors Peter Urban, Sven Schorge
 */

#pragma once

//#define _USE_MATH_DEFINES // for C++ // windows // this is not necessary
#include <cmath>

#include <Eigen/Eigen>
#include <Eigen/Geometry>
#include <array>
#include <boost/algorithm/string.hpp>
#include <iostream>
#include <tuple>
#include <unordered_map>
#include <vector>

namespace themachinethatgoesping {
namespace tools {
namespace rotationfunctions {

/**
 * @brief Shift angles into specified angular range: yaw [0,2pi], pitch [-p/2°, p/2°], roll [-pi,
 * pi]
 *
 * @tparam floattype double or gloat
 * @param ypr Matrix with yaw, pitch and roll value in rad
 * @return std::array<floattype, 3> (Matrix with yaw, pitch and roll value in rad)
 */
template<typename floattype>
std::array<floattype, 3> normalize_angles_rad(std::array<floattype, 3> ypr)
{
    /* pitch is constrained to -90° -> 90°
     * otherwise there is two possibilities to reach every point.
     * because: rotate(yaw,pitch,roll) == rotate(yaw+pi,pi-pitch,roll+pi)
     * Also note: pitch = 90 degrees leads to a gimbal lock situation
     */
    static const floattype M_2PI    = 2. * M_PI;
    static const floattype M_PI_3_2 = M_PI_2 * 3.;

    while (ypr[1] > M_PI_3_2)
    {
        ypr[1] -= M_2PI;
    }
    while (ypr[1] < -M_PI_2)
    {
        ypr[1] += 2 * M_PI;
    }
    while (ypr[1] > M_PI_2)
    {
        ypr[0] -= M_PI;
        ypr[1] = M_PI - ypr[1];
        ypr[2] -= M_PI;
    }

    // roll is defined within -180° -> +179.0000 or +- pi
    while (ypr[2] < M_PI)
        ypr[2] += M_2PI;
    while (ypr[2] >= M_PI)
        ypr[2] -= M_2PI;

    // yaw is defined within 0 - 359.9999 ° or 0 - 2pi
    while (ypr[0] < 0)
        ypr[0] += M_2PI;
    while (ypr[0] >= M_2PI)
        ypr[0] -= M_2PI;

    return ypr;
}

/**
 * @brief Shift angles into specified angular range: yaw [0°,359.99°], pitch [-90°, 90°], roll
 * [-180¶, 179.99°]
 *
 * @tparam floattype double or gloat
 * @param ypr Matrix with yaw, pitch and roll value in °
 * @return std::array<floattype, 3> (Matrix with yaw, pitch and roll value in °)
 */
template<typename floattype>
std::array<floattype, 3> normalize_angles_degrees(std::array<floattype, 3> ypr)
{
    //

    /* pitch is constrained to -90° -> 90°
     * otherwise there is two possibilities to reach every point.
     * because: rotate(yaw,pitch,roll) == rotate(yaw+pi,pi-pitch,roll+pi)
     * Also note: pitch = 90 degrees leads to a gimbal lock situation
     */
    while (ypr[1] > 270.)
    {
        ypr[1] -= 360.;
    }
    while (ypr[1] < -90.)
    {
        ypr[1] += 360.;
    }
    while (ypr[1] > 90.)
    {
        ypr[0] -= 180.;
        ypr[1] = 180. - ypr[1];
        ypr[2] -= 180.;
    }

    // roll is defined within -180° -> +179.999 or +- pi
    while (ypr[2] < 180.)
        ypr[2] += 360.;
    while (ypr[2] >= 180.)
        ypr[2] -= 360.;

    // yaw is defined within 0 - 359.9999 ° or 0 - 2pi
    while (ypr[0] < 0)
        ypr[0] += 360.;
    while (ypr[0] >= 360.)
        ypr[0] -= 360.;

    return ypr;
}

/**
 * @brief compute heading from northing and easting
 * north 0°/360°, east 90°, south 180°, west 270
 *
 * @param northing northing in m
 * @param easting easting in m
 * @param radians return as rad, otherwise as degrees
 * @return heading in rad or degrees
 */
inline double compute_heading(double northing, double easting, bool radians = false)
{
    double heading = atan2(easting, northing);
    if (heading < 0)
        heading += 2 * M_PI;

    if (!radians)
        heading *= 180. / M_PI;

    return heading;
}

} // namespace rotationfunctions
} // namespace tools
} // namespace themachinethatgoesping
