// SPDX-FileCopyrightText: 2022 Tim Weiß, GEOMAR Helmholtz Centre for Ocean Research Kiel
// SPDX-FileCopyrightText: 2022 Peter Urban, GEOMAR Helmholtz Centre for Ocean Research Kiel
// SPDX-FileCopyrightText: 2022 Peter Urban, Ghent University
//
// SPDX-License-Identifier: MPL-2.0

#pragma once

#include <complex>
#include <themachinethatgoesping/tools/helper.hpp>

/**
 * @brief Type definitions for Ek60 types according to Ek60 Reference manual
 * see also http://www.simrad.net/simrad_ref_english/default.htm
 *
 * Note: these definitions are valid for EK60 and the EK80 files.
 */

/*  */
//
namespace themachinethatgoesping {
namespace echosounders {
namespace simrad {

using simrad_char  = char;
using simrad_WORD  = uint16_t;
using simrad_short = int16_t;
using simrad_Int   = int32_t;
using simrad_long  = int32_t; // no error, long is specified as 32bit int in manual
using simrad_float = float;   // this must be 32bit!
using simrad_complex_float =
    std::complex<simrad_float>; // complex real,imaginary (used in FIL1 and RAW3)
using simrad_double   = double; // this must be 64bit!
using simrad_DWORDLON = int64_t;

enum class t_SimradDatagramIdentifier : simrad_long
{
    XML0 = 810306904, ///< Unspecified (unknown) XML datagram
    TAG0 = 809976148, ///< ???
    FIL1 = 827083078, ///< Filter datagram
    NME0 = 809848142, ///< Unspecified (unknown) NMEA datagram
    MRU0 = 810897997, ///< Motion datagram
    RAW3 = 861356370  ///< Raw sample data datagram
};

inline std::string datagram_type_to_string(simrad_long value)
{
    return tools::helper::int_as_string<simrad_long>(value);
}

inline std::string datagram_type_to_string(t_SimradDatagramIdentifier value)
{
    return tools::helper::int_as_string<simrad_long>(simrad_long(value));
}

inline simrad_long SimradDatagram_type_from_string(std::string_view value)
{
    return tools::helper::string_as_int<simrad_long>(value);
}

} // namespace simrad

// ----- interface? -----

inline std::string datagram_identifier_to_string(simrad::t_SimradDatagramIdentifier value)
{
    return tools::helper::int_as_string<simrad::simrad_long>(simrad::simrad_long(value));
}

inline std::string datagram_identifier_info(simrad::t_SimradDatagramIdentifier datagram_type)
{
    // this should work, but doesn't
    // return magic_enum::enum_contains(datagram_type);
    using simrad::t_SimradDatagramIdentifier;

    switch (datagram_type)
    {
        case t_SimradDatagramIdentifier::MRU0:
            return "Motion binary datagram";
        case t_SimradDatagramIdentifier::NME0:
            return "NMEA text datagram";
        case t_SimradDatagramIdentifier::XML0:
            return "XML0 text datagram";
        case t_SimradDatagramIdentifier::TAG0:
            return "Annotation datagram";
        case t_SimradDatagramIdentifier::FIL1:
            return "Filter binary datagram";
        case t_SimradDatagramIdentifier::RAW3:
            return "Sample binary datagram";
        default:
            return "unknown (" + std::to_string(magic_enum::enum_integer(datagram_type)) + ")";
    }
}

} // namespace echosounders
} // namespace themachinethatgoesping
