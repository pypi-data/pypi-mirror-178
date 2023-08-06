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

#include <boost/algorithm/string.hpp>

// xtensor includes
#include <xtensor/xadapt.hpp>
#include <xtensor/xarray.hpp>
#include <xtensor/xio.hpp>
#include <xtensor/xview.hpp>

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
 * @brief Filter binary datagram (FIL1)
 * This datagram contains filter coefficients used by the EK80 to filter the received signal.
 *
 */
struct FIL1 : public SimradDatagram
{
    // ----- datagram content -----
    simrad_short _Stage   = '\x00';      ///< Filter stage number
    simrad_char  _Spare_1 = '\x00';      ///< For future expansions
    simrad_char  _Spare_2 = '\x00';      ///< For future expansions
    std::string  _ChannelID;             ///< Channel identification (size is always 128)
    simrad_short _NoOfCoefficients = 0;  ///< Number of complex filter coefficients
    simrad_short _DecimationFactor = -1; ///< Filter decimation factor

    xt::xtensor<simrad_float, 2> _Coefficients; ///< Filter coefficients, ...)

  private:
    // ----- public constructors -----
    explicit FIL1(SimradDatagram header)
        : SimradDatagram(std::move(header))
    {
    }

  public:
    // ----- constructors -----
    FIL1()
        : SimradDatagram(148, simrad_long(t_SimradDatagramIdentifier::FIL1))
    {
    }
    ~FIL1() = default;

    // ----- operators -----
    bool operator==(const FIL1& other) const
    {
        using namespace tools::helper; // approx and approx_container

        return SimradDatagram::operator==(other) && _Stage == other._Stage &&
               _Spare_1 == other._Spare_1 && _Spare_2 == other._Spare_2 &&
               _ChannelID == other._ChannelID && _NoOfCoefficients == other._NoOfCoefficients &&
               _DecimationFactor == other._DecimationFactor &&
               approx_container(xt::flatten(_Coefficients), xt::flatten(other._Coefficients));
    }
    bool operator!=(const FIL1& other) const { return !operator==(other); }

    // ----- getter setter -----
    simrad_short                        get_stage() const { return _Stage; }
    simrad_char                         get_spare_1() const { return _Spare_1; }
    simrad_char                         get_spare_2() const { return _Spare_2; }
    std::string                         get_channel_id() const { return _ChannelID; }
    simrad_short                        get_no_of_coefficients() const { return _NoOfCoefficients; }
    simrad_short                        get_decimation_factor() const { return _DecimationFactor; }
    const xt::xtensor<simrad_float, 2>& get_coefficients() const { return _Coefficients; }

    void set_stage(simrad_short stage) { _Stage = stage; }
    void set_spare_1(simrad_char spare_1) { _Spare_1 = spare_1; }
    void set_spare_2(simrad_char spare_2) { _Spare_2 = spare_2; }
    void set_channel_id(std::string channel_id) { _ChannelID = channel_id; }
    void set_no_of_coefficients(simrad_short no_of_coefficients)
    {
        _NoOfCoefficients = no_of_coefficients;
    }
    void set_decimation_factor(simrad_short decimation_factor)
    {
        _DecimationFactor = decimation_factor;
    }
    void set_coefficients(xt::xtensor<simrad_float, 2> coefficients)
    {
        _Coefficients = std::move(coefficients);
    }

