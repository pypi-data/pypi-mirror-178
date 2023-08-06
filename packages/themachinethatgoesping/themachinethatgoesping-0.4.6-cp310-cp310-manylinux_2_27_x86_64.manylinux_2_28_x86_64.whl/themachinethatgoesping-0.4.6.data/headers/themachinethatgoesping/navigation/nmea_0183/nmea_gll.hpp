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
 * @brief The NMEA GLL datagram contains time, position, and status. Typically received from
a global navigation satellite system (GNSS device).
 *
 */
class NMEA_GLL : public NMEA_Base
{

  public:
    /**
     * @brief Construct a new nmea gll object from an existing NMEA_Base datagram
     *
     * @param base Underlying NMEA_Base datagram
     * @param check Check if the NMEA string is valid
     */
    NMEA_GLL(NMEA_Base base, bool check = false)
        : NMEA_Base(std::move(base))
    {
        if (check)
        {
            if (get_sentence_type() != "GLL")
                throw std::runtime_error(
                    fmt::format("NMEA_GLL: wrong sentence type [{}]", get_sentence_type()));
        }
        parse_fields();
    }

    // ----- NMEA GLL attributes -----
    double get_latitude() const
    {
        if (get_field(1) == "N")
            return nmea_latitude_field_to_double(get_field(0));
        else
            return -nmea_latitude_field_to_double(get_field(0));
    }
    double get_longitude() const
    {
        if (get_field(3) == "E")
            return nmea_longitude_field_to_double(get_field(2));
        else
            return -nmea_longitude_field_to_double(get_field(2));
    }

    std::string get_utc_time_string() const { return std::string(get_field(4)); }
    bool        get_status() const { return get_field(5) == "A"; }

    char get_mode() const
    {
        try
        {
            return get_field(6)[0];
        }
        catch ([[maybe_unused]] std::out_of_range& e)
        {
            return '\x00';
        }
    }
    std::string get_mode_explained() const
    {
        char mode = get_mode();
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

    // ----- binary streaming -----
    // this has to be explicit, because otherwise the compiler will use the base class version
    static NMEA_GLL from_stream(std::istream& is)
    {
        return NMEA_GLL(NMEA_Base::from_stream(is), true);
    }

    // ----- objectprinter -----
    tools::classhelper::ObjectPrinter __printer__(unsigned int float_precision) const
    {
        tools::classhelper::ObjectPrinter printer("NMEA GLL Datagram", float_precision);

        printer.append(NMEA_Base::__printer__(float_precision));

        printer.register_section("GLL attributes");

        printer.register_string(
            "latitude",
            navtools::latitude_to_string(get_latitude(), navtools::t_latlon_format::minutes, 2),
            "ddd°mm.mm'N/S");
        printer.register_string(
            "longitude",
            navtools::longitude_to_string(get_longitude(), navtools::t_latlon_format::minutes, 2),
            "ddd°mm.mm'E/W");

        printer.register_value("utc_time_string", get_utc_time_string(), "HHMMSS.SS");
        printer.register_value("status", this->get_status());
        printer.register_value("mode", get_mode(), get_mode_explained());

        return printer;
    }

    // ----- class helper macros -----
    __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__
    __STREAM_DEFAULT_TOFROM_BINARY_FUNCTIONS__(NMEA_GLL)
};

} // nmea_0183
} // namespace navigation
} // namespace themachinethatgoesping
