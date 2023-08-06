// SPDX-FileCopyrightText: 2022 Peter Urban, Ghent University
//
// SPDX-License-Identifier: MPL-2.0

#pragma once

// include bitsery
#include <bitsery/bitsery.h>

// helper
#include "helper.hpp"

// eigen quaternions
#include <Eigen/Eigen>
#include <Eigen/Geometry>

// define quaternion type
using t_quaternion = Eigen::Quaternion<double>;

// define how object should be serialized/deserialized
namespace Eigen {
template<typename S>
void serialize(S& s, Quaterniond& q)
{
    s.value8b(q.w());
    s.value8b(q.x());
    s.value8b(q.y());
    s.value8b(q.z());
}

template<typename S>
void serialize(S& s, Quaternionf& q)
{
    s.value4b(q.w());
    s.value4b(q.x());
    s.value4b(q.y());
    s.value4b(q.z());
}

}