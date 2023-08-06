// SPDX-FileCopyrightText: 2022 Peter Urban, Tim Weiß, GEOMAR Helmholtz Centre for Ocean
// Research Kiel SPDX-FileCopyrightText: 2022 Peter Urban, Ghent University
//
// SPDX-License-Identifier: MPL-2.0

#pragma once

#include <charconv>
#include <string>

#include <themachinethatgoesping/tools/classhelper/objectprinter.hpp>

#include "nmea_base.hpp"

namespace themachinethatgoesping {
namespace navigation {
namespace nmea_0183 {

/**
 * @brief The NMEA VBW datagram contains the vessels course and speed over ground.
 *
 */
class NMEA_VTG : public NMEA_Base
{

  public:
    /**
     * @brief Construct a new nmea vtg object from an existing NMEA_Base datagram
     *
     * @param base Underlying NMEA_Base datagram
     * @param check Check if the NMEA string is valid
     */
    NMEA_VTG(NMEA_Base base, bool check = false)
        : NMEA_Base(std::move(base))
    {
        if (check)
        {
            if (get_sentence_type() != "VTG")
                throw std::runtime_error(
                    fmt::format("NMEA_VTG: wrong sentence type [{}]", get_sentence_type()));
        }
        parse_fields();
    }

    // ----- NMEA VTG attributes -----
    double get_course_over_ground_degrees_true() const { return get_field_as_double(0); }
    double get_course_over_ground_degrees_magnetic() const { return get_field_as_double(2); }
    double get_speed_over_ground_knots() const { return get_field_as_double(4); }
    double get_speed_over_ground_kmh() const { return get_field_as_double(6); }

    char get_mode() const
    {
        try
        {
            return get_field(8)[0];
        }
        catch ([[maybe_unused]] std::out_of_range& e)
        {
            return '\x00';
        }
    }
    std::string get_mode_explained() const
    {
        switch (get_mode())
        {
            case 'A':
                return "Autonomous";
            case 'D':
                return "Differential";
            case 'E':
                return "Estimated";
            case 'M':
                return "Manual";
            case 'S':
                return "Simulated";
            case 'N':
                return "Data not valid";
            default:
                return "Unknown";
        }
    }

    // ----- binary streaming -----
    // this has to be explicit, because otherwise the compiler will use the base class version
    static NMEA_VTG from_stream(std::istream& is)
    {
        return NMEA_VTG(NMEA_Base::from_stream(is), true);
    }

    // ----- objectprinter -----
    tools::classhelper::ObjectPrinter __printer__(unsigned int float_precision) const
    {
        tools::classhelper::ObjectPrinter printer("NMEA VTG Datagram", float_precision);

        printer.append(NMEA_Base::__printer__(float_precision));

        printer.register_section("VTG attributes");
        printer.register_value(
            "course_over_ground_degrees_true", get_course_over_ground_degrees_true(), "° (true)");
        printer.register_value("course_over_ground_degrees_magnetic",
                               get_course_over_ground_degrees_magnetic(),
                               "° (magnetic)");
        printer.register_value("speed_over_ground_knots", get_speed_over_ground_knots(), "knots");
        printer.register_value("speed_over_ground_kmh", get_speed_over_ground_kmh(), "km/h");
        printer.register_value("mode", get_mode(), get_mode_explained());

        return printer;
    }

    // ----- class helper macros -----
    __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__
    __STREAM_DEFAULT_TOFROM_BINARY_FUNCTIONS__(NMEA_VTG)
};

} // nmea_0183
} // namespace navigation
} // namespace themachinethatgoesping
