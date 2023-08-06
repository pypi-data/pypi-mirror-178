// SPDX-FileCopyrightText: 2022 Tim Weiß, GEOMAR Helmholtz Centre for Ocean Research Kiel
// SPDX-FileCopyrightText: 2022 Peter Urban, GEOMAR Helmholtz Centre for Ocean Research Kiel
// SPDX-FileCopyrightText: 2022 Peter Urban, Ghent University
//
// SPDX-License-Identifier: MPL-2.0

#pragma once

// std includes
#include <map>
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

#include <themachinethatgoesping/navigation/sensorconfiguration.hpp>

#include "helper.hpp"
#include "xml_configuration_activepingmode.hpp"
#include "xml_configuration_sensor.hpp"
#include "xml_configuration_transceiver.hpp"
#include "xml_configuration_transducer.hpp"
#include "xml_node.hpp"

#include "channelconfiguration.hpp"

namespace themachinethatgoesping {
namespace echosounders {
namespace simrad {
namespace datagrams {
namespace xml_datagrams {

/**
 * @brief XML base datagram
 *
 */
struct XML_Configuration
{
    // Header attributes
    std::string FileFormatVersion;
    std::string Version;
    std::string TimeBias;
    std::string ApplicationName;
    std::string Copyright;

    std::vector<XML_Configuration_Sensor>      ConfiguredSensors;
    std::vector<XML_Configuration_Transducer>  Transducers;
    std::vector<XML_Configuration_Transceiver> Transceivers;
    XML_Configuration_ActivePingMode           ActivePingMode;

    int32_t unknown_children   = 0;
    int32_t unknown_attributes = 0;

    std::map<std::string, ChannelConfiguration>                  ChannelConfigurations;
    std::map<std::string, std::vector<XML_Configuration_Sensor>> SensorConfigurations = {
        { "fallback", { XML_Configuration_Sensor() } }
    };

  public:
    // ----- constructors -----
    XML_Configuration() = default;
    XML_Configuration(const pugi::xml_node& node) { initialize(node); }
    ~XML_Configuration() = default;

    const XML_Configuration_Transceiver& get_transceiver(std::string_view channel_id) const
    {
        for (const auto& transceiver : Transceivers)
            for (const auto& channel : transceiver.Channels)
                if (channel.ChannelID == channel_id)
                    return transceiver;

        throw std::runtime_error(
            "[XML_Configuration_Transceiver]: No transceiver found for channel " +
            std::string(channel_id));
    }

    std::map<std::string, XML_Configuration_Transceiver> get_transceivers() const
    {
        std::map<std::string, XML_Configuration_Transceiver> transceivers;
        for (const auto& transceiver : Transceivers)
            for (const auto& channel : transceiver.Channels)
                transceivers[channel.ChannelID] = transceiver;

        return transceivers;
    }

    const XML_Configuration_Transceiver_Channel& get_transceiver_channel(
        std::string_view channel_id) const
    {
        for (const auto& transceiver : Transceivers)
            for (const auto& channel : transceiver.Channels)
                if (channel.ChannelID == channel_id)
                    return channel;

        throw std::runtime_error(
            "[XML_Configuration_Transceiver]: No transceiver channel found for channel " +
            std::string(channel_id));
    }

    std::map<std::string, XML_Configuration_Transceiver_Channel> get_transceiver_channels() const
    {
        std::map<std::string, XML_Configuration_Transceiver_Channel> channels;
        for (const auto& transceiver : Transceivers)
            for (const auto& channel : transceiver.Channels)
                channels[channel.ChannelID] = channel;

        return channels;
    }

    navigation::SensorConfiguration get_sensor_configuration() const
    {
        navigation::SensorConfiguration sensor_configuration;

        sensor_configuration.set_position_source(
            get_prioritized_sensor({ "Latitude", "Longitude" }).get_sensor_offsets());
        sensor_configuration.set_depth_source(
            get_prioritized_sensor({ "Latitude", "Longitude" }).get_sensor_offsets());
        sensor_configuration.set_attitude_source(
            get_prioritized_sensor({ "Roll", "Pitch", "Heave" }).get_sensor_offsets());
        sensor_configuration.set_heading_source(
            get_prioritized_sensor({ "Heading" }).get_sensor_offsets());

        for (const auto& [channel_id, channel] : ChannelConfigurations)
        {
            sensor_configuration.add_target(channel_id, channel.get_sensor_offsets());
        }

        return sensor_configuration;
    }

    XML_Configuration_Sensor get_prioritized_sensor(
        const std::vector<std::string_view>& prio_values) const
    {
        return get_sensors_sorted_by_priority(prio_values).front();
    }

