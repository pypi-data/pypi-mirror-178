// SPDX-FileCopyrightText: 2022 Tim Weiß, GEOMAR Helmholtz Centre for Ocean Research Kiel
// SPDX-FileCopyrightText: 2022 Peter Urban, GEOMAR Helmholtz Centre for Ocean Research Kiel
// SPDX-FileCopyrightText: 2022 Peter Urban, Ghent University
//
// SPDX-License-Identifier: MPL-2.0

#pragma once

// std includes
#include <bitset>
#include <string>
#include <unordered_map>
#include <vector>

#include <boost/algorithm/string.hpp>

// xtensor includes
#include <xtensor/xadapt.hpp>
#include <xtensor/xarray.hpp>
#include <xtensor/xnoalias.hpp>
#include <xtensor/xview.hpp>

// themachinethatgoesping import
#include <themachinethatgoesping/tools/classhelper/objectprinter.hpp>
#include <themachinethatgoesping/tools/helper.hpp>
#include <themachinethatgoesping/tools/timeconv.hpp>

#include "../simrad_types.hpp"
#include "RAW3_datatypes/RAW3_datatypes.hpp"
#include "simraddatagram.hpp"

namespace themachinethatgoesping {
namespace echosounders {
namespace simrad {
namespace datagrams {

/**
 * @brief Sample binary datagram (RAW3)
 * This datagram contains the sample data for each ping. The exact datatype and size depends on the
 * Datatype field!
 *
 */
struct RAW3 : public SimradDatagram
{
    // ----- datagram content -----
    std::array<char, 128>           _ChannelID; ///< Channel identification (size is always 128)
    RAW3_datatypes::t_RAW3_DataType _Datatype;  ///< Datatype
    uint8_t _NumberOfComplexSamples; ///< Number of transducer samples per sample (used when
                                     ///< Datatype is complex)
    simrad_char _Spare_1;            ///< Spare 1
    simrad_char _Spare_2;            ///< Spare 2
    simrad_long _Offset;             ///< First sample number in the datagram
    simrad_long _Count;              ///< Number of samples in the datagram

    RAW3_datatypes::RAW3_DataVariant _SampleData; ///< Sample data

    // std::variant<xt::xtensor<simrad_float>,
    //              xt::xtensor<simrad_complex_float,2>> _Samples; ///< Sample data

  private:
    // ----- public constructors -----
    explicit RAW3(SimradDatagram header)
        : SimradDatagram(std::move(header))
    {
    }

  public:
    // ----- constructors -----
    RAW3()
        : SimradDatagram(152, simrad_long(t_SimradDatagramIdentifier::RAW3))
        , _ChannelID()
        , _Datatype(RAW3_datatypes::t_RAW3_DataType(0b00000000))
        , _NumberOfComplexSamples(0)
        , _Spare_1('\x00')
        , _Spare_2('\x00')
        , _Offset(0)
        , _Count(0)
        , _SampleData()
    {
        _ChannelID.fill('\x00');
    }
    ~RAW3() = default;

    // ----- operators -----
    bool operator==(const RAW3& other) const
    {
        using namespace tools::helper; // approx and approx_container

        return SimradDatagram::operator==(other) && _ChannelID == other._ChannelID &&
               _Datatype == other._Datatype &&
               _NumberOfComplexSamples == other._NumberOfComplexSamples &&
               _Spare_1 == other._Spare_1 && _Spare_2 == other._Spare_2 &&
               _Offset == other._Offset && _Count == other._Count &&
               _SampleData == other._SampleData;
    }
    bool operator!=(const RAW3& other) const { return !operator==(other); }

    // ----- getter setter -----
    std::string_view get_channel_id() const { return std::string_view(_ChannelID.data(), 128); }
    std::string_view get_channel_id_stripped() const
    {
        auto channel_id = get_channel_id();
        return channel_id.substr(0, channel_id.find('\x00'));
    }
    void set_channel_id(std::string_view channel_id)
    {
        if (channel_id.size() > 128)
            throw std::runtime_error("channel_id too long");

        std::copy(channel_id.begin(), channel_id.end(), _ChannelID.begin());
        // fill _ChannelID with \x00
        std::fill(_ChannelID.begin() + channel_id.size(), _ChannelID.end(), '\x00');
    }
    RAW3_datatypes::t_RAW3_DataType get_data_type() const
    {
        // set short to 0 except for the last 4 bits
        return _Datatype;
    }
    void set_data_type(RAW3_datatypes::t_RAW3_DataType data_type) { _Datatype = data_type; }

    /**
     * @brief Get the number of complex samples.
     * This corresponds to the number of transducer elements.
     * This field is only valid for complex data types.
     *
     * @return simrad_short
     */
    uint8_t get_number_of_complex_samples() const
    {
        // complex data types set at least bit 3
        if (uint8_t(_Datatype) < 4)
            return 1;

        // the number of samples is written in _Datatype bits 8-10
        return _NumberOfComplexSamples;
    }
    void set_number_of_complex_samples(uint8_t number_of_complex_samples)
    {
        _NumberOfComplexSamples = number_of_complex_samples;
    }

    simrad_char get_spare_1() const { return _Spare_1; }
    simrad_char get_spare_2() const { return _Spare_2; }
    simrad_long get_offset() const { return _Offset; }
    void        set_offset(simrad_long offset) { _Offset = offset; }
    simrad_long get_count() const { return _Count; }
    void        set_count(simrad_long count) { _Count = count; }

    /**
     * @brief Get the sample data.
     * The sample data is stored in a variant of xtensor containers.
     * The exact type depends on the data type.
     *
     * @return RAW3_datatypes::RAW3_DataVariant
     */
    RAW3_datatypes::RAW3_DataVariant& sample_data() { return _SampleData; }

