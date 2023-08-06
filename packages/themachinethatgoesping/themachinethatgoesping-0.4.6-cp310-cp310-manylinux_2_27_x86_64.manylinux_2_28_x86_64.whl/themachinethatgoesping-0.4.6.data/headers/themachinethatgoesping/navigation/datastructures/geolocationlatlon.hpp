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
#include "geolocation.hpp"

namespace themachinethatgoesping {
namespace navigation {
namespace datastructures {

// forward declarations for location conversions
struct GeoLocationUTM; // defined in geolocationutm.hpp

/**
 * @brief A structure to store a georeferenced location and attitude (e.g. of a sensor)
 * Unlike the base GeoLocation object, this also stores latitude and longitude coordinates
 *
 */
struct GeoLocationLatLon : public GeoLocation
{
    double latitude  = 0.0; ///< in °, positive northwards
    double longitude = 0.0; ///< in °, positive eastwards
    /**
     * @brief Construct a new Sensor Position object (all offsets set to 0)
     *
     */
    GeoLocationLatLon() = default;

    /**
     * @brief Construct a new Sensor Data Lat Lon object using a base sensor data object
     *
     * @param location
     * @param latitude in °, positive northwards
     * @param longitude in °, positive eastwards
     */
    GeoLocationLatLon(const GeoLocation& location, double latitude, double longitude)
        : GeoLocation(location)
        , latitude(latitude)
        , longitude(longitude)
    {
    }

    /**
     * @brief Construct an GeoLocationLatLon object from an existing GeoLocationUTM object (this
     * allows for implicit conversion from GeoLocationUTM class)
     *
     */
    GeoLocationLatLon(const GeoLocationUTM& location_utm); // defined in geolocationutm.hpp

    /**
     * @brief Construct a new GeoLocationLatLon object
     *
     * @param latitude in °, positive northwards
     * @param longitude in °, positive eastwards
     * @param z in m, positive downwards
     * @param yaw in °, 0° is north, 90° is east
     * @param pitch in °, positive means bow up
     * @param roll in °, positive means port up
     */
    GeoLocationLatLon(double latitude,
                      double longitude,
                      double z,
                      double yaw,
                      double pitch,
                      double roll)
        : GeoLocation(z, yaw, pitch, roll)
        , latitude(latitude)
        , longitude(longitude)
    {
    }

    /**
     * @brief Construct a new GeoLocationLatLon object from a string
     *
     * @param str string containing the location in the format "latitude,longitude,z,yaw,pitch,roll"
     */
    bool operator!=(const GeoLocationLatLon& rhs) const { return !(operator==(rhs)); }

    /**
     * @brief Check if two GeoLocationLatLon objects are equal
     *
     * @param rhs
     * @return true if equal
     * @return false if not equal
     */
    bool operator==(const GeoLocationLatLon& other) const
    {
        if (GeoLocation::operator==(other))
            if (tools::helper::approx(latitude, other.latitude))
                if (tools::helper::approx(longitude, other.longitude))
                    return true;

        return false;
    }

  private:
    // ----- bitsery -----
    friend bitsery::Access;
    template<typename S>
    void serialize(S& s)
    {
        s.ext(*this, bitsery::ext::BaseClass<GeoLocation>{});
        s.value8b(latitude);
        s.value8b(longitude);
    }

  public:
    // ----- objectprinter -----
    tools::classhelper::ObjectPrinter __printer__(unsigned int float_precision) const
    {
        tools::classhelper::ObjectPrinter printer("GeoLocationLatLon", float_precision);

        printer.register_string(
            "latitude",
            navtools::latitude_to_string(latitude, navtools::t_latlon_format::seconds, 1),
            "ddd°mm',ss.s''N/S");
        printer.register_string(
            "longitude",
            navtools::longitude_to_string(longitude, navtools::t_latlon_format::seconds, 1),
            "ddd°mm',ss.s''E/W");

        printer.append(GeoLocation::__printer__(float_precision));

        return printer;
    }

  public:
    // -- class helper function macros --
    // define to_binary and from_binary functions (needs the serialize function)
    __BITSERY_DEFAULT_TOFROM_BINARY_FUNCTIONS__(GeoLocationLatLon)
    // define info_string and print functions (needs the __printer__ function)
    __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__
};

} // namespace datastructures
} // namespace navigation
} // namespace themachinethatgoesping