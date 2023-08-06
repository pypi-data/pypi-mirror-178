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
#include "xml_configuration_transceiver_channel.hpp"
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
struct XML_Configuration_Transceiver
{
    std::string TransceiverName;
    std::string TransceiverType;
    std::string MarketSegment;
    std::string EthernetAddress;
    std::string IPAddress;
    std::string TransceiverSoftwareVersion;
    std::string Version;

    double Impedance         = NAN;
    double RxSampleFrequency = NAN;
    int    SerialNumber      = -1;
    int    TransceiverNumber;
    int    Multiplexing;

    std::vector<XML_Configuration_Transceiver_Channel> Channels;

    int32_t unknown_children   = 0;
    int32_t unknown_attributes = 0;

  public:
    // ----- constructors -----
    XML_Configuration_Transceiver() = default;
    XML_Configuration_Transceiver(const pugi::xml_node& node) { initialize(node); }
    ~XML_Configuration_Transceiver() = default;

    void initialize(const pugi::xml_node& root_node)
    {
        if (strcmp(root_node.name(), "Transceiver"))
        {
            throw std::runtime_error(
                std::string("XML_Configuration_Transceiver: wrong root node type '") +
                root_node.name() + "'");
        }
        unknown_attributes = 0;
        unknown_children   = 0; // there should only be TelegramValue nodes

        // there should only be one child for this node
        for (const auto& node : root_node.children())
        {
            if (!strcmp(node.name(), "Channels"))
            {
                for (const auto& sensor_node : node.children())
                {
                    Channels.emplace_back(sensor_node);
                }
                for (const auto& attr : node.attributes())
                {
                    ++unknown_attributes;
                    std::cerr << "WARNING: [Configuration/ConfiguredSensors] Unknown Attribute: "
                              << attr.name() << std::endl;
                }

                continue;
            }

            std::cerr << "WARNING: [Configuration/ConfiguredSensors] Unknown child: " << node.name()
                      << std::endl;

            unknown_children = 1;
        }

        for (auto& attr : root_node.attributes())
        {
            std::string_view name = attr.name();
            if (name == "TransceiverName")
            {
                TransceiverName = attr.value();
                continue;
            }
            else if (name == "TransceiverType")
            {
                TransceiverType = attr.value();
                continue;
            }
            else if (name == "MarketSegment")
            {
                MarketSegment = attr.value();
                continue;
            }
            else if (name == "EthernetAddress")
            {
                EthernetAddress = attr.value();
                continue;
            }
            else if (name == "IPAddress")
            {
                IPAddress = attr.value();
                continue;
            }
            else if (name == "TransceiverSoftwareVersion")
            {
                TransceiverSoftwareVersion = attr.value();
                continue;
            }
            else if (name == "Version")
            {
                Version = attr.value();
                continue;
            }
            else if (name == "Impedance")
            {
                Impedance = tools::helper::string_to_double(attr.value());
                continue;
            }
            else if (name == "RxSampleFrequency")
            {
                RxSampleFrequency = tools::helper::string_to_double(attr.value());
                continue;
            }
            else if (name == "SerialNumber")
            {
                SerialNumber = std::stoi(attr.value());
                continue;
            }
            else if (name == "TransceiverNumber")
            {
                TransceiverNumber = std::stoi(attr.value());
                continue;
            }
            else if (name == "Multiplexing")
            {
                Multiplexing = std::stoi(attr.value());
                continue;
            }

            std::cerr << "WARNING: [Configuration_Transceiver] Unknown attribute: " << name
                      << std::endl;
            unknown_attributes += 1;
        }
    }

    bool parsed_completely() const { return unknown_children == 0 && unknown_attributes == 0; }

    // ----- file I/O -----
    static XML_Configuration_Transceiver from_stream(std::istream& is)
    {
        XML_Configuration_Transceiver xml;

        xml.TransceiverName = tools::classhelper::stream::container_from_stream<std::string>(is);
        xml.TransceiverType = tools::classhelper::stream::container_from_stream<std::string>(is);
        xml.MarketSegment   = tools::classhelper::stream::container_from_stream<std::string>(is);
        xml.EthernetAddress = tools::classhelper::stream::container_from_stream<std::string>(is);
        xml.IPAddress       = tools::classhelper::stream::container_from_stream<std::string>(is);
        xml.TransceiverSoftwareVersion =
            tools::classhelper::stream::container_from_stream<std::string>(is);
        xml.Version = tools::classhelper::stream::container_from_stream<std::string>(is);

        is.read(reinterpret_cast<char*>(&xml.Impedance), sizeof(xml.Impedance) * 2);
        is.read(reinterpret_cast<char*>(&xml.SerialNumber), sizeof(xml.SerialNumber) * 3);

        size_t size;
        is.read(reinterpret_cast<char*>(&size), sizeof(size));
        xml.Channels.resize(size);
        for (auto& value : xml.Channels)
        {
            value = XML_Configuration_Transceiver_Channel::from_stream(is);
        }

        is.read(reinterpret_cast<char*>(&xml.unknown_children), sizeof(xml.unknown_children));
        is.read(reinterpret_cast<char*>(&xml.unknown_attributes), sizeof(xml.unknown_attributes));

        return xml;
    }

