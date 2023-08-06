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
#include "sensordatalatlon.hpp"
#include "sensordatalocal.hpp"

namespace themachinethatgoesping {
namespace navigation {
namespace datastructures {

/**
 * @brief A structure to store a georeferenced data and attitude data from different sensors
 * (e.g. GPS, IMU, etc.)
 * Unlike SensorDataLatLon, this structure stores UTM coordinates.
 *
 */
struct SensorDataUTM : public SensorDataLocal
{
    int  utm_zone = 0; ///< UTM/UPS zone number
    bool utm_northern_hemisphere =
        true; ///< if true: northern hemisphere, else: southern hemisphere

    /**
     * @brief Construct a new Sensor Position object (all offsets set to 0)
     *
     */
    SensorDataUTM() = default;

    /**
     * @brief Construct a new Sensor Data Local object using a base sensor data object
     *
     * @param data
     * @param northing in m, positive northwards
     * @param easting in m, positive eastwards
     * @param utm_zone UTM/UPS zone number
     * @param utm_northern_hemisphere if true: northern hemisphere, else: southern hemisphere
     */
    SensorDataUTM(const SensorData& data,
                  double            northing,
                  double            easting,
                  int               utm_zone,
                  bool              utm_northern_hemisphere)
        : SensorDataLocal(data, northing, easting)
        , utm_zone(utm_zone)
        , utm_northern_hemisphere(utm_northern_hemisphere)
    {
    }

    /**
     * @brief Construct an SensorDataUTM object from an existing SensorDataLocal object (using a
     * known zone and hemisphere)
     *
     * @param data_local
     * @param utm_zone UTM/UPS zone number
     * @param utm_northern_hemisphere if true: northern hemisphere, else: southern hemisphere
     */
    SensorDataUTM(const SensorDataLocal& data_local, int utm_zone, bool utm_northern_hemisphere)
        : SensorDataLocal(data_local)
        , utm_zone(utm_zone)
        , utm_northern_hemisphere(utm_northern_hemisphere)
    {
    }

    /**
     * @brief Construct an SensorDataUTM object from an existing SensorDataLatLon object (this
     * allows for implicit conversion from SensorDataLatLon class)
     *
     */
    SensorDataUTM(const SensorDataLatLon& data, int setzone = -1)
        : SensorDataUTM(from_sensordata(data, setzone))
    {
    }

    /**
     * @brief Construct a new SensorDataUTM object
     *
     * @param northing in m, positive northwards
     * @param easting in m, positive eastwards
     * @param utm_zone UTM/UPS zone number
     * @param utm_northern_hemisphere if true: northern hemisphere, else: southern hemisphere
     * @param depth in m, positive downwards
     * @param heave is added to depth in m, positive upwards
     * @param heading in °, 0° is north, 90° is east
     * @param pitch in °, positive means bow up
     * @param roll in °, positive means port up
     */
    SensorDataUTM(double northing,
                  double easting,
                  int    utm_zone,
                  bool   utm_northern_hemisphere,
                  double depth,
                  double heave,
                  double heading,
                  double pitch,
                  double roll)
        : SensorDataLocal(northing, easting, depth, heave, heading, pitch, roll)
        , utm_zone(utm_zone)
        , utm_northern_hemisphere(utm_northern_hemisphere)
    {
    }

    bool operator!=(const SensorDataUTM& rhs) const { return !(operator==(rhs)); }
    /**
     * @brief Check if two SensorDataUTM objects are equal
     *
     * @param rhs
     * @return true if equal
     * @return false if not equal
     */
    bool operator==(const SensorDataUTM& rhs) const
    {
        if (SensorDataLocal::operator==(rhs))
            if (utm_zone == rhs.utm_zone)
                if (utm_northern_hemisphere == rhs.utm_northern_hemisphere)
                    return true;

        return false;
    }
    /**
     * @brief Convert a utm sensordatalatlon to an unprojected data
     *
     * @param data_utm
     * @return SensorDataLatLon
     */
    static SensorDataLatLon to_sensordata(const SensorDataUTM& data_utm)
    {
        SensorDataLatLon data(
            0, 0, data_utm.depth, data_utm.heave, data_utm.heading, data_utm.pitch, data_utm.roll);

        GeographicLib::UTMUPS::Reverse(data_utm.utm_zone,
                                       data_utm.utm_northern_hemisphere,
                                       data_utm.easting,
                                       data_utm.northing,
                                       data.latitude,
                                       data.longitude);

        return data;
    }

    /**
     * @brief Construct convert a SensorDataLatLon Object to UTM
     *
     * @param data valid SensorDataLatLon object
     * @param setzone set a preferred UTM zone negative means automatic, zero means UPS, positive
     * means a particular UTM zone
     * @return SensorDataUTM
     */
    static SensorDataUTM from_sensordata(const SensorDataLatLon& data, int setzone = -1)
    {
        SensorDataUTM data_utm(
            0, 0, 0, 0, data.depth, data.heave, data.heading, data.pitch, data.roll);

        GeographicLib::UTMUPS::Forward(data.latitude,
                                       data.longitude,
                                       data_utm.utm_zone,
                                       data_utm.utm_northern_hemisphere,
                                       data_utm.easting,
                                       data_utm.northing,
                                       setzone);

        return data_utm;
    }

  private:
    // serialization support using bitsery
    friend bitsery::Access;
    template<typename S>
    void serialize(S& s)
    {
        s.ext(*this, bitsery::ext::BaseClass<SensorDataLocal>{});
        s.value4b(utm_zone);
        s.value1b(utm_northern_hemisphere);
    }

  public:
    tools::classhelper::ObjectPrinter __printer__(unsigned int float_precision) const
    {
        tools::classhelper::ObjectPrinter printer("SensorDataUTM", float_precision);

        auto base_printer = SensorDataLocal::__printer__(float_precision);
        base_printer.remove_sections();
        printer.append(base_printer);
        printer.register_value("utm_zone", utm_zone, "", 2);
        printer.register_value("utm_northern_hemisphere", utm_northern_hemisphere, "", 3);

        return printer;
    }

  public:
    // -- class helper function macros --
    // define to_binary and from_binary functions (needs the serialization function)
    __BITSERY_DEFAULT_TOFROM_BINARY_FUNCTIONS__(SensorDataUTM)
    // define info_string and print functions (needs the __printer__ function)
    __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__
};

// backwards conversion
inline SensorDataLatLon::SensorDataLatLon(const SensorDataUTM& data_utm)
    : SensorDataLatLon(SensorDataUTM::to_sensordata(data_utm))
{
}

} // namespace datastructures
} // namespace navigation
} // namespace themachinethatgoesping