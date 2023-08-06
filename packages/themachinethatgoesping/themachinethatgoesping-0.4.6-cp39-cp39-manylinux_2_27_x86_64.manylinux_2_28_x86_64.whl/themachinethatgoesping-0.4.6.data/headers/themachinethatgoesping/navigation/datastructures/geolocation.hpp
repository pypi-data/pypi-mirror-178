// Kiel SPDX-FileCopyrightText: 2022 Peter Urban, Ghent University
//
// SPDX-License-Identifier: MPL-2.0

#pragma once

#include <GeographicLib/Geocentric.hpp>
#include <GeographicLib/Geodesic.hpp>
#include <GeographicLib/LocalCartesian.hpp>

#include <themachinethatgoesping/tools/classhelper/bitsery.hpp>
#include <themachinethatgoesping/tools/classhelper/objectprinter.hpp>
#include <themachinethatgoesping/tools/helper.hpp>
#include <themachinethatgoesping/tools/rotationfunctions/quaternions.hpp>

#include "../navtools.hpp"

namespace themachinethatgoesping {
namespace navigation {
namespace datastructures {

/**
 * @brief A structure to store a georeferenced location and attitude (e.g. of a sensor)
 * This structure does not store any coordinates except the depth (z)
 *
 */
struct GeoLocation
{
    double z     = 0;   ///< in m, positive downwards
    double yaw   = 0.0; ///< in °, 0° is north, 90° is east
    double pitch = 0.0; ///< in °, positive means bow up
    double roll  = 0.0; ///< in °, positive means port up

    /**
     * @brief Construct a new Position object
     *
     */
    GeoLocation() = default;

    /**
     * @brief Construct a new GeoLocation object
     *
     * @param z in m, positive downwards
     * @param yaw in °, 0° is north, 90° is east
     * @param pitch in °, positive means bow up
     * @param roll in °, positive means port up
     */
    GeoLocation(double z, double yaw, double pitch, double roll)
        : z(z)
        , yaw(yaw)
        , pitch(pitch)
        , roll(roll)
    {
    }

    /**
     * @brief Construct a new GeoLocation object from a string
     *
     * @param str string containing the location in the format "latitude,longitude,z,yaw,pitch,roll"
     */
    bool operator!=(const GeoLocation& rhs) const { return !(operator==(rhs)); }

    /**
     * @brief Check if two GeoLocation objects are equal
     *
     * @param rhs
     * @return true if equal
     * @return false if not equal
     */
    bool operator==(const GeoLocation& rhs) const
    {
        if (tools::helper::approx(z, rhs.z))
            if (tools::helper::approx(yaw, rhs.yaw))
                if (tools::helper::approx(pitch, rhs.pitch))
                    if (tools::helper::approx(roll, rhs.roll))
                        return true;

        return false;
    }

  private:
    // serialization support using bitsery
    friend bitsery::Access;
    template<typename S>
    void serialize(S& s)
    {
        s.value8b(z);
        s.value8b(yaw);
        s.value8b(pitch);
        s.value8b(roll);
    }

  public:
    tools::classhelper::ObjectPrinter __printer__(unsigned int float_precision) const
    {
        tools::classhelper::ObjectPrinter printer("GeoLocation", float_precision);

        printer.register_value("z", z, "positive downwards, m");
        printer.register_value("yaw", yaw, "90 ° at east");
        printer.register_value("pitch", pitch, "° positive bow up");
        printer.register_value("roll", roll, "° positive port up");

        return printer;
    }

  public:
    // -- class helper function macros --
    // define to_binary and from_binary functions (needs the serialize function)
    __BITSERY_DEFAULT_TOFROM_BINARY_FUNCTIONS__(GeoLocation)
    // define info_string and print functions (needs the __printer__ function)
    __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__
};

} // namespace datastructures
} // namespace navigation
} // namespace themachinethatgoesping