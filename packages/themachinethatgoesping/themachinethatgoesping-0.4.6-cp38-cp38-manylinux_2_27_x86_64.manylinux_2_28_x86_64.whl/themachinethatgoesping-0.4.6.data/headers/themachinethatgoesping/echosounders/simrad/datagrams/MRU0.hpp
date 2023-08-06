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
 * @brief Motion binary datagram (MRU0)
 * This datagram contains heave, roll, pitch and heading as float values.
 * Conveniently, these values can be used directly in themachinethatgoesping navigation processing
 * because they are defined in the default coordinate system / value range.
 *
 */
struct MRU0 : public SimradDatagram
{
    // ----- datagram content -----
    simrad_float _Heave   = NAN; ///< Heave in m, positive up
    simrad_float _Roll    = NAN; ///< Roll in degrees, positive port up
    simrad_float _Pitch   = NAN; ///< Pitch in degrees, positive nose up
    simrad_float _Heading = NAN; ///< Heading in degrees, 0° north, 90° east

  private:
    // ----- public constructors -----
    explicit MRU0(SimradDatagram header)
        : SimradDatagram(std::move(header))
    {
    }

  public:
    // ----- constructors -----
    MRU0()
        : SimradDatagram(12 + 4 * sizeof(simrad_float),
                         simrad_long(t_SimradDatagramIdentifier::MRU0))
    {
    }
    ~MRU0() = default;

    // ----- operators -----
    bool operator==(const MRU0& other) const
    {
        using tools::helper::approx;

        return SimradDatagram::operator==(other) && approx(_Heave, other._Heave) &&
               approx(_Roll, other._Roll) && approx(_Pitch, other._Pitch) &&
               approx(_Heading, other._Heading);
    }
    bool operator!=(const MRU0& other) const { return !operator==(other); }

    // ----- getter setter -----
    float get_heave() const { return _Heave; }
    float get_roll() const { return _Roll; }
    float get_pitch() const { return _Pitch; }
    float get_heading() const { return _Heading; }
    void  set_heave(float value) { _Heave = value; }
    void  set_roll(float value) { _Roll = value; }
    void  set_pitch(float value) { _Pitch = value; }
    void  set_heading(float value) { _Heading = value; }

    // ----- file I/O -----
    static MRU0 from_stream(std::istream& is, SimradDatagram header)
    {
        MRU0 datagram(std::move(header));
        is.read(reinterpret_cast<char*>(&datagram._Heave), 4 * sizeof(simrad_float));

        // verify the datagram is read correctly by reading the length field at the end
        datagram._verify_datagram_end(is);

        return datagram;
    }

    static MRU0 from_stream(std::istream& is)
    {
        return from_stream(is, SimradDatagram::from_stream(is, t_SimradDatagramIdentifier::MRU0));
    }

    static MRU0 from_stream(std::istream& is, t_SimradDatagramIdentifier type)
    {
        if (type != t_SimradDatagramIdentifier::MRU0)
            throw std::runtime_error("MRU0::from_stream: wrong datagram type");

        return from_stream(is, SimradDatagram::from_stream(is, t_SimradDatagramIdentifier::MRU0));
    }

    void to_stream(std::ostream& os)
    {
        _Length       = simrad_long(12 + 4 * sizeof(simrad_float));
        _DatagramType = simrad_long(t_SimradDatagramIdentifier::MRU0);
        SimradDatagram::to_stream(os);
        os.write(reinterpret_cast<const char*>(&_Heave), 4 * sizeof(simrad_float));
        os.write(reinterpret_cast<const char*>(&_Length), sizeof(simrad_long));
    }

    // ----- objectprinter -----
    tools::classhelper::ObjectPrinter __printer__(unsigned int float_precision) const
    {
        tools::classhelper::ObjectPrinter printer("Motion binary datagram", float_precision);

        printer.append(SimradDatagram::__printer__(float_precision));

        printer.register_section("Motion data");
        printer.register_value("Heave", _Heave, "m");
        printer.register_value("Roll", _Roll, "°");
        printer.register_value("Pitch", _Pitch, "°");
        printer.register_value("Heading", _Heading, "°");

        return printer;
    }

    // ----- class helper macros -----
    __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__
    __STREAM_DEFAULT_TOFROM_BINARY_FUNCTIONS_NOT_CONST__(MRU0)
};

}
}
}
}