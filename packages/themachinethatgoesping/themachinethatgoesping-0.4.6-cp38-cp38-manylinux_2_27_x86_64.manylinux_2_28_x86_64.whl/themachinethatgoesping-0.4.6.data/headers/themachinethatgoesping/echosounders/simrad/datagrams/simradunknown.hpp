// SPDX-FileCopyrightText: 2022 Tim Weiß, GEOMAR Helmholtz Centre for Ocean Research Kiel
// SPDX-FileCopyrightText: 2022 Peter Urban, GEOMAR Helmholtz Centre for Ocean Research Kiel
// SPDX-FileCopyrightText: 2022 Peter Urban, Ghent University
//
// SPDX-License-Identifier: MPL-2.0

#pragma once

// std includes
#include <string>
#include <unordered_map>
#include <vector>

// themachinethatgoesping import
#include <themachinethatgoesping/tools/classhelper/objectprinter.hpp>
#include <themachinethatgoesping/tools/classhelper/stream.hpp>
#include <themachinethatgoesping/tools/timeconv.hpp>

#include "../simrad_types.hpp"
#include "simraddatagram.hpp"

namespace themachinethatgoesping {
namespace echosounders {
namespace simrad {
namespace datagrams {

struct SimradUnknown : public SimradDatagram
{
    // ----- datagram content -----
    std::string raw_content;

  private:
    // ----- private constructors -----
    explicit SimradUnknown(SimradDatagram header)
        : SimradDatagram(std::move(header))
    {
    }

  public:
    // ----- public constructors -----
    SimradUnknown()  = default;
    ~SimradUnknown() = default;

    // ----- operators -----
    bool operator==(const SimradUnknown& other) const
    {
        return SimradDatagram::operator==(other) && raw_content == other.raw_content;
    }
    bool operator!=(const SimradUnknown& other) const { return !operator==(other); }

    static SimradUnknown from_stream(std::istream& is, SimradDatagram header)
    {
        SimradUnknown datagram(std::move(header));

        if (datagram._Length > 12)
            datagram.raw_content.resize(size_t(datagram._Length - 12));
        else
            throw std::runtime_error("ERROR[SimradUnknown::from_stream]: _Length is too small");

        is.read(datagram.raw_content.data(), datagram.raw_content.size());

        // verify the datagram is read correctly by reading the length field at the end
        datagram._verify_datagram_end(is);

        return datagram;
    }

    static SimradUnknown from_stream(std::istream& is)
    {
        return from_stream(is, SimradDatagram::from_stream(is));
    }

    static SimradUnknown from_stream(std::istream&              is,
                                     t_SimradDatagramIdentifier datagram_identifier)
    {
        return from_stream(is, std::move(SimradDatagram::from_stream(is, datagram_identifier)));
    }

    void to_stream(std::ostream& os)
    {
        _Length = simrad_long(12 + raw_content.size());
        SimradDatagram::to_stream(os);

        os.write(raw_content.data(), raw_content.size());
        os.write(reinterpret_cast<const char*>(&_Length), sizeof(simrad_long));
    }

    // ----- objectprinter -----
    tools::classhelper::ObjectPrinter __printer__(unsigned int float_precision) const
    {
        tools::classhelper::ObjectPrinter printer("SimradUnknown", float_precision);

        printer.append(SimradDatagram::__printer__(float_precision));

        return printer;
    }

    // ----- class helper macros -----
    __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__
    __STREAM_DEFAULT_TOFROM_BINARY_FUNCTIONS_NOT_CONST__(SimradUnknown)
};

} // namespace datagrams
} // namespace simrad
} // namespace echosounders
} // namespace themachinethatgoesping