    std::vector<XML_Configuration_Sensor> get_sensors_sorted_by_priority(
        const std::vector<std::string_view>& prio_values) const
    {
        std::vector<std::pair<unsigned int, const XML_Configuration_Sensor*>> sensor_priorities;

        // loop through SensorConfigurations
        for (const auto& [key, sensors] : SensorConfigurations)
        {
            // loop through sensors
            for (const auto& sensor : sensors)
            {
                int prio = 99;

                // loop through Telegrams
                for (const auto& telegram : sensor.Telegrams)
                {
                    // loop through Values
                    for (const auto& value : telegram.Values)
                    {
                        // summ prio if value.Name in prio_values
                        if (std::find(prio_values.begin(), prio_values.end(), value.Name) !=
                            prio_values.end())
                            prio -= value.Priority;
                    }
                }

                if (prio < 99)
                    sensor_priorities.push_back(std::make_pair(prio, &sensor));
            }
        }

        // return vector of sensors sorted by priority (lowest prio values)
        // std::vector<XML_Configuration_Sensor> sensors_sorted_by_priority;
        std::vector<XML_Configuration_Sensor> sensors_sorted_by_priority;

        std::sort(sensor_priorities.begin(),
                  sensor_priorities.end(),
                  [](const auto& a, const auto& b) { return a.first > b.first; });

        for (const auto& sensor : sensor_priorities)
            sensors_sorted_by_priority.push_back(*sensor.second);

        if (sensors_sorted_by_priority.empty())
        {
            sensors_sorted_by_priority = { XML_Configuration_Sensor() };

            sensors_sorted_by_priority[0].Type = "fallback";
            sensors_sorted_by_priority[0].Name = "fallback";
        }

        return sensors_sorted_by_priority;
    }

    void initialize_sensorconfigurations()
    {
        for (const auto& sensor : ConfiguredSensors)
        {
            SensorConfigurations[sensor.Type].push_back(sensor);
        }
    }

    void initialize_channelconfigurations()
    {
        std::map<std::string, XML_Configuration_Transducer> transducers;
        for (const auto& tr : Transducers)
            transducers[tr.TransducerName] = tr;

        for (const auto& trc : Transceivers)
        {
            for (const auto& ch : trc.Channels)
            {
                ChannelConfigurations[ch.ChannelID] = ChannelConfiguration(
                    ch.ChannelID, ch, trc, transducers[ch.Transducer.TransducerName]);
            }
        }
    }

    void initialize(const pugi::xml_node& root_node)
    {
        if (strcmp(root_node.name(), "Configuration"))
        {
            throw std::runtime_error(std::string("XML_Configuration: wrong root node type '") +
                                     root_node.name() + "'");
        }
        unknown_attributes = 0;
        unknown_children   = 0; // there should only be one child for this node

        // there should only be one child for this node
        for (const auto& node : root_node.children())
        {
            if (!strcmp(node.name(), "ConfiguredSensors"))
            {
                for (const auto& sensor_node : node.children())
                {
                    ConfiguredSensors.emplace_back(sensor_node);
                }
                for (const auto& attr : node.attributes())
                {
                    if (!strcmp(attr.name(), "MergeOperation"))
                    {
                        continue;
                    }

                    ++unknown_attributes;
                    std::cerr << "WARNING: [Configuration/ConfiguredSensors] Unknown Attribute: "
                              << attr.name() << std::endl;
                }

                continue;
            }
            else if (!strcmp(node.name(), "Transducers"))
            {
                for (const auto& sensor_node : node.children())
                {
                    Transducers.emplace_back(sensor_node);
                }
                for (const auto& attr : node.attributes())
                {
                    if (!strcmp(attr.name(), "MergeOperation"))
                    {
                        continue;
                    }

                    ++unknown_attributes;
                    std::cerr << "WARNING: [Configuration/Transducers] Unknown Attribute: "
                              << attr.name() << std::endl;
                }

                continue;
            }
            else if (!strcmp(node.name(), "Transceivers"))
            {
                for (const auto& sensor_node : node.children())
                {
                    Transceivers.emplace_back(sensor_node);
                }
                for (const auto& attr : node.attributes())
                {
                    if (!strcmp(attr.name(), "MergeOperation"))
                    {
                        continue;
                    }

                    ++unknown_attributes;
                    std::cerr << "WARNING: [Configuration/Transceivers] Unknown Attribute: "
                              << attr.name() << std::endl;
                }

                continue;
            }
            else if (!strcmp(node.name(), "ActivePingMode"))
            {
                if (!ActivePingMode.Mode.empty())
                {
                    ++unknown_children;
                    std::cerr << "WARNING: [Configuration/ActivePingMode] More than one "
                                 "ActivePingMode element!: "
                              << node.name() << std::endl;

                    continue;
                }

                ActivePingMode = XML_Configuration_ActivePingMode(node);

                continue;
            }
            else if (!strcmp(node.name(), "Header"))
            {
                for (const auto& header_node : node.children())
                {
                    ++unknown_children;
                    std::cerr << "WARNING: [Configuration/THeader] Unknown children: "
                              << header_node.name() << std::endl;
                }
                for (const auto& attr : node.attributes())
                {
                    if (!strcmp(attr.name(), "FileFormatVersion"))
                    {
                        FileFormatVersion = attr.value();
                        continue;
                    }
                    else if (!strcmp(attr.name(), "Version"))
                    {
                        Version = attr.value();
                        continue;
                    }
                    else if (!strcmp(attr.name(), "TimeBias"))
                    {
                        TimeBias = attr.value();
                        continue;
                    }
                    else if (!strcmp(attr.name(), "ApplicationName"))
                    {
                        ApplicationName = attr.value();
                        continue;
                    }
                    else if (!strcmp(attr.name(), "Copyright"))
                    {
                        Copyright = attr.value();
                        continue;
                    }

                    ++unknown_attributes;
                    std::cerr << "WARNING: [Configuration/Header] Unknown Attribute: "
                              << attr.name() << std::endl;
                }

                continue;
            }

            std::cerr << "WARNING: [Configuration] Unknown child: " << node.name() << std::endl;

            ++unknown_children;
        }

        initialize_channelconfigurations();
        initialize_sensorconfigurations();
    }

