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
#include "xml_configuration_sensor_telegramvalue.hpp"
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
struct XML_Configuration_Sensor_Telegram
{
    bool        Enabled = false;
    std::string SubscriptionPath;
    std::string Type;
    std::string SensorType;
    std::string Name;

    std::vector<XML_Configuration_Sensor_TelegramValue> Values;

    int32_t unknown_children   = 0;
    int32_t unknown_attributes = 0;

  public:
    // ----- constructors -----
    XML_Configuration_Sensor_Telegram() = default;
    XML_Configuration_Sensor_Telegram(const pugi::xml_node& node) { initialize(node); }
    ~XML_Configuration_Sensor_Telegram() = default;

    void initialize(const pugi::xml_node& root_node)
    {
        if (strcmp(root_node.name(), "Telegram"))
        {
            throw std::runtime_error(
                std::string("XML_Configuration_Sensor_Telegram: wrong root node type '") +
                root_node.name() + "'");
        }
        unknown_attributes = 0;
        unknown_children   = 0; // there should only be TelegramValue nodes

        // there should only be one child for this node
        for (const auto& node : root_node.children())
        {
            if (strcmp(node.name(), "Value"))
            {
                std::cerr << "WARNING: [Configuration_Sensor_Telegram] Unknown child: "
                          << node.name() << std::endl;

                unknown_children = 1;

                continue;
            }

            Values.emplace_back(node);
        }

        for (auto& attr : root_node.attributes())
        {
            std::string_view name = attr.name();
            if (name == "Enabled")
            {
                Enabled = std::stoi(
                    attr.value()); // TODO: can this value only be 0 and 1 or also true and false?
                continue;
            }
            if (name == "SubscriptionPath")
            {
                SubscriptionPath = attr.value();
                continue;
            }
            if (name == "Type")
            {
                Type = attr.value();
                continue;
            }
            if (name == "SensorType")
            {
                SensorType = attr.value();
                continue;
            }
            if (name == "Name")
            {
                Name = attr.value();
                continue;
            }

            std::cerr << "WARNING: [Configuration_Sensor_Telegram] Unknown attribute: " << name
                      << std::endl;
            unknown_attributes += 1;
        }
    }

    bool parsed_completely() const { return unknown_children == 0 && unknown_attributes == 0; }

    // ----- file I/O -----
    static XML_Configuration_Sensor_Telegram from_stream(std::istream& is)
    {
        XML_Configuration_Sensor_Telegram xml;

        is.read(reinterpret_cast<char*>(&xml.Enabled), sizeof(xml.Enabled));
        xml.SubscriptionPath = tools::classhelper::stream::container_from_stream<std::string>(is);
        xml.Type             = tools::classhelper::stream::container_from_stream<std::string>(is);
        xml.SensorType       = tools::classhelper::stream::container_from_stream<std::string>(is);
        xml.Name             = tools::classhelper::stream::container_from_stream<std::string>(is);

        size_t size;
        is.read(reinterpret_cast<char*>(&size), sizeof(size));
        xml.Values.resize(size);
        for (auto& value : xml.Values)
        {
            value = XML_Configuration_Sensor_TelegramValue::from_stream(is);
        }

        is.read(reinterpret_cast<char*>(&xml.unknown_children), sizeof(xml.unknown_children));
        is.read(reinterpret_cast<char*>(&xml.unknown_attributes), sizeof(xml.unknown_attributes));

        return xml;
    }

    void to_stream(std::ostream& os) const
    {
        os.write(reinterpret_cast<const char*>(&Enabled), sizeof(Enabled));
        tools::classhelper::stream::container_to_stream(os, SubscriptionPath);
        tools::classhelper::stream::container_to_stream(os, Type);
        tools::classhelper::stream::container_to_stream(os, SensorType);
        tools::classhelper::stream::container_to_stream(os, Name);

        size_t size = Values.size();
        os.write(reinterpret_cast<const char*>(&size), sizeof(size));
        for (const auto& value : Values)
        {
            value.to_stream(os);
        }

        os.write(reinterpret_cast<const char*>(&unknown_children), sizeof(unknown_children));
        os.write(reinterpret_cast<const char*>(&unknown_attributes), sizeof(unknown_attributes));
    }

    // ----- operators -----
    bool operator==(const XML_Configuration_Sensor_Telegram& other) const
    {
        return Enabled == other.Enabled && SubscriptionPath == other.SubscriptionPath &&
               Type == other.Type && SensorType == other.SensorType && Name == other.Name &&
               Values == other.Values;

        // && unknown_children == other.unknown_children &&
        // unknown_attributes == other.unknown_attributes;
    }
    bool operator!=(const XML_Configuration_Sensor_Telegram& other) const
    {
        return !operator==(other);
    }

    // ----- objectprinter -----
    tools::classhelper::ObjectPrinter __printer__(unsigned int float_precision) const
    {
        tools::classhelper::ObjectPrinter printer("EK80 XML0 Configuration_Sensor_Telegram",
                                                  float_precision);

        if (!Values.empty())
        {
            printer.register_section("children (Values)");
            for (const auto& value : Values)
            {
                printer.register_value(
                    "Value", value.Name, fmt::format("Priority {}", value.Priority));
            }
        }

        printer.register_section("attributes");

        printer.register_value("Enabled", Enabled);
        printer.register_string("SubscriptionPath", SubscriptionPath);
        printer.register_string("Type", Type);
        printer.register_string("Name", Name);

        return printer;
    }

    // ----- class helper macros -----
    __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__ __STREAM_DEFAULT_TOFROM_BINARY_FUNCTIONS__(
        XML_Configuration_Sensor_Telegram)
};

}
}
}
}
}