    void to_stream(std::ostream& os) const
    {
        tools::classhelper::stream::container_to_stream(os, TransceiverName);
        tools::classhelper::stream::container_to_stream(os, TransceiverType);
        tools::classhelper::stream::container_to_stream(os, MarketSegment);
        tools::classhelper::stream::container_to_stream(os, EthernetAddress);
        tools::classhelper::stream::container_to_stream(os, IPAddress);
        tools::classhelper::stream::container_to_stream(os, TransceiverSoftwareVersion);
        tools::classhelper::stream::container_to_stream(os, Version);

        os.write(reinterpret_cast<const char*>(&Impedance), sizeof(Impedance) * 2);
        os.write(reinterpret_cast<const char*>(&SerialNumber), sizeof(SerialNumber) * 3);

        size_t size = Channels.size();
        os.write(reinterpret_cast<const char*>(&size), sizeof(size));
        for (const auto& value : Channels)
        {
            value.to_stream(os);
        }

        os.write(reinterpret_cast<const char*>(&unknown_children), sizeof(unknown_children));
        os.write(reinterpret_cast<const char*>(&unknown_attributes), sizeof(unknown_attributes));
    }

    // ----- operators -----
    bool operator==(const XML_Configuration_Transceiver& other) const
    {
        using tools::helper::approx;

        return TransceiverName == other.TransceiverName &&
               TransceiverType == other.TransceiverType && MarketSegment == other.MarketSegment &&
               EthernetAddress == other.EthernetAddress && IPAddress == other.IPAddress &&
               TransceiverSoftwareVersion == other.TransceiverSoftwareVersion &&
               Version == other.Version && approx(Impedance, other.Impedance) &&
               approx(RxSampleFrequency, other.RxSampleFrequency) &&
               SerialNumber == other.SerialNumber && TransceiverNumber == other.TransceiverNumber &&
               Multiplexing == other.Multiplexing && Channels == other.Channels;

        // && unknown_children == other.unknown_children &&
        // unknown_attributes == other.unknown_attributes;
    }
    bool operator!=(const XML_Configuration_Transceiver& other) const { return !operator==(other); }

    // ----- objectprinter -----
    tools::classhelper::ObjectPrinter __printer__(unsigned int float_precision) const
    {
        tools::classhelper::ObjectPrinter printer("EK80 XML0 Configuration_Transceiver",
                                                  float_precision);

        if (!Channels.empty())
        {
            printer.register_section("children (Channels)");
            printer.register_value("Channels", Channels.size());
            // for (const auto& telegram : Telegrams)
            // {
            //     std::string values = "";
            //     for (const auto& value : telegram.Values)
            //     {
            //         values += fmt::format("{} ({}),", value.Name, value.Priority);
            //     }
            //     // remove trailing ',' if there is one
            //     if (!values.empty())
            //     {
            //         values.pop_back();
            //     }

            //     printer.register_value("Telegram", telegram.Name, values);
            // }
        }

        printer.register_section("attributes");
        printer.register_string("TransceiverName", TransceiverName);
        printer.register_string("TransceiverType", TransceiverType);
        printer.register_string("MarketSegment", MarketSegment);
        printer.register_string("EthernetAddress", EthernetAddress);
        printer.register_string("IPAddress", IPAddress);
        printer.register_string("TransceiverSoftwareVersion", TransceiverSoftwareVersion);
        printer.register_string("Version", Version);

        printer.register_value("Impedance", Impedance);
        printer.register_value("RxSampleFrequency", RxSampleFrequency);
        printer.register_value("SerialNumber", SerialNumber);
        printer.register_value("TransceiverNumber", TransceiverNumber);
        printer.register_value("Multiplexing", Multiplexing);

        printer.register_value("unknown_children", unknown_children);
        printer.register_value("unknown_attributes", unknown_attributes);

        return printer;
    }

    // ----- class helper macros -----
    __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__ __STREAM_DEFAULT_TOFROM_BINARY_FUNCTIONS__(
        XML_Configuration_Transceiver)
};

}
}
}
}
}