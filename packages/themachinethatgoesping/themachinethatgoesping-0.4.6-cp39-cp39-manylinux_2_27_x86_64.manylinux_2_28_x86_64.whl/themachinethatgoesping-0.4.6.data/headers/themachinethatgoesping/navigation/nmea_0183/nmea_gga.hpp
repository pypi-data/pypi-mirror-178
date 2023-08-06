// SPDX-FileCopyrightText: 2022 Peter Urban, Tim Weiß, GEOMAR Helmholtz Centre for Ocean
// Research Kiel SPDX-FileCopyrightText: 2022 Peter Urban, Ghent University
//
// SPDX-License-Identifier: MPL-2.0

#pragma once

#include <charconv>
#include <string>

#include <themachinethatgoesping/tools/classhelper/objectprinter.hpp>
#include <themachinethatgoesping/tools/timeconv.hpp>

#include "../navtools.hpp"
#include "helper.hpp"
#include "nmea_base.hpp"

namespace themachinethatgoesping {
namespace navigation {
namespace nmea_0183 {

/**
 * @brief The NMEA GGA datagram contains time, position, and fix. Typically received from
a global navigation satellite system (GNSS device).
 *
 */
class NMEA_GGA : public NMEA_Base
{

  public:
    /**
     * @brief Construct a new nmea gga object from an existing NMEA_Base datagram
     *
     * @param base Underlying NMEA_Base datagram
     * @param check Check if the NMEA string is valid
     */
    NMEA_GGA(NMEA_Base base, bool check = false)
        : NMEA_Base(std::move(base))
    {
        if (check)
        {
            if (get_sentence_type() != "GGA")
                throw std::runtime_error(
                    fmt::format("NMEA_GGA: wrong sentence type [{}]", get_sentence_type()));
        }
        parse_fields();
    }

    // ----- NMEA GGA attributes -----
    std::string get_utc_time_string() const { return std::string(get_field(0)); }
    double      get_latitude() const
    {
        if (get_field(2) == "N")
            return nmea_latitude_field_to_double(get_field(1));
        else
            return -nmea_latitude_field_to_double(get_field(1));
    }
    double get_longitude() const
    {
        if (get_field(4) == "E")
            return nmea_longitude_field_to_double(get_field(3));
        else
            return -nmea_longitude_field_to_double(get_field(3));
    }

    int         get_quality() const { return get_field_as_int(5); }
    std::string get_quality_explained() const
    {
        switch (get_quality())
        {
            case 0:
                return "invalid";
            case 1:
                return "GPS fix";
            case 2:
                return "DGPS fix";
            case 3:
                return "PPS fix";
            case 4:
                return "RTK fix";
            case 5:
                return "Float RTK";
            case 6:
                return "estimated (dead reckoning) fix";
            case 7:
                return "manual input mode";
            case 8:
                return "simulation mode";
            default:
                return "unknown";
        }
    }
    int    get_number_of_satellites() const { return get_field_as_int(6); }
    double get_horizontal_dilution_of_precision() const { return get_field_as_double(7); }
    double get_altitude() const { return get_field_as_double(8); }
    double get_geoidal_separation() const { return get_field_as_double(10); }
    double get_age_of_differential_gps_data() const { return get_field_as_double(12); }
    int    get_differential_reference_station_id() const { return get_field_as_int(13); }

    // ----- binary streaming -----
    // this has to be explicit, because otherwise the compiler will use the base class version
    static NMEA_GGA from_stream(std::istream& is)
    {
        return NMEA_GGA(NMEA_Base::from_stream(is), true);
    }

    // ----- objectprinter -----
    tools::classhelper::ObjectPrinter __printer__(unsigned int float_precision) const
    {
        tools::classhelper::ObjectPrinter printer("NMEA GGA Datagram", float_precision);

        printer.append(NMEA_Base::__printer__(float_precision));

        printer.register_section("GGA attributes");
        printer.register_value("utc_time_string", get_utc_time_string(), "HHMMSS.SS");

        printer.register_string(
            "latitude",
            navtools::latitude_to_string(get_latitude(), navtools::t_latlon_format::minutes, 2),
            "ddd°mm.mm'N/S");
        printer.register_string(
            "longitude",
            navtools::longitude_to_string(get_longitude(), navtools::t_latlon_format::minutes, 2),
            "ddd°mm.mm'E/W");

        printer.register_value("quality", get_quality(), get_quality_explained());
        printer.register_value("number_of_satellites", get_number_of_satellites());
        printer.register_value("horizontal_dilution_of_precision",
                               get_horizontal_dilution_of_precision());
        printer.register_value("altitude", get_altitude(), "m");
        printer.register_value("geoidal_separation", get_geoidal_separation(), "m");
        printer.register_value(
            "age_of_differential_gps_data", get_age_of_differential_gps_data(), "s");
        printer.register_value("differential_reference_station_id",
                               get_differential_reference_station_id());

        return printer;
    }

    // ----- class helper macros -----
    __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__
    __STREAM_DEFAULT_TOFROM_BINARY_FUNCTIONS__(NMEA_GGA)
};

} // nmea_0183
} // namespace navigation
} // namespace themachinethatgoesping
