// SPDX-FileCopyrightText: 2022 Peter Urban, Tim Weiß, GEOMAR Helmholtz Centre for Ocean
// Research Kiel SPDX-FileCopyrightText: 2022 Peter Urban, Ghent University
//
// SPDX-License-Identifier: MPL-2.0

// TODO: write tests

#pragma once

#include <charconv>
#include <string>

#include <themachinethatgoesping/tools/classhelper/objectprinter.hpp>

#include "nmea_base.hpp"

namespace themachinethatgoesping {
namespace navigation {
namespace nmea_0183 {

/**
 * @brief The NMEA VHW datagram contains the vessel's compass heading and the speed relative to the
 * water.
 *
 */
class NMEA_VHW : public NMEA_Base
{

  public:
    /**
     * @brief Construct a new nmea vhw object from an existing NMEA_Base datagram
     *
     * @param base Underlying NMEA_Base datagram
     * @param check Check if the NMEA string is valid
     */
    NMEA_VHW(NMEA_Base base, bool check = false)
        : NMEA_Base(std::move(base))
    {
        if (check)
        {
            if (get_sentence_type() != "VHW")
                throw std::runtime_error(
                    fmt::format("NMEA_VHW: wrong sentence type [{}]", get_sentence_type()));
        }
        parse_fields();
    }

    // ----- NMEA VHW attributes -----
    double get_vessel_heading_true() const { return get_field_as_double(0); }
    double get_vessel_heading_magnetic() const { return get_field_as_double(2); }
    double get_speed_over_water_knots() const { return get_field_as_double(4); }
    double get_speed_over_water_kmh() const { return get_field_as_double(6); }

    // ----- binary streaming -----
    // this has to be explicit, because otherwise the compiler will use the base class version
    static NMEA_VHW from_stream(std::istream& is)
    {
        return NMEA_VHW(NMEA_Base::from_stream(is), true);
    }

    // ----- objectprinter -----
    tools::classhelper::ObjectPrinter __printer__(unsigned int float_precision) const
    {
        tools::classhelper::ObjectPrinter printer("NMEA VHW Datagram", float_precision);

        printer.append(NMEA_Base::__printer__(float_precision));

        printer.register_section("VHW attributes");
        printer.register_value("vessel_heading_true", get_vessel_heading_true(), "°, true");
        printer.register_value(
            "vessel_heading_magnetic", get_vessel_heading_magnetic(), "°, magnetic");
        printer.register_value("speed_over_water_knots", get_speed_over_water_knots(), "knots");
        printer.register_value("speed_over_water_kmh", get_speed_over_water_kmh(), "km/h");

        return printer;
    }

    // ----- class helper macros -----
    __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__
    __STREAM_DEFAULT_TOFROM_BINARY_FUNCTIONS__(NMEA_VHW)
};

} // nmea_0183
} // namespace navigation
} // namespace themachinethatgoesping
