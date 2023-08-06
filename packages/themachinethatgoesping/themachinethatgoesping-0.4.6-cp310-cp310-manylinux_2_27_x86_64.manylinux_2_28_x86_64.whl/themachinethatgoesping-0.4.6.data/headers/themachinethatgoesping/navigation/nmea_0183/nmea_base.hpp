// SPDX-FileCopyrightText: 2022 Peter Urban, Tim Weiß, GEOMAR Helmholtz Centre for Ocean
// Research Kiel SPDX-FileCopyrightText: 2022 Peter Urban, Ghent University
//
// SPDX-License-Identifier: MPL-2.0

#pragma once

#include <charconv>
#include <string>

#include <themachinethatgoesping/tools/classhelper/objectprinter.hpp>
#include <themachinethatgoesping/tools/classhelper/stream.hpp>

#include <themachinethatgoesping/tools/helper.hpp>

namespace themachinethatgoesping {
namespace navigation {
namespace nmea_0183 {

class NMEA_Base
{
  protected:
    std::string      _sentence;
    std::vector<int> _fields;

  public:
    NMEA_Base() = default;

    NMEA_Base(std::string data)
        : _sentence(std::move(data))
    {
        parse_fields();
    }

    // NMEA_Base(std::string&& data)
    //     : _sentence(std::move(data))
    // {
    //     parse_fields();
    // }

    static NMEA_Base from_stream(std::istream& is, size_t length)
    {
        NMEA_Base nmea_base;
        nmea_base._sentence.resize(length);
        is.read(nmea_base._sentence.data(), nmea_base._sentence.size());

        return nmea_base;
    }

    static NMEA_Base from_stream(std::istream& is)
    {
        NMEA_Base nmea_base;
        size_t    size;
        is.read(reinterpret_cast<char*>(&size), sizeof(size));
        nmea_base._sentence.resize(size);
        is.read(nmea_base._sentence.data(), nmea_base._sentence.size());

        return nmea_base;
    }

    void to_stream(std::ostream& os) const
    {
        size_t size = this->size();
        os.write(reinterpret_cast<char*>(&size), sizeof(size));
        os.write(this->_sentence.data(), this->_sentence.size());
    }

    void to_stream_dont_write_size(std::ostream& os) const
    {
        os.write(this->_sentence.data(), this->_sentence.size());
    }

    // operators
    bool   operator==(const NMEA_Base& other) const { return _sentence == other._sentence; }
    bool   operator!=(const NMEA_Base& other) const { return _sentence != other._sentence; }
    size_t size() const { return _sentence.size(); }

    void parse_fields()
    {
        _fields.clear();
        // find all ','
        int i = 0;
        for (; i < int(_sentence.size()); i++)
        {
            if (_sentence[i] == ',')
                _fields.push_back(i);
            if (_sentence[i] == '\x00')
                break;
        }
        _fields.push_back(i);
    };

    std::string_view get_field(size_t index) const
    {
        if (index < _fields.size() - 1)
            return std::string_view(_sentence).substr(_fields[index] + 1,
                                                      _fields[index + 1] - _fields[index] - 1);

        return "";
    }

    double get_field_as_double(size_t index) const
    {
        return themachinethatgoesping::tools::helper::string_to_double(get_field(index));
    }

    int get_field_as_int(size_t index) const
    {
        try
        {
            return std::stoi(std::string(get_field(index)));
        }
        catch (...)
        {
            return 0;
        }
    }

    std::string_view get_sender_id() const
    {
        try
        {
            if (_sentence.at(0) != '$')
                return "invalid";

            return std::string_view(_sentence).substr(1, 2);
        }
        catch (...)
        {
            return "invalid";
        }
    }

    std::string_view get_sentence_type() const
    {
        try
        {
            if (_sentence.at(0) != '$')
                return "invalid";

            return std::string_view(_sentence).substr(3, 3);
        }
        catch (...)
        {
            return "invalid";
        }
    }

    std::string_view get_sentence_id() const
    {
        try
        {
            if (_sentence.at(0) != '$')
                return "invalid";

            return std::string_view(_sentence).substr(1, 5);
        }
        catch (...)
        {
            return "invalid";
        }
    }

    std::string_view get_sentence() const { return std::string_view(_sentence); }

    // ----- objectprinter -----
    tools::classhelper::ObjectPrinter __printer__(unsigned int float_precision) const
    {
        tools::classhelper::ObjectPrinter printer("NMEA sentence", float_precision);

        printer.register_value("Sender", get_sender_id(), "");
        printer.register_value("Type", get_sentence_type(), "");
        printer.register_value("Full sentence", get_sentence(), "");

        return printer;
    }

    // ----- class helper macros -----
    __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__
    __STREAM_DEFAULT_TOFROM_BINARY_FUNCTIONS__(NMEA_Base)
};

} // nmea_0183
} // namespace navigation
} // namespace themachinethatgoesping
