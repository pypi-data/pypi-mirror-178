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
 * @brief The NMEA GST datagram contains Position error statistics. Typically received from
 * a global navigation satellite system (GNSS device).
 *
 */
class NMEA_GST : public NMEA_Base
{

  public:
    /**
     * @brief Construct a new nmea GST object from an existing NMEA_Base datagram
     *
     * @param base Underlying NMEA_Base datagram
     * @param check Check if the NMEA string is valid
     */
    NMEA_GST(NMEA_Base base, bool check = false)
        : NMEA_Base(std::move(base))
    {
        if (check)
        {
            if (get_sentence_type() != "GST")
                throw std::runtime_error(
                    fmt::format("NMEA_GST: wrong sentence type [{}]", get_sentence_type()));
        }
        parse_fields();
    }

    // ----- NMEA GST attributes -----
    std::string get_utc_time_string() const { return std::string(get_field(0)); }
    double      get_psuedorange_rms() const { return get_field_as_double(1); }
    double      get_semimajor_error() const { return get_field_as_double(2); }
    double      get_semiminor_error() const { return get_field_as_double(3); }
    double      get_semimajor_error_orientation() const { return get_field_as_double(4); }
    double      get_latitude_error_deviation() const { return get_field_as_double(5); }
    double      get_longitude_error_deviation() const { return get_field_as_double(6); }
    double      get_altitude_error_deviation() const { return get_field_as_double(7); }

    // ----- binary streaming -----
    // this has to be explicit, because otherwise the compiler will use the base class version
    static NMEA_GST from_stream(std::istream& is)
    {
        return NMEA_GST(NMEA_Base::from_stream(is), true);
    }

    // ----- objectprinter -----
    tools::classhelper::ObjectPrinter __printer__(unsigned int float_precision) const
    {
        tools::classhelper::ObjectPrinter printer("NMEA GST Datagram", float_precision);

        printer.append(NMEA_Base::__printer__(float_precision));

        printer.register_section("GST attributes");
        printer.register_value("utc_time_string", get_utc_time_string(), "hhmmss.ss");
        printer.register_value("psuedorange_rms", get_psuedorange_rms(), "m");
        printer.register_value("semimajor_error", get_semimajor_error(), "m");
        printer.register_value("semiminor_error", get_semiminor_error(), "m");
        printer.register_value(
            "semimajor_error_orientation", get_semimajor_error_orientation(), "deg");
        printer.register_value("latitude_error_deviation", get_latitude_error_deviation(), "m");
        printer.register_value("longitude_error_deviation", get_longitude_error_deviation(), "m");
        printer.register_value("altitude_error_deviation", get_altitude_error_deviation(), "m");

        return printer;
    }

    // ----- class helper macros -----
    __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__
    __STREAM_DEFAULT_TOFROM_BINARY_FUNCTIONS__(NMEA_GST)
};

} // nmea_0183
} // namespace navigation
} // namespace themachinethatgoesping
