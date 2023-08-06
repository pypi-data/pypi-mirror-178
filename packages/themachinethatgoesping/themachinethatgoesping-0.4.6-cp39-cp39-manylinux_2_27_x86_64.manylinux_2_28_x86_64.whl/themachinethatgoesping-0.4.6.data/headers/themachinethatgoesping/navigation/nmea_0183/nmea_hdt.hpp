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
 * @brief The NMEA HDT datagram contains the true vessel heading typically received from a compass.
 *
 */
class NMEA_HDT : public NMEA_Base
{

  public:
    /**
     * @brief Construct a new nmea hdt object from an existing NMEA_Base datagram
     *
     * @param base Underlying NMEA_Base datagram
     * @param check Check if the NMEA string is valid
     */
    NMEA_HDT(NMEA_Base base, bool check = false)
        : NMEA_Base(std::move(base))
    {
        if (check)
        {
            if (get_sentence_type() != "HDT")
                throw std::runtime_error(
                    fmt::format("NMEA_HDT: wrong sentence type [{}]", get_sentence_type()));
        }
        parse_fields();
    }

    // ----- NMEA HDT attributes -----
    double get_heading_degrees_true() const { return get_field_as_double(0); }

    // ----- binary streaming -----
    // this has to be explicit, because otherwise the compiler will use the base class version
    static NMEA_HDT from_stream(std::istream& is)
    {
        return NMEA_HDT(NMEA_Base::from_stream(is), true);
    }

    // ----- objectprinter -----
    tools::classhelper::ObjectPrinter __printer__(unsigned int float_precision) const
    {
        tools::classhelper::ObjectPrinter printer("NMEA HDT Datagram", float_precision);

        printer.append(NMEA_Base::__printer__(float_precision));

        printer.register_section("HDT attributes");
        printer.register_value("heading_degrees_true", get_heading_degrees_true());

        return printer;
    }

    // ----- class helper macros -----
    __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__
    __STREAM_DEFAULT_TOFROM_BINARY_FUNCTIONS__(NMEA_HDT)
};

} // nmea_0183
} // namespace navigation
} // namespace themachinethatgoesping