    // ----- file I/O -----
    static FIL1 from_stream(std::istream& is, SimradDatagram header)
    {
        FIL1 datagram(std::move(header));
        datagram._ChannelID.resize(128);

        is.read(reinterpret_cast<char*>(&datagram._Stage), sizeof(datagram._Stage));
        is.read(reinterpret_cast<char*>(&datagram._Spare_1), sizeof(datagram._Spare_1));
        is.read(reinterpret_cast<char*>(&datagram._Spare_2), sizeof(datagram._Spare_2));
        is.read(datagram._ChannelID.data(), datagram._ChannelID.size());
        is.read(reinterpret_cast<char*>(&datagram._NoOfCoefficients),
                sizeof(datagram._NoOfCoefficients));
        is.read(reinterpret_cast<char*>(&datagram._DecimationFactor),
                sizeof(datagram._DecimationFactor));

        int size = datagram._NoOfCoefficients * sizeof(simrad_float) * 2;
        if (size + 148 != datagram._Length)
            throw std::runtime_error(
                fmt::format("FIL1: size mismatch (NoOfCoefficients {}/{} vs datagram Length {})",
                            datagram._NoOfCoefficients,
                            size,
                            datagram._Length));

        using xt_shape = xt::xtensor<simrad_float, 2>::shape_type;
        datagram._Coefficients =
            xt::empty<simrad_float>(xt_shape({ size_t(datagram._NoOfCoefficients), 2 }));

        is.read(reinterpret_cast<char*>(datagram._Coefficients.data()),
                datagram._Coefficients.size() * sizeof(simrad_float));

        // verify the datagram is read correctly by reading the length field at the end
        datagram._verify_datagram_end(is);

        return datagram;
    }

    static FIL1 from_stream(std::istream& is)
    {
        return from_stream(is, SimradDatagram::from_stream(is, t_SimradDatagramIdentifier::FIL1));
    }

    static FIL1 from_stream(std::istream& is, t_SimradDatagramIdentifier type)
    {
        if (type != t_SimradDatagramIdentifier::FIL1)
            throw std::runtime_error("FIL1::from_stream: wrong datagram type");

        return from_stream(is, SimradDatagram::from_stream(is, t_SimradDatagramIdentifier::FIL1));
    }

    void to_stream(std::ostream& os)
    {
        _NoOfCoefficients = simrad_short(_Coefficients.size() / 2);

        _Length       = simrad_long(_Coefficients.size() * sizeof(simrad_float) + 148);
        _DatagramType = simrad_long(t_SimradDatagramIdentifier::FIL1);
        _ChannelID.resize(128, '\x00');

        SimradDatagram::to_stream(os);

        os.write(reinterpret_cast<char*>(&_Stage), sizeof(_Stage));
        os.write(reinterpret_cast<char*>(&_Spare_1), sizeof(_Spare_1));
        os.write(reinterpret_cast<char*>(&_Spare_2), sizeof(_Spare_2));
        os.write(_ChannelID.data(), _ChannelID.size());
        os.write(reinterpret_cast<char*>(&_NoOfCoefficients), sizeof(_NoOfCoefficients));
        os.write(reinterpret_cast<char*>(&_DecimationFactor), sizeof(_DecimationFactor));
        os.write(reinterpret_cast<char*>(_Coefficients.data()),
                 _Coefficients.size() * sizeof(simrad_float));
        os.write(reinterpret_cast<char*>(&_Length), sizeof(_Length));
    }

    // ----- objectprinter -----
    tools::classhelper::ObjectPrinter __printer__(unsigned int float_precision) const
    {
        tools::classhelper::ObjectPrinter printer("Filter binary datagram (FIL1)", float_precision);

        printer.append(SimradDatagram::__printer__(float_precision));

        std::string channel_id = _ChannelID;
        // remove all non ascii characters
        channel_id.erase(std::remove_if(channel_id.begin(),
                                        channel_id.end(),
                                        [](char c) { return !std::isprint(c); }),
                         channel_id.end());
        // remove all white spaces
        channel_id.erase(std::remove_if(channel_id.begin(),
                                        channel_id.end(),
                                        [](char c) { return std::isspace(c); }),
                         channel_id.end());

        printer.register_section("Filter datagram content");
        printer.register_value("Stage", _Stage);
        printer.register_value("Spare_1", _Spare_1);
        printer.register_value("Spare_2", _Spare_2);
        printer.register_string("ChannelID", channel_id);
        printer.register_value("NoOfCoefficients", _NoOfCoefficients);
        printer.register_value("DecimationFactor", _DecimationFactor);

        printer.register_section("Filter coefficients");
        std::stringstream ss;
        ss << _Coefficients;
        printer.register_string("Coefficients", ss.str());

        return printer;
    }

    // ----- class helper macros -----
    __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__
    __STREAM_DEFAULT_TOFROM_BINARY_FUNCTIONS_NOT_CONST__(FIL1)
};

}
}
}
}