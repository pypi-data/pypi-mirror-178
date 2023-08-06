// SPDX-FileCopyrightText: 2022 Tim Weiß, GEOMAR Helmholtz Centre for Ocean Research Kiel
// SPDX-FileCopyrightText: 2022 Peter Urban, GEOMAR Helmholtz Centre for Ocean Research Kiel
// SPDX-FileCopyrightText: 2022 Peter Urban, Ghent University
//
// SPDX-License-Identifier: MPL-2.0

#pragma once

#include "datagrams/FIL1.hpp"
#include "datagrams/MRU0.hpp"
#include "datagrams/NME0.hpp"
#include "datagrams/RAW3.hpp"
#include "datagrams/TAG0.hpp"
#include "datagrams/XML0.hpp"
#include "datagrams/simraddatagram.hpp"
#include "datagrams/simradunknown.hpp"
#include "simrad_types.hpp"

#include <pybind11/pybind11.h>

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

namespace datagrams {

using t_SimradDatagramVariant =
    std::variant<SimradDatagram, NME0, XML0, MRU0, RAW3, FIL1, TAG0, SimradUnknown>;

struct SimradDatagramVariant
{
    t_SimradDatagramVariant _datagram_variant;

  public:
    SimradDatagramVariant() = default;
    SimradDatagramVariant(t_SimradDatagramVariant&& datagram_variant)
        : _datagram_variant(std::move(datagram_variant))
    {
    }

    static t_SimradDatagramVariant from_stream(std::istream&              is,
                                               t_SimradDatagramIdentifier datagram_type)
    {
        switch (datagram_type)
        {
            case t_SimradDatagramIdentifier::MRU0:
                return t_SimradDatagramVariant(MRU0::from_stream(is));
            case t_SimradDatagramIdentifier::NME0:
                return t_SimradDatagramVariant(NME0::from_stream(is));
            case t_SimradDatagramIdentifier::XML0:
                return t_SimradDatagramVariant(XML0::from_stream(is));
            case t_SimradDatagramIdentifier::TAG0:
                return t_SimradDatagramVariant(TAG0::from_stream(is));
            case t_SimradDatagramIdentifier::FIL1:
                return t_SimradDatagramVariant(FIL1::from_stream(is));
            case t_SimradDatagramIdentifier::RAW3:
                return t_SimradDatagramVariant(RAW3::from_stream(is));
            default:
                return t_SimradDatagramVariant(SimradUnknown::from_stream(is, datagram_type));
        }
    }

    /**
     * @brief This is the visitor function that  tries to convert the internal variant to the
     * specified type.
     *
     * @tparam t_ProgressBar
     * @param progress_bar ProgressBar class that is derived from I_ProgressBar
     * @return I_ProgressBar&
     */
    template<typename t_Datagram>
    t_Datagram& operator()() const
    {
        return t_Datagram(_datagram_variant);
    }
};

} // namespace datagrams
} // namespace simrad
} // namespace echosounders
} // namespace themachinethatgoesping
