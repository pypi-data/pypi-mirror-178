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
#include "positionaloffsets.hpp"

namespace themachinethatgoesping {
namespace navigation {
namespace datastructures {

/**
 * @brief A structure to store a georeferenced location and attitude data from different sensors
 * (e.g. IMU, etc.)
 * No gps coordinates are stored in this structure (only depth).
 *
 */
struct SensorData
{
    double depth   = 0.0; ///< in m, positive downwards
    double heave   = 0.0; ///< from heave source, will be added to depth in m, positive upwards
    double heading = 0.0; ///< from heading source in °, 0° is north, 90° is east
    double pitch   = 0.0; ///< from attitude source, in °, positive means bow up
    double roll    = 0.0; ///< from attitude source, in °, positive means port up

    /**
     * @brief Construct a new SensorData object
     *
     */
    SensorData() = default;

    /**
     * @brief Construct a new SensorData object
     *
     * @param depth from depth source, in m, positive downwards
     * @param heave from heave sensor, will be added to depth in m, positive upwards
     * @param heading from heading source, in °, 0° is north, 90° is east
     * @param pitch from attitude source, in °, positive means bow up
     * @param roll from attitude source, in °, positive means port up
     */
    SensorData(double depth, double heave, double heading, double pitch, double roll)
        : depth(depth)
        , heave(heave)
        , heading(heading)
        , pitch(pitch)
        , roll(roll)
    {
    }

    bool operator!=(const SensorData& rhs) const { return !(operator==(rhs)); }
    /**
     * @brief Check if two SensorData objects are equal
     *
     * @param rhs
     * @return true if equal
     * @return false if not equal
     */
    bool operator==(const SensorData& rhs) const
    {
        if (tools::helper::approx(depth, rhs.depth))
            if (tools::helper::approx(heave, rhs.heave))
                if (tools::helper::approx(heading, rhs.heading))
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
        s.value8b(depth);
        s.value8b(heave);
        s.value8b(heading);
        s.value8b(pitch);
        s.value8b(roll);
    }

  public:
    tools::classhelper::ObjectPrinter __printer__(unsigned int float_precision) const
    {
        tools::classhelper::ObjectPrinter printer("SensorData", float_precision);

        printer.register_value("depth", depth, "positive downwards, m");
        printer.register_value("heave", heave, "positive upwards, m");
        printer.register_value("heading", heading, "0° is north, 90 ° is east");
        printer.register_value("pitch", pitch, "° positive bow up");
        printer.register_value("roll", roll, "° positive port up");

        return printer;
    }

  public:
    // -- class helper function macros --
    // define to_binary and from_binary functions (needs the serialization function)
    __BITSERY_DEFAULT_TOFROM_BINARY_FUNCTIONS__(SensorData)
    // define info_string and print functions (needs the __printer__ function)
    __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__
};

} // namespace datastructures
} // namespace navigation
} // namespace themachinethatgoesping