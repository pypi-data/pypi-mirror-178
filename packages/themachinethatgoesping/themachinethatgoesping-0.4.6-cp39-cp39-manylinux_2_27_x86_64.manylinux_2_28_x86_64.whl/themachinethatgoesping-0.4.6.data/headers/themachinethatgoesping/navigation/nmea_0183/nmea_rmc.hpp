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
 * @brief The NMEA RMC datagram contains time, date, position, course and speed data. Typically
received from a global navigation satellite system (GNSS device).
 *
 */
class NMEA_RMC : public NMEA_Base
{

  public:
    /**
     * @brief Construct a new nmea rmc object from an existing NMEA_Base datagram
     *
     * @param base Underlying NMEA_Base datagram
     * @param check Check if the NMEA string is valid
     */
    NMEA_RMC(NMEA_Base base, bool check = false)
        : NMEA_Base(std::move(base))
    {
        if (check)
        {
            if (get_sentence_type() != "RMC")
                throw std::runtime_error(
                    fmt::format("NMEA_RMC: wrong sentence type [{}]", get_sentence_type()));
        }
        parse_fields();
    }

    // ----- NMEA RMC attributes -----
    std::string get_utc_time_string() const { return std::string(get_field(0)); }
    bool        get_status() const { return get_field(1) == "A"; }

    double get_latitude() const
    {
        if (get_field(3) == "N")
            return nmea_latitude_field_to_double(get_field(2));
        else
            return -nmea_latitude_field_to_double(get_field(2));
    }
    double get_longitude() const
    {
        if (get_field(5) == "E")
            return nmea_longitude_field_to_double(get_field(4));
        else
            return -nmea_longitude_field_to_double(get_field(4));
    }

    double      get_speed_over_ground_knots() const { return get_field_as_double(6); }
    double      get_course_over_ground_degrees_true() const { return get_field_as_double(7); }
    std::string get_utc_date_string() const { return std::string(get_field(8)); }
    double      get_magnetic_variation() const { return get_field_as_double(9); }
    char        get_mode() const
    {
        try
        {
            return get_field(10)[0];
        }
        catch ([[maybe_unused]] std::out_of_range& e)
        {
            return '\x00';
        }
    }
    std::string get_mode_explained() const
    {
        char mode = this->get_mode();
        if (mode == 'A')
            return "Autonomous";
        if (mode == 'D')
            return "Differential";
        if (mode == 'E')
            return "Estimated";
        if (mode == 'M')
            return "Manual";
        if (mode == 'S')
            return "Simulated";
        if (mode == 'N')
            return "Data not valid";
        return "Unknown";
    }

    // ----- conversions -----
    /**
     * @brief Convert the datagram into a unixtime stamp
     *
     * @return unixtime (seconds since 1970-01-01 00:00:00 UTC)
     */
    double to_timestamp() const
    {
        try
        {
            using themachinethatgoesping::tools::timeconv::datestring_to_unixtime;
            auto field_time = get_field(0);
            auto field_date = get_field(8);

            if (field_time.size() < 6 || field_date.size() < 6)
                return std::numeric_limits<double>::quiet_NaN();

            auto   date_time = get_utc_time_string() + "-" + get_utc_date_string() + '-' + "0000";
            double timestamp = datestring_to_unixtime(date_time, "%H%M%S-%d%m%y-%z");
            return timestamp;
        }
        catch (...)
        {
            return std::numeric_limits<double>::quiet_NaN();
        }
    }

    /**
     * @brief Convert the datagram into a date time string
     *        Note: this function uses to_timestamp()
     *
     * @param format Format string (see
     * https://howardhinnant.github.io/date/date.html#to_stream_formatting)
     * @return date time string
     */
    std::string to_date_string(const std::string& format = "%z__%d-%m-%Y__%H:%M:%S") const
    {
        using themachinethatgoesping::tools::timeconv::unixtime_to_datestring;
        return unixtime_to_datestring(to_timestamp(), 2, format);
    }

    // ----- binary streaming -----
    // this has to be explicit, because otherwise the compiler will use the base class version
    static NMEA_RMC from_stream(std::istream& is)
    {
        return NMEA_RMC(NMEA_Base::from_stream(is), true);
    }

    // ----- objectprinter -----
    tools::classhelper::ObjectPrinter __printer__(unsigned int float_precision) const
    {
        tools::classhelper::ObjectPrinter printer("NMEA RMC Datagram", float_precision);

        printer.append(NMEA_Base::__printer__(float_precision));

        printer.register_section("RMC attributes");
        printer.register_value("utc_time_string", get_utc_time_string(), "HHMMSS.SS");
        printer.register_value("status", get_status());

        printer.register_string(
            "latitude",
            navtools::latitude_to_string(get_latitude(), navtools::t_latlon_format::minutes, 2),
            "ddd°mm.mm'N/S");
        printer.register_string(
            "longitude",
            navtools::longitude_to_string(get_longitude(), navtools::t_latlon_format::minutes, 2),
            "ddd°mm.mm'E/W");

        printer.register_value("speed_over_ground_knots", get_speed_over_ground_knots());
        printer.register_value("course_over_ground_degrees_true",
                               get_course_over_ground_degrees_true());
        printer.register_value("date", get_utc_date_string());
        printer.register_value("magnetic_variation", get_magnetic_variation());
        printer.register_value("mode", get_mode(), get_mode_explained());

        printer.register_section("Converted attributes");
        printer.register_value("to_timestamp", std::to_string(to_timestamp()), "unixtime");
        printer.register_value("to_date_string", to_date_string());

        return printer;
    }

    // ----- class helper macros -----
    __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__
    __STREAM_DEFAULT_TOFROM_BINARY_FUNCTIONS__(NMEA_RMC)
};

} // nmea_0183
} // namespace navigation
} // namespace themachinethatgoesping
