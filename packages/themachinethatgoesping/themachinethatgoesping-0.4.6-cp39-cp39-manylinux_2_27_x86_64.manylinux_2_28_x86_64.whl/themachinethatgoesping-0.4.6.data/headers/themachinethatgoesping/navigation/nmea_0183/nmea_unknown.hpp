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
 * @brief Thie NMEA datagram was not yet implemented in themachinethatgoesping.
 *
 */
class NMEA_Unknown : public NMEA_Base
{

  public:
    /**
     * @brief Construct a new nmea Unknown object from an existing NMEA_Base datagram
     *
     * @param base Underlying NMEA_Base datagram
     * @param check Check if the NMEA string is valid
     */
    NMEA_Unknown(NMEA_Base base, [[maybe_unused]] bool check = false)
        : NMEA_Base(std::move(base))
    {
        // if (check) {
        // }
        parse_fields();
    }

    // ----- binary streaming -----
    // this has to be explicit, because otherwise the compiler will use the base class version
    static NMEA_Unknown from_stream(std::istream& is)
    {
        return NMEA_Unknown(NMEA_Base::from_stream(is), true);
    }

    // ----- objectprinter -----
    tools::classhelper::ObjectPrinter __printer__(unsigned int float_precision) const
    {
        tools::classhelper::ObjectPrinter printer("NMEA Datagram (not implemented)",
                                                  float_precision);

        printer.append(NMEA_Base::__printer__(float_precision));
        return printer;
    }

    // ----- class helper macros -----
    __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__
    __STREAM_DEFAULT_TOFROM_BINARY_FUNCTIONS__(NMEA_Unknown)
};

} // nmea_0183
} // namespace navigation
} // namespace themachinethatgoesping
