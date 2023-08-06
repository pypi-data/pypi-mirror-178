// Kiel SPDX-FileCopyrightText: 2022 Peter Urban, Ghent University
//
// SPDX-License-Identifier: MPL-2.0

#pragma once

#include <bitsery/ext/inheritance.h>

#include <GeographicLib/UTMUPS.hpp>

#include <themachinethatgoesping/tools/classhelper/bitsery.hpp>
#include <themachinethatgoesping/tools/classhelper/objectprinter.hpp>
#include <themachinethatgoesping/tools/helper.hpp>
#include <themachinethatgoesping/tools/rotationfunctions/quaternions.hpp>

#include "../navtools.hpp"
#include "sensordata.hpp"

namespace themachinethatgoesping {
namespace navigation {
namespace datastructures {

/**
 * @brief A structure to store a georeferenced data and attitude data from different sensors
 * (e.g. GPS, IMU, etc.)
 * Unlike SensorDataUTM, this structure stores coordinates without zone and hemisphere information.
 *
 */
struct SensorDataLocal : public SensorData
{
    double northing = 0.0; ///< in m, positive northwards
    double easting  = 0.0; ///< in m, positive eastwards

    /**
     * @brief Construct a new Sensor Position object (all offsets set to 0)
     *
     */
    SensorDataLocal() = default;

    /**
     * @brief Construct a new Sensor Data Local object using a base sensor data object
     *
     * @param data
     * @param northing in m, positive northwards
     * @param easting in m, positive eastwards
     */
    SensorDataLocal(const SensorData& data, double northing, double easting)
        : SensorData(data)
        , northing(northing)
        , easting(easting)
    {
    }

    /**
     * @brief Construct a new SensorDataLocal object
     *
     * @param northing in m, positive northwards
     * @param easting in m, positive eastwards
     * @param depth in m, positive downwards
     * @param heave from heave sensor, will be added to depth in m, positive upwards
     * @param heading in °, 0° is north, 90° is east
     * @param pitch in °, positive means bow up
     * @param roll in °, positive means port up
     */
    SensorDataLocal(double northing,
                    double easting,
                    double depth,
                    double heave,
                    double heading,
                    double pitch,
                    double roll)
        : SensorData(depth, heave, heading, pitch, roll)
        , northing(northing)
        , easting(easting)
    {
    }

    bool operator!=(const SensorDataLocal& rhs) const { return !(operator==(rhs)); }
    /**
     * @brief Check if two SensorDataLocal objects are equal
     *
     * @param rhs
     * @return true if equal
     * @return false if not equal
     */
    bool operator==(const SensorDataLocal& rhs) const
    {
        if (SensorData::operator==(rhs))
            if (tools::helper::approx(northing, rhs.northing))
                if (tools::helper::approx(easting, rhs.easting))
                    return true;

        return false;
    }

  private:
    // serialization support using bitsery
    friend bitsery::Access;
    template<typename S>
    void serialize(S& s)
    {
        s.ext(*this, bitsery::ext::BaseClass<SensorData>{});
        s.value8b(northing);
        s.value8b(easting);
    }

  public:
    tools::classhelper::ObjectPrinter __printer__(unsigned int float_precision) const
    {
        tools::classhelper::ObjectPrinter printer("SensorDataLocal", float_precision);

        printer.register_value("northing", northing, "positive northwards, m");
        printer.register_value("easting", easting, "positive eastwards, m");

        printer.append(SensorData::__printer__(float_precision));

        return printer;
    }

  public:
    // -- class helper function macros --
    // define to_binary and from_binary functions (needs the serialization function)
    __BITSERY_DEFAULT_TOFROM_BINARY_FUNCTIONS__(SensorDataLocal)
    // define info_string and print functions (needs the __printer__ function)
    __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__
};

} // namespace datastructures
} // namespace navigation
} // namespace themachinethatgoesping