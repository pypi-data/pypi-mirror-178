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

#include "helper.hpp"

namespace themachinethatgoesping {
namespace tools {
namespace rotationfunctions {

/**
 * @brief create an eigen quaternion by rotating yaw (z axis), pitch (y axis) and roll (x axis)
 *
 * @tparam floattype
 * @param ypr array that contains yaw, pitch and roll value
 * @param input_in_degrees if true, yaw pitch and roll input values are in ° otherwise rad
 * @return Eigen::Quaternion<floattype>
 */
template<typename floattype>
Eigen::Quaternion<floattype> quaternion_from_ypr(std::array<floattype, 3> ypr,
                                                 bool                     input_in_degrees = true)
{
    static const floattype _quaternion_from_ypr_to_rad = M_PI / 180.;

    // check if values are valid
    if (!std::isfinite(ypr[0]) || !std::isfinite(ypr[1]) || !std::isfinite(ypr[2]))
    {
        throw std::invalid_argument(
            "ERROR[quaternion_from_ypr]: NAN or INFINITY yaw, pitch or roll value!");
    }

    // convert to rad
    if (input_in_degrees)
    {
        ypr[0] *= _quaternion_from_ypr_to_rad;
        ypr[1] *= _quaternion_from_ypr_to_rad;
        ypr[2] *= _quaternion_from_ypr_to_rad;
    }

    // create quaternion by rotating around axes first, yaw, then pitch, then roll
    Eigen::Quaternion<floattype> q =
        Eigen::AngleAxis<floattype>(ypr[0], Eigen::Matrix<floattype, 1, 3>::UnitZ()) *
        Eigen::AngleAxis<floattype>(ypr[1], Eigen::Matrix<floattype, 1, 3>::UnitY()) *
        Eigen::AngleAxis<floattype>(ypr[2], Eigen::Matrix<floattype, 1, 3>::UnitX());

    // normalize quaternion
    q.normalize();

    return q;
}

/**
 * @brief create an eigen quaternion by rotating yaw (z axis), pitch (y axis) and roll (x axis)
 *
 * @tparam floattype floating point value
 * @param yaw rotation around z axis [° or rad]
 * @param pitch rotation around y axis [° or rad]
 * @param roll rotation around x axis [° or rad]
 * @param input_in_degrees if true, yaw pitch and roll input values are in ° otherwise rad
 * @return Eigen::Quaternion<floattype>
 */
template<typename floattype>
Eigen::Quaternion<floattype> quaternion_from_ypr(floattype yaw,
                                                 floattype pitch,
                                                 floattype roll,
                                                 bool      input_in_degrees = true)
{
    std::array<floattype, 3> ypr = { yaw, pitch, roll };

    return quaternion_from_ypr(std::move(ypr), input_in_degrees);
}

/**
 * @brief Convert quaternion to yaw, pitch and roll
 *
 * @tparam floattype
 * @param q quaternion
 * @param output_to_degrees  if true, yaw pitch and roll input values are in ° otherwise rad
 * @return std::array<floattype, 3> yaw, pitch and roll
 */
template<typename floattype>
std::array<floattype, 3> ypr_from_quaternion(Eigen::Quaternion<floattype> q,
                                             bool                         output_to_degrees = true)
{
    q.normalize();

    auto                     Me  = q.toRotationMatrix().eulerAngles(2, 1, 0);
    std::array<floattype, 3> ypr = { Me[0], Me[1], Me[2] };

    /* pitch is constrained to -90° -> 89.9999°
     * otherwise there is two possibilities to reach every point.
     * because: rotate(yaw,pitch,roll) == rotate(yaw+pi,pi-pitch,roll+pi)
     * Also note: pitch = 90 degrees leads to a gimbal lock situation
     */
    ypr = normalize_angles_rad(ypr);

    static const floattype _ypr_from_quaternion_to_degrees = 180 / M_PI;
    if (output_to_degrees)
    {
        ypr[0] *= _ypr_from_quaternion_to_degrees;
        ypr[1] *= _ypr_from_quaternion_to_degrees;
        ypr[2] *= _ypr_from_quaternion_to_degrees;
    }

    return ypr;
}

// --- vectorized calls ---

/**
 * @brief create eigen quaternions by rotating yaw (z axis), pitch (y axis) and roll (x axis) values
 * (vectorized call)
 *
 * @tparam floattype floating point value
 * @param YPR vector of yaw, pitch and roll rotation values [° or rad]
 * @param input_in_degrees if true, yaw pitch and roll input values are in ° otherwise rad
 * @return std::vector<Eigen::Quaternion<floattype>>
 */
template<typename floattype>
std::vector<Eigen::Quaternion<floattype>> quaternion_from_ypr(
    const std::vector<std::array<floattype, 3>>& YPR,
    bool                                         input_in_degrees = true)
{
    std::vector<Eigen::Quaternion<floattype>> Q;
    Q.reserve(YPR.size());
    for (const auto ypr : YPR)
    {
        Q.push_back(quaternion_from_ypr(ypr, input_in_degrees));
    }

    return Q;
}

/**
 * @brief create eigen quaternions by rotating yaw (z axis), pitch (y axis) and roll (x axis) values
 * (vectorized call)
 *
 * @tparam floattype
 * @tparam floattype floating point value
 * @param yaw vector of rotation values around the z axis [° or rad]
 * @param pitch vector of rotation values the y axis [° or rad]
 * @param roll of rotation values the x axis [° or rad]
 * @param input_in_degrees if true, yaw pitch and roll input values are in ° otherwise rad
 * @return std::vector<Eigen::Quaternion<floattype>>
 */
template<typename floattype>
std::vector<Eigen::Quaternion<floattype>> quaternion_from_ypr(const std::vector<floattype>& yaw,
                                                              const std::vector<floattype>& pitch,
                                                              const std::vector<floattype>& roll,
                                                              bool input_in_degrees = true)
{
    if (yaw.size() != pitch.size() || yaw.size() != roll.size())
    {
        throw std::invalid_argument(
            "ERROR[quaternion_from_ypr]: input vectors must have the same size!");
    }

    std::vector<Eigen::Quaternion<floattype>> Q;
    Q.reserve(yaw.size());
    for (unsigned int i = 0; i < yaw.size(); ++i)
    {
        Q.push_back(quaternion_from_ypr(yaw[i], pitch[i], roll[i], input_in_degrees));
    }

    return Q;
}

/**
 * @brief Convert quaternions to yaw, pitch and roll values (vectorized call)
 *
 * @tparam floattype
 * @param Q vector of quaternions
 * @param output_to_degrees  if true, yaw pitch and roll input values are in ° otherwise rad
 * @return std::vector<std::array<floattype, 3>>
 */
template<typename floattype>
std::vector<std::array<floattype, 3>> ypr_from_quaternion(
    const std::vector<Eigen::Quaternion<floattype>>& Q,
    bool                                             output_to_degrees = true)
{
    std::vector<std::array<floattype, 3>> YPR;
    YPR.resize(Q.size());

    for (unsigned int i = 0; i < Q.size(); ++i)
    {
        YPR[i] = ypr_from_quaternion(Q[i], output_to_degrees);
    }

    return YPR;
}

/// ---- untested ////
/**
 * @brief get_quaterniond_from_vector: creates a Quaternion that holds the passed
 * parameters x,y,z as a Vector
 * @param x: x as double or float
 * @param y: y as double or float
 * @param z: z as double or float
 * @param w: w as double or float with the default value 0.0
 * @return returns the Quaternion that holds a vector
 */
template<typename floattype>
Eigen::Quaternion<floattype> get_quaterniond_from_vector(floattype x,
                                                         floattype y,
                                                         floattype z,
                                                         floattype w = 0.0)
{
    Eigen::Vector3<floattype>    vec_to_rotate(x, y, z);
    Eigen::Quaternion<floattype> vec_to_rotate_as_quat;
    vec_to_rotate_as_quat.w()   = w;
    vec_to_rotate_as_quat.vec() = vec_to_rotate;
    return vec_to_rotate_as_quat;
}

/**
 * @brief get_quaterniond_from_vector: creates a Quaternion that holds the passed
 * parameters x,y,z as a Vector
 * @param xyz: x, y, z as Array<floattype, 3>
 * @param w: w as double or float with the default value 0.0
 * @return returns the Quaternion that holds a vector
 */
template<typename floattype>
Eigen::Quaternion<floattype> get_quaterniond_from_vector(const std::array<floattype, 3>& xyz,
                                                         const floattype                 w = 0.0)
{
    return get_quaterniond_from_vector(xyz[0], xyz[1], xyz[2], w);
}

template<typename floattype>
std::vector<floattype> get_quaternion_wxyz(const Eigen::Quaternion<floattype>& q)
{
    return { q.w(), q.x(), q.y(), q.z() };
}

/**
 * @brief OVERLOADED rotateXYZ: rotates a x,y,z vector with the passed
 * parameters roll, pitch, yaw as a Quaternion
 * @param q: roll, pitch, yaw as Quaternion<floattype>
 * @param x: x as double
 * @param y: y as double
 * @param z: z as double
 * @return returns vector with rotated xyz
 */
template<typename floattype>
Eigen::Vector3d rotateXYZ(Eigen::Quaternion<floattype> q, floattype x, floattype y, floattype z)
{
    q.normalize();

    Eigen::Quaternion<floattype> vec_to_rotate_as_quat = get_quaterniond_from_vector(x, y, z);

    Eigen::Quaternion<floattype> rotated_quaternion = q * vec_to_rotate_as_quat * q.inverse();

    Eigen::Vector3d rotatedV = rotated_quaternion.vec();

    return rotatedV;
}

/**
 * @brief OVERLOADED rotateXYZ: rotates a x,y,z vector as a Quaternion with the
 * passed parameters roll, pitch, yaw as a Quaternion
 * @param q: roll, pitch, yaw as Quaternion<floattype>
 * @param v: x, y, z as Quaternion<floattype>
 * @return returns vector with rotated xyz
 */
template<typename floattype>
Eigen::Vector3d rotateXYZ(Eigen::Quaternion<floattype> q, Eigen::Quaternion<floattype> v)
{
    q.normalize();

    Eigen::Quaternion<floattype> rotated_quaternion = q * v * q.inverse();

    Eigen::Vector3d rotatedV = rotated_quaternion.vec();

    return rotatedV;
}

} // namespace rotationfunctions
} // namespace tools
} // namespace themachinethatgoesping
