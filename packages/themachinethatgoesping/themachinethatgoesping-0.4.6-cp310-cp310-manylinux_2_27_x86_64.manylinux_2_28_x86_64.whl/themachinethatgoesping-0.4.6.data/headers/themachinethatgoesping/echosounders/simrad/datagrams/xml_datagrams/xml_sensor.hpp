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

#include <boost/algorithm/string/find.hpp>

#include <pugixml.hpp>

// themachinethatgoesping import
#include <themachinethatgoesping/tools/classhelper/objectprinter.hpp>
#include <themachinethatgoesping/tools/classhelper/stream.hpp>
#include <themachinethatgoesping/tools/helper.hpp>
#include <themachinethatgoesping/tools/timeconv.hpp>

#include "helper.hpp"
#include "xml_node.hpp"

namespace themachinethatgoesping {
namespace echosounders {
namespace simrad {
namespace datagrams {
namespace xml_datagrams {

/**
 * @brief XML base datagram
 *
 */
struct XML_Sensor
{
    bool        IsManual    = false;
    double      ManualValue = NAN;
    std::string Type;

    int32_t unknown_children   = 0;
    int32_t unknown_attributes = 0;

  public:
    // ----- constructors -----
    XML_Sensor() = default;
    XML_Sensor(const pugi::xml_node& node) { initialize(node); }
    ~XML_Sensor() = default;

    void initialize(const pugi::xml_node& root_node)
    {
        if (strcmp(root_node.name(), "Sensor"))
        {
            throw std::runtime_error(std::string("XML_Sensor: wrong root node type '") +
                                     root_node.name() + "'");
        }
        unknown_attributes = 0;
        unknown_children   = 0; // there should be no child

        // there should only be one child for this node
        for (const auto& node : root_node.children())
        {
            std::cerr << "WARNING: [Sensor] Unknown child: " << node.name() << std::endl;

            unknown_children = 1;
        }

        for (const auto& attr : root_node.attributes())
        {
            std::string_view name = attr.name();
            if (name == "IsManual")
            {
                IsManual = std::stoi(attr.value()); // TODO: is this only 0/1 or also false/true?
                continue;
            }
            if (name == "ManualValue")
            {
                ManualValue = tools::helper::string_to_double(attr.value());
                continue;
            }
            if (name == "Type")
            {
                Type = attr.value();
                continue;
            }
            std::cerr << "WARNING: [Sensor] Unknown attribute: " << name << std::endl;
            unknown_attributes += 1;
        }
    }

    bool parsed_completely() const { return unknown_children == 0 && unknown_attributes == 0; }

    // ----- file I/O -----
    static XML_Sensor from_stream(std::istream& is)
    {
        XML_Sensor xml;
        is.read(reinterpret_cast<char*>(&xml.IsManual), sizeof(xml.IsManual));
        is.read(reinterpret_cast<char*>(&xml.ManualValue), sizeof(xml.ManualValue));
        xml.Type = tools::classhelper::stream::container_from_stream<std::string>(is);

        is.read(reinterpret_cast<char*>(&xml.unknown_children), sizeof(xml.unknown_children));
        is.read(reinterpret_cast<char*>(&xml.unknown_attributes), sizeof(xml.unknown_attributes));

        return xml;
    }

    void to_stream(std::ostream& os) const
    {
        os.write(reinterpret_cast<const char*>(&IsManual), sizeof(IsManual));
        os.write(reinterpret_cast<const char*>(&ManualValue), sizeof(ManualValue));
        tools::classhelper::stream::container_to_stream(os, Type);

        os.write(reinterpret_cast<const char*>(&unknown_children), sizeof(unknown_children));
        os.write(reinterpret_cast<const char*>(&unknown_attributes), sizeof(unknown_attributes));
    }

    // ----- operators -----
    bool operator==(const XML_Sensor& other) const
    {
        return IsManual == other.IsManual &&
               tools::helper::approx(ManualValue, other.ManualValue) && Type == other.Type;
        // && unknown_children == other.unknown_children &&
        // unknown_attributes == other.unknown_attributes;
    }
    bool operator!=(const XML_Sensor& other) const { return !operator==(other); }

    // ----- objectprinter -----
    tools::classhelper::ObjectPrinter __printer__(unsigned int float_precision) const
    {
        tools::classhelper::ObjectPrinter printer("EK80 XML0 Sensor", float_precision);
        printer.register_value("IsManual", IsManual);
        printer.register_value("ManualValue", ManualValue);
        printer.register_string("Type", Type);

        return printer;
    }

    // ----- class helper macros -----
    __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__ __STREAM_DEFAULT_TOFROM_BINARY_FUNCTIONS__(
        XML_Sensor)
};

}
}
}
}
}