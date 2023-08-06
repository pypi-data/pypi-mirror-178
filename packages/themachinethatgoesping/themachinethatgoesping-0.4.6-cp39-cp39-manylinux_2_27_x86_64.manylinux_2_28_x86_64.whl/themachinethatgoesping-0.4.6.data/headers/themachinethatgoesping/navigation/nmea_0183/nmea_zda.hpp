// SPDX-FileCopyrightText: 2022 Peter Urban, Tim Weiß, GEOMAR Helmholtz Centre for Ocean
// Research Kiel SPDX-FileCopyrightText: 2022 Peter Urban, Ghent University
//
// SPDX-License-Identifier: MPL-2.0

#pragma once

#include <charconv>
#include <string>

#include <themachinethatgoesping/tools/classhelper/objectprinter.hpp>
#include <themachinethatgoesping/tools/timeconv.hpp>

#include "nmea_base.hpp"

namespace themachinethatgoesping {
namespace navigation {
namespace nmea_0183 {

/**
 * @brief The NMEA ZDA datagram contains the universal time code (UTC), get_day, get_month, get_year
and local time zone offsets.
 *
 */
class NMEA_ZDA : public NMEA_Base
{

  public:
    /**
     * @brief Construct a new nmea zda object from an existing NMEA_Base datagram
     *
     * @param base Underlying NMEA_Base datagram
     * @param check Check if the NMEA string is valid
     */
    NMEA_ZDA(NMEA_Base base, bool check = false)
        : NMEA_Base(std::move(base))
    {
        if (check)
        {
            if (get_sentence_type() != "ZDA")
                throw std::runtime_error(
                    fmt::format("NMEA_ZDA: wrong sentence type [{}]", get_sentence_type()));
        }
        parse_fields();
    }

    std::string get_utc_time_string() const { return std::string(get_field(0)); }
    int         get_day() const { return get_field_as_int(1); }
    int         get_month() const { return get_field_as_int(2); }
    int         get_year() const { return get_field_as_int(3); }
    int         get_local_zone_hours() const { return get_field_as_int(4); }
    int         get_local_zone_minutes() const { return get_field_as_int(5); }

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

            std::string time_string   = _sentence.substr(7, _sentence.size() - 8);
            double      unixtime      = datestring_to_unixtime(time_string, "%H%M%S,%d,%m,%Y");
            auto        field_hours   = get_field(4);
            auto        field_minutes = get_field(4);
            if (!field_hours.empty() && field_hours != "00")
            {
                // int hours;
                // std::from_chars(field_hours.data(), field_hours.data() + field_hours.size(),
                // hours); unixtime += 3600 * hours;
                unixtime += 3600 * std::stoi(std::string(field_hours));
            }
            if (!field_minutes.empty() && field_minutes != "00")
            {
                // int minutes;
                // std::from_chars(field_minutes.data(), field_minutes.data() +
                // field_minutes.size(),
                //                 minutes);
                // unixtime += 60 * minutes;
                unixtime += 60 * std::stoi(std::string(field_minutes));
            }

            return unixtime;
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
    std::string to_date_string(std::string format = std::string("%z__%d-%m-%Y__%H:%M:%S")) const
    {
        using themachinethatgoesping::tools::timeconv::unixtime_to_datestring;
        return unixtime_to_datestring(to_timestamp(), 2, format);
    }

    // ----- binary streaming -----
    // this has to be explicit, because otherwise the compiler will use the base class version
    static NMEA_ZDA from_stream(std::istream& is)
    {
        return NMEA_ZDA(NMEA_Base::from_stream(is), true);
    }

    // ----- objectprinter -----
    tools::classhelper::ObjectPrinter __printer__(unsigned int float_precision) const
    {
        tools::classhelper::ObjectPrinter printer("NMEA ZDA Datagram", float_precision);

        printer.append(NMEA_Base::__printer__(float_precision));

        printer.register_section("ZDA attributes");
        printer.register_value("utc_time_string", get_utc_time_string(), "HHMMSS.SS");
        printer.register_value("day", get_day());
        printer.register_value("month", get_month());
        printer.register_value("year", get_year());
        printer.register_value("local_zone_hours", get_local_zone_hours());
        printer.register_value("local_zone_minutes", get_local_zone_minutes());

        printer.register_section("Converted attributes");
        printer.register_value("timestamp", std::to_string(to_timestamp()), "unixtime");
        printer.register_value("date_string", to_date_string());

        return printer;
    }

    // ----- class helper macros -----
    __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__
    __STREAM_DEFAULT_TOFROM_BINARY_FUNCTIONS__(NMEA_ZDA)
};

} // nmea_0183
} // namespace navigation
} // namespace themachinethatgoesping
