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
#include <themachinethatgoesping/tools/helper.hpp>
#include <themachinethatgoesping/tools/timeconv.hpp>

#include "../simrad_types.hpp"
#include "simraddatagram.hpp"

namespace themachinethatgoesping {
namespace echosounders {
namespace simrad {
namespace datagrams {

/**
 * @brief Motion binary datagram (TAG0)
 * This datagram contains heave, roll, pitch and heading as float values.
 * Conveniently, these values can be used directly in themachinethatgoesping navigation processing
 * because they are defined in the default coordinate system / value range.
 *
 */
struct TAG0 : public SimradDatagram
{
    // ----- datagram content -----
    std::string _Text; ///< _Text annotation string (e.g. interesting fish shoal in echogram)

  private:
    // ----- public constructors -----
    explicit TAG0(SimradDatagram header)
        : SimradDatagram(std::move(header))
    {
    }

  public:
    // ----- constructors -----
    TAG0()
        : SimradDatagram(12, simrad_long(t_SimradDatagramIdentifier::TAG0))
    {
    }
    TAG0(std::string text_anotation)
        : SimradDatagram(simrad_long(12 + text_anotation.size()),
                         simrad_long(t_SimradDatagramIdentifier::TAG0))
        , _Text(std::move(text_anotation))
    {
    }
    ~TAG0() = default;

    // ----- operators -----
    bool operator==(const TAG0& other) const
    {
        return SimradDatagram::operator==(other) && _Text == other._Text;
    }
    bool operator!=(const TAG0& other) const { return !operator==(other); }

    // ----- getter setter -----
    const std::string& get_text() const { return _Text; }
    void               set_text(std::string text) { _Text = std::move(text); }

    // ----- file I/O -----
    static TAG0 from_stream(std::istream& is, SimradDatagram header)
    {
        TAG0 datagram(std::move(header));
        datagram._Text.resize(datagram._Length - 12);
        is.read(datagram._Text.data(), datagram._Text.size());

        // verify the datagram is read correctly by reading the length field at the end
        datagram._verify_datagram_end(is);

        return datagram;
    }

    static TAG0 from_stream(std::istream& is)
    {
        return from_stream(is, SimradDatagram::from_stream(is, t_SimradDatagramIdentifier::TAG0));
    }

    static TAG0 from_stream(std::istream& is, t_SimradDatagramIdentifier type)
    {
        if (type != t_SimradDatagramIdentifier::TAG0)
            throw std::runtime_error("TAG0::from_stream: wrong datagram type");

        return from_stream(is, SimradDatagram::from_stream(is, t_SimradDatagramIdentifier::TAG0));
    }

    void to_stream(std::ostream& os)
    {
        _Length       = simrad_long(12 + _Text.size());
        _DatagramType = simrad_long(t_SimradDatagramIdentifier::TAG0);
        SimradDatagram::to_stream(os);
        os.write(_Text.data(), _Text.size());
        os.write(reinterpret_cast<const char*>(&_Length), sizeof(simrad_long));
    }

    // ----- objectprinter -----
    tools::classhelper::ObjectPrinter __printer__(unsigned int float_precision) const
    {
        tools::classhelper::ObjectPrinter printer("Annotation datagram", float_precision);

        printer.append(SimradDatagram::__printer__(float_precision));

        printer.register_section("Annotation data");
        printer.register_string("Text", _Text);

        return printer;
    }

    // ----- class helper macros -----
    __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__
    __STREAM_DEFAULT_TOFROM_BINARY_FUNCTIONS_NOT_CONST__(TAG0)
};

}
}
}
}