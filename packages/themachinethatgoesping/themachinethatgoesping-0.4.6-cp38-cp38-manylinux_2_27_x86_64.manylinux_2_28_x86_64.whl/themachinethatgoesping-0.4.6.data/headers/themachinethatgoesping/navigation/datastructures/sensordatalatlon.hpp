// Kiel SPDX-FileCopyrightText: 2022 Peter Urban, Ghent University
//
// SPDX-License-Identifier: MPL-2.0

#pragma once

#include <bitsery/ext/inheritance.h>

#include <GeographicLib/Geocentric.hpp>
#include <GeographicLib/Geodesic.hpp>
#include <GeographicLib/LocalCartesian.hpp>

#include <themachinethatgoesping/tools/classhelper/bitsery.hpp>
#include <themachinethatgoesping/tools/classhelper/objectprinter.hpp>
#include <themachinethatgoesping/tools/helper.hpp>
#include <themachinethatgoesping/tools/rotationfunctions/quaternions.hpp>

#include "../navtools.hpp"
#include "sensordata.hpp"

namespace themachinethatgoesping {
namespace navigation {
namespace datastructures {

// forward declarations for location conversions
struct SensorDataUTM; // defined in sensordatautm.hpp

/**
 * @brief A structure to store a georeferenced location and attitude data from different sensors
 * (e.g. GPS, IMU, etc.)
 *
 */
struct SensorDataLatLon : public SensorData
{
    double latitude  = 0.0; ///< in °, positive northwards
    double longitude = 0.0; ///< in °, positive eastwards

    /**
     * @brief Construct a new SensorDataLatLon object (all offsets set to 0)
     *
     */
    SensorDataLatLon() = default;

    /**
     * @brief Construct a new Sensor Data Lat Lon object using a base sensor data object
     *
     * @param data
     * @param latitude in °, positive northwards
     * @param longitude in °, positive eastwards
     */
    SensorDataLatLon(const SensorData& data, double latitude, double longitude)
        : SensorData(data)
        , latitude(latitude)
        , longitude(longitude)
    {
    }

    /**
     * @brief Construct an SensorDataLatLon object from an existing SensorDataUTM object (this
     * allows for implicit conversion from SensorDataUTM class)
     *
     */
    SensorDataLatLon(const SensorDataUTM& data_utm); // defined in sensordatautm.hpp

    /**
     * @brief Construct a new SensorDataLatLon object
     *
     * @param latitude in °, positive northwards
     * @param longitude in °, positive eastwards
     * @param depth in m, positive downwards
     * @param heave from heave sensor, will be added to depth in m, positive upwards
     * @param heading  in °, 0° is north, 90° is east
     * @param pitch in °, positive means bow up
     * @param roll in °, positive means port up
     */
    SensorDataLatLon(double latitude,
                     double longitude,
                     double depth,
                     double heave,
                     double heading,
                     double pitch,
                     double roll)
        : SensorData(depth, heave, heading, pitch, roll)
        , latitude(latitude)
        , longitude(longitude)
    {
    }

    bool operator!=(const SensorDataLatLon& rhs) const { return !(operator==(rhs)); }
    /**
     * @brief Check if two SensorDataLatLon objects are equal
     *
     * @param rhs
     * @return true if equal
     * @return false if not equal
     */
    bool operator==(const SensorDataLatLon& rhs) const
    {
        if (SensorData::operator==(rhs))
            if (tools::helper::approx(latitude, rhs.latitude))
                if (tools::helper::approx(longitude, rhs.longitude))
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
        s.value8b(latitude);
        s.value8b(longitude);
    }

  public:
    tools::classhelper::ObjectPrinter __printer__(unsigned int float_precision) const
    {
        tools::classhelper::ObjectPrinter printer("SensorDataLatLon", float_precision);

        printer.register_string(
            "latitude",
            navtools::latitude_to_string(latitude, navtools::t_latlon_format::seconds, 1),
            "ddd°mm',ss.s''N/S");
        printer.register_string(
            "longitude",
            navtools::longitude_to_string(longitude, navtools::t_latlon_format::seconds, 1),
            "ddd°mm',ss.s''E/W");

        printer.append(SensorData::__printer__(float_precision));

        return printer;
    }

  public:
    // -- class helper function macros --
    // define to_binary and from_binary functions (needs the serialization function)
    __BITSERY_DEFAULT_TOFROM_BINARY_FUNCTIONS__(SensorDataLatLon)
    // define info_string and print functions (needs the __printer__ function)
    __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__
};

} // namespace datastructures
} // namespace navigation
} // namespace themachinethatgoesping