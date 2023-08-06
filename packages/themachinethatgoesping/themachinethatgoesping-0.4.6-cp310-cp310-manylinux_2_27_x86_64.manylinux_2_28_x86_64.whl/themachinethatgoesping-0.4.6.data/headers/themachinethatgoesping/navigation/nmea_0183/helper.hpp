// SPDX-FileCopyrightText: 2022 Peter Urban, Tim Weiß, GEOMAR Helmholtz Centre for Ocean
// Research Kiel SPDX-FileCopyrightText: 2022 Peter Urban, Ghent University
//
// SPDX-License-Identifier: MPL-2.0

#pragma once

#include <charconv>
#include <string>

#include <themachinethatgoesping/tools/classhelper/objectprinter.hpp>
#include <themachinethatgoesping/tools/helper.hpp>
#include <themachinethatgoesping/tools/timeconv.hpp>

#include "../navtools.hpp"

namespace themachinethatgoesping {
namespace navigation {
namespace nmea_0183 {

/**
 * @brief convert dddd.mm to double
 * (this is the format used in NMEA 0183)
 *
 * @param field
 * @return double
 */
inline double nmea_latitude_field_to_double(std::string_view field)
{
    using themachinethatgoesping::tools::helper::string_to_double;

    if (field.size() < 4)
    {
        return std::numeric_limits<double>::quiet_NaN();
    }

    double degrees = string_to_double(field.substr(0, 2));
    double minutes = string_to_double(field.substr(2, field.size() - 2));

    return degrees + minutes / 60;
}

/**
 * @brief convert dddmm.mm to double
 * (this is the format used in NMEA 0183)
 *
 * @param field
 * @return double
 */
inline double nmea_longitude_field_to_double(std::string_view field)
{
    using themachinethatgoesping::tools::helper::string_to_double;

    if (field.size() < 5)
    {
        return std::numeric_limits<double>::quiet_NaN();
    }

    double degrees = string_to_double(field.substr(0, 3));
    double minutes = string_to_double(field.substr(3, field.size() - 3));

    return degrees + minutes / 60;
}

} // nmea_0183
} // namespace navigation
} // namespace themachinethatgoesping