    /**
     * @brief Get the sample data.
     * The sample data is stored in a variant of xtensor containers.
     * The exact type depends on the data type.
     *
     * @return RAW3_datatypes::RAW3_DataVariant
     */
    const RAW3_datatypes::RAW3_DataVariant& get_sample_data() const { return _SampleData; }
    void set_sample_data(RAW3_datatypes::RAW3_DataVariant sample_data)
    {
        _SampleData = sample_data;
    }

    // ----- file I/O -----
    RAW3_datatypes::RAW3_DataVariant read_skipped_sample_data(
        std::istream&          is,
        std::istream::pos_type header_pos) const
    {
        is.seekg(header_pos + std::istream::pos_type(152));
        return read_sample_data(is);
    }

    RAW3_datatypes::RAW3_DataVariant read_sample_data(std::istream& is) const
    {
        using namespace RAW3_datatypes;

        switch (this->_Datatype)
        {
            case t_RAW3_DataType::ComplexFloat32:
                return RAW3_DataComplexFloat32::from_stream(
                    is, this->_Count, this->_Count, this->get_number_of_complex_samples());
            case t_RAW3_DataType::PowerAndAngle:
                return RAW3_DataPowerAndAngle::from_stream(is, this->_Count, this->_Count);

            case t_RAW3_DataType::Power:
                return RAW3_DataPower::from_stream(is, this->_Count, this->_Count);
            case t_RAW3_DataType::Angle:
                return RAW3_DataAngle::from_stream(is, this->_Count, this->_Count);
            default:
                std::cerr << fmt::format("WARNING: RAW3 data type [{}] not yet implemented!",
                                         magic_enum::enum_name(this->_Datatype))
                          << std::endl;
                return RAW3_DataSkipped::from_stream(
                    is, this->_Count, this->get_data_type(), this->get_number_of_complex_samples());
        }
    }

    static RAW3 from_stream(std::istream& is, SimradDatagram header, bool skip_sample_data = false)
    {
        using namespace RAW3_datatypes;

        RAW3 datagram(std::move(header));
        is.read(datagram._ChannelID.data(), 140);

        if (skip_sample_data)
        {
            datagram._SampleData =
                RAW3_DataSkipped::from_stream(is,
                                              datagram._Count,
                                              datagram.get_data_type(),
                                              datagram.get_number_of_complex_samples());
        }
        else
        {
            datagram._SampleData = datagram.read_sample_data(is);
        }

        datagram._verify_datagram_end(is);

        return datagram;
    }

    static RAW3 from_stream(std::istream& is, bool skip_sample_data = false)
    {
        return from_stream(is,
                           SimradDatagram::from_stream(is, t_SimradDatagramIdentifier::RAW3),
                           skip_sample_data);
    }

    static RAW3 from_stream(std::istream&              is,
                            t_SimradDatagramIdentifier type,
                            bool                       skip_sample_data = false)
    {
        if (type != t_SimradDatagramIdentifier::RAW3)
            throw std::runtime_error("RAW3::from_stream: wrong datagram type");

        return from_stream(is,
                           SimradDatagram::from_stream(is, t_SimradDatagramIdentifier::RAW3),
                           skip_sample_data);
    }

    void to_stream(std::ostream& os)
    {
        //_Count = _Samples.size();
        auto data_type_size = RAW3_DataType_size(_Datatype);

        // TODO: support 16 bit complex data
        _Length = simrad_long(_Count * data_type_size * get_number_of_complex_samples() + 152);

        _DatagramType = simrad_long(t_SimradDatagramIdentifier::RAW3);
        //_ChannelID.resize(128, '\x00');

        SimradDatagram::to_stream(os);

        os.write(_ChannelID.data(), 140);

        tools::helper::visit_variant(
            _SampleData,
            [&os, this](RAW3_datatypes::RAW3_DataSkipped& data) {
                data.to_stream(
                    os, this->_Count, this->get_data_type(), this->get_number_of_complex_samples());
            },
            [&os](auto& data) { data.to_stream(os); });

        os.write(reinterpret_cast<const char*>(&_Length), sizeof(simrad_long));
    }

    // ----- objectprinter -----
    tools::classhelper::ObjectPrinter __printer__(unsigned int float_precision) const
    {
        tools::classhelper::ObjectPrinter printer("Sample binary datagram", float_precision);

        printer.append(SimradDatagram::__printer__(float_precision));

        std::string channel_id = std::string(get_channel_id());
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

        std::stringstream datatype_as_bytes;
        datatype_as_bytes << "0b" << std::bitset<8>(uint8_t(_Datatype));

        std::stringstream csamples_as_bytes;
        csamples_as_bytes << "0b" << std::bitset<8>(_NumberOfComplexSamples);

        printer.register_section("Sample datagram header");
        printer.register_string("ChannelID", channel_id);
        printer.register_string("Datatype (bytes)", datatype_as_bytes.str());
        printer.register_enum("Datatype", _Datatype);
        printer.register_value("Complex samples (bytes)", csamples_as_bytes.str());
        printer.register_value("Complex samples", _NumberOfComplexSamples);
        printer.register_value("Spare_1", _Spare_1);
        printer.register_value("Spare_2", _Spare_2);
        printer.register_value("_Offset", _Offset);
        printer.register_value("_Count", _Count);

        printer.register_section(fmt::format("Sample data ({})", magic_enum::enum_name(_Datatype)));
        printer.append(tools::helper::visit_variant(_SampleData, [float_precision](auto& data) {
            return data.__printer__(float_precision);
        }));

        return printer;
    }

    // ----- class helper macros -----
    __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__
    __STREAM_DEFAULT_TOFROM_BINARY_FUNCTIONS_NOT_CONST__(RAW3)
};

}
}
}
}