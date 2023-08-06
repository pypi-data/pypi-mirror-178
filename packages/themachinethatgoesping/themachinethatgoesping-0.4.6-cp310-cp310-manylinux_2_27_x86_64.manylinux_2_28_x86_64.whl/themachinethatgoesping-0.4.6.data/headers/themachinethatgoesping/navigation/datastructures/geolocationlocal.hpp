// Kiel SPDX-FileCopyrightText: 2022 Peter Urban, Ghent University
//
// SPDX-License-Identifier: MPL-2.0

#pragma once

#include <GeographicLib/UTMUPS.hpp>

#include <themachinethatgoesping/tools/classhelper/bitsery.hpp>
#include <themachinethatgoesping/tools/classhelper/objectprinter.hpp>
#include <themachinethatgoesping/tools/helper.hpp>
#include <themachinethatgoesping/tools/rotationfunctions/quaternions.hpp>

//#include "geolocationutm.hpp"

namespace themachinethatgoesping {
namespace navigation {
namespace datastructures {

/**
 * @brief A structure to store a georeferenced location and attitude (e.g. of a sensor)
 * unlike the default GeoLocation structure, this object stores local northing and easting
 * coordinates. These coordinates can be converted to UTM coordinates if the zone and hemisphere are
 * known.
 */
struct GeoLocationLocal : public GeoLocation
{
    double northing = 0.0; ///< in m, positive northwards
    double easting  = 0.0; ///< in m, positive eastwards

    /**
     * @brief Construct a new Sensor Position object (all offsets set to 0)
     *
     */
    GeoLocationLocal() = default;

    /**
     * @brief Construct a new GeoLocationLocal object
     *
     * @param location
     * @param northing in m, positive northwards
     * @param easting in m, positive eastwards
     */
    GeoLocationLocal(const GeoLocation& location, double northing, double easting)
        : GeoLocation(location)
        , northing(northing)
        , easting(easting)
    {
    }

    /**
     * @brief Construct a new GeoLocationLocal object
     *
     * @param northing in m, positive northwards
     * @param easting in m, positive eastwards
     * @param z in m, positive downwards
     * @param yaw in °, 0° is north, 90° is east
     * @param pitch in °, positive means bow up
     * @param roll in °, positive means port up
     */
    GeoLocationLocal(double northing,
                     double easting,
                     double z,
                     double yaw,
                     double pitch,
                     double roll)
        : GeoLocation(z, yaw, pitch, roll)
        , northing(northing)
        , easting(easting)
    {
    }

    bool operator!=(const GeoLocationLocal& rhs) const { return !(operator==(rhs)); }
    bool operator==(const GeoLocationLocal& rhs) const
    {
        if (GeoLocation::operator==(rhs))
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
        s.ext(*this, bitsery::ext::BaseClass<GeoLocation>{});
        s.value8b(northing);
        s.value8b(easting);
    }

  public:
    tools::classhelper::ObjectPrinter __printer__(unsigned int float_precision) const
    {
        tools::classhelper::ObjectPrinter printer("GeoLocationLocal", float_precision);

        printer.register_value("northing", northing, "positive northwards, m");
        printer.register_value("easting", easting, "positive eastwards, m");

        printer.append(GeoLocation::__printer__(float_precision));

        return printer;
    }

  public:
    // -- class helper function macros --
    // define to_binary and from_binary functions (needs the serialize function)
    __BITSERY_DEFAULT_TOFROM_BINARY_FUNCTIONS__(GeoLocationLocal)
    // define info_string and print functions (needs the __printer__ function)
    __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__
};

} // namespace datastructures
} // namespace navigation
} // namespace themachinethatgoesping