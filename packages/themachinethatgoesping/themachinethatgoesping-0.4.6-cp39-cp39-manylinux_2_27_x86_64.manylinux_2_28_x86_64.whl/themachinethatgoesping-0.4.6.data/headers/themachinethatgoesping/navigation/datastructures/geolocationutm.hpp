// Kiel SPDX-FileCopyrightText: 2022 Peter Urban, Ghent University
//
// SPDX-License-Identifier: MPL-2.0

#pragma once

#include <GeographicLib/UTMUPS.hpp>

#include <themachinethatgoesping/tools/classhelper/bitsery.hpp>
#include <themachinethatgoesping/tools/classhelper/objectprinter.hpp>
#include <themachinethatgoesping/tools/helper.hpp>
#include <themachinethatgoesping/tools/rotationfunctions/quaternions.hpp>

#include "geolocationlatlon.hpp"
#include "geolocationlocal.hpp"

namespace themachinethatgoesping {
namespace navigation {
namespace datastructures {

/**
 * @brief A structure to store a georeferenced location and attitude (e.g. of a sensor)
 * unlike the default GeoLocation structure, this object stores utm coordinates
 */
struct GeoLocationUTM : public GeoLocationLocal
{
    int  zone                = 0;    ///< UTM/UPS zone number
    bool northern_hemisphere = true; ///< if true: northern hemisphere, else: southern hemisphere

    /**
     * @brief Construct a new Sensor Position object
     *
     */
    GeoLocationUTM() = default;

    /**
     * @brief Construct an GeoLocationUTM object from an existing GeoLocationLocal object (using a
     * known zone and hemisphere)
     *
     * @param location_local
     * @param zone UTM/UPS zone number
     * @param northern_hemisphere if true: northern hemisphere, else: southern hemisphere
     */
    GeoLocationUTM(const GeoLocationLocal& location_local, int zone, bool northern_hemisphere)
        : GeoLocationLocal(location_local)
        , zone(zone)
        , northern_hemisphere(northern_hemisphere)
    {
    }

    /**
     * @brief Construct an GeoLocationUTM object from an existing GeoLocationLatLon object (this
     * allows for implicit conversion from GeoLocationLatLon class)
     *
     */
    GeoLocationUTM(const GeoLocationLatLon& location, int setzone = -1)
        : GeoLocationUTM(from_geolocation_latlon(location, setzone))
    {
    }

    /**
     * @brief Construct a new GeoLocationUTM object
     *
     * @param northing in m, positive northwards
     * @param easting in m, positive eastwards
     * @param zone UTM/UPS zone number
     * @param northern_hemisphere if true: northern hemisphere, else: southern hemisphere
     * @param z in m, positive downwards
     * @param yaw in °, 0° is north, 90° is east
     * @param pitch in °, positive means bow up
     * @param roll in °, positive means port up
     */
    GeoLocationUTM(double northing,
                   double easting,
                   int    zone,
                   bool   northern_hemisphere,
                   double z,
                   double yaw,
                   double pitch,
                   double roll)
        : GeoLocationLocal(northing, easting, z, yaw, pitch, roll)
        , zone(zone)
        , northern_hemisphere(northern_hemisphere)
    {
    }

    bool operator!=(const GeoLocationUTM& rhs) const { return !(operator==(rhs)); }
    bool operator==(const GeoLocationUTM& rhs) const
    {
        if (GeoLocationLocal::operator==(rhs))
            if (zone == rhs.zone)
                if (northern_hemisphere == rhs.northern_hemisphere)
                    return true;

        return false;
    }

    /**
     * @brief Convert a utm geolocationlatlon to an unprojected location
     *
     * @param location_utm
     * @return GeoLocationLatLon
     */
    static GeoLocationLatLon to_geolocation_latlon(const GeoLocationUTM& location_utm)
    {
        GeoLocationLatLon location(
            0, 0, location_utm.z, location_utm.yaw, location_utm.pitch, location_utm.roll);

        GeographicLib::UTMUPS::Reverse(location_utm.zone,
                                       location_utm.northern_hemisphere,
                                       location_utm.easting,
                                       location_utm.northing,
                                       location.latitude,
                                       location.longitude);

        return location;
    }

    /**
     * @brief Construct convert a GeoLocationLatLon Object to UTM
     *
     * @param location valid GeoLocationLatLon object
     * @param setzone set a preferred UTM zone negative means automatic, zero means UPS, positive
     * means a particular UTM zone
     * @return GeoLocationUTM
     */
    static GeoLocationUTM from_geolocation_latlon(const GeoLocationLatLon& location,
                                                  int                      setzone = -1)
    {
        GeoLocationUTM location_utm(
            0, 0, 0, 0, location.z, location.yaw, location.pitch, location.roll);

        GeographicLib::UTMUPS::Forward(location.latitude,
                                       location.longitude,
                                       location_utm.zone,
                                       location_utm.northern_hemisphere,
                                       location_utm.easting,
                                       location_utm.northing,
                                       setzone);

        return location_utm;
    }

  private:
    // serialization support using bitsery
    friend bitsery::Access;
    template<typename S>
    void serialize(S& s)
    {
        s.value8b(northing);
        s.value8b(easting);
        s.value4b(zone);
        s.value1b(northern_hemisphere);
        s.value8b(z);
        s.value8b(yaw);
        s.value8b(pitch);
        s.value8b(roll);
    }

  public:
    tools::classhelper::ObjectPrinter __printer__(unsigned int float_precision) const
    {
        tools::classhelper::ObjectPrinter printer("GeoLocationUTM", float_precision);

        auto base_printer = GeoLocationLocal::__printer__(float_precision);
        base_printer.remove_sections();
        printer.append(base_printer);
        printer.register_value("zone", zone, "", 2);
        printer.register_value("northern_hemisphere", northern_hemisphere, "", 3);

        return printer;
    }

  public:
    // -- class helper function macros --
    // define to_binary and from_binary functions (needs the serialize function)
    __BITSERY_DEFAULT_TOFROM_BINARY_FUNCTIONS__(GeoLocationUTM)
    // define info_string and print functions (needs the __printer__ function)
    __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__
};

// backwards conversion
inline GeoLocationLatLon::GeoLocationLatLon(const GeoLocationUTM& location_utm)
    : GeoLocationLatLon(GeoLocationUTM::to_geolocation_latlon(location_utm))
{
}

} // namespace datastructures
} // namespace navigation
} // namespace themachinethatgoesping