    bool parsed_completely() const { return unknown_children == 0 && unknown_attributes == 0; }

    // ----- file I/O -----
    static XML_Configuration from_stream(std::istream& is)
    {
        XML_Configuration xml;

        xml.FileFormatVersion = tools::classhelper::stream::container_from_stream<std::string>(is);
        xml.Version           = tools::classhelper::stream::container_from_stream<std::string>(is);
        xml.TimeBias          = tools::classhelper::stream::container_from_stream<std::string>(is);
        xml.ApplicationName   = tools::classhelper::stream::container_from_stream<std::string>(is);
        xml.Copyright         = tools::classhelper::stream::container_from_stream<std::string>(is);

        size_t size;

        is.read(reinterpret_cast<char*>(&size), sizeof(size));
        xml.ConfiguredSensors.resize(size);
        for (auto& node : xml.ConfiguredSensors)
        {
            node = XML_Configuration_Sensor::from_stream(is);
        }

        is.read(reinterpret_cast<char*>(&size), sizeof(size));
        xml.Transducers.resize(size);
        for (auto& node : xml.Transducers)
        {
            node = XML_Configuration_Transducer::from_stream(is);
        }

        is.read(reinterpret_cast<char*>(&size), sizeof(size));
        xml.Transceivers.resize(size);
        for (auto& node : xml.Transceivers)
        {
            node = XML_Configuration_Transceiver::from_stream(is);
        }

        xml.ActivePingMode = XML_Configuration_ActivePingMode::from_stream(is);

        return xml;
    }

    void to_stream(std::ostream& os) const
    {
        tools::classhelper::stream::container_to_stream(os, FileFormatVersion);
        tools::classhelper::stream::container_to_stream(os, Version);
        tools::classhelper::stream::container_to_stream(os, TimeBias);
        tools::classhelper::stream::container_to_stream(os, ApplicationName);
        tools::classhelper::stream::container_to_stream(os, Copyright);

        size_t size;

        size = ConfiguredSensors.size();
        os.write(reinterpret_cast<const char*>(&size), sizeof(size));
        for (const auto& node : ConfiguredSensors)
        {
            node.to_stream(os);
        }

        size = Transducers.size();
        os.write(reinterpret_cast<const char*>(&size), sizeof(size));
        for (const auto& node : Transducers)
        {
            node.to_stream(os);
        }

        size = Transceivers.size();
        os.write(reinterpret_cast<const char*>(&size), sizeof(size));
        for (const auto& node : Transceivers)
        {
            node.to_stream(os);
        }

        ActivePingMode.to_stream(os);
    }

    // ----- operators -----
    bool operator==(const XML_Configuration& other) const
    {
        return ConfiguredSensors == other.ConfiguredSensors && Transducers == other.Transducers &&
               Transceivers == other.Transceivers && ActivePingMode == other.ActivePingMode &&
               FileFormatVersion == other.FileFormatVersion && Version == other.Version &&
               TimeBias == other.TimeBias && ApplicationName == other.ApplicationName;
    }
    bool operator!=(const XML_Configuration& other) const { return !operator==(other); }

    // ----- objectprinter -----
    tools::classhelper::ObjectPrinter __printer__(unsigned int float_precision) const
    {
        tools::classhelper::ObjectPrinter printer("EK80 XML0 Configuration Datagram",
                                                  float_precision);
        printer.register_section("children");
        printer.register_value("ConfiguredSensors", ConfiguredSensors.size());
        printer.register_value("Transducers", Transducers.size());
        printer.register_value("Transceivers", Transceivers.size());
        if (!ActivePingMode.Mode.empty())
        {
            printer.register_value("ActivePingMode", ActivePingMode.Mode);
        }

        printer.register_section("channels");
        unsigned int i = 0;
        for (const auto& ch : ChannelConfigurations)
        {
            printer.register_string(fmt::format("Channel ({})", i++), ch.first);
        }

        printer.register_section("attributes (Header)");
        printer.register_string("FileFormatVersion", FileFormatVersion);
        printer.register_string("Version", Version);
        printer.register_string("TimeBias", TimeBias);
        printer.register_string("ApplicationName", ApplicationName);
        printer.register_string("Copyright", Copyright);

        return printer;
    }

    // ----- class helper macros -----
    __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__ __STREAM_DEFAULT_TOFROM_BINARY_FUNCTIONS__(
        XML_Configuration)
};

}
}
}
}
}