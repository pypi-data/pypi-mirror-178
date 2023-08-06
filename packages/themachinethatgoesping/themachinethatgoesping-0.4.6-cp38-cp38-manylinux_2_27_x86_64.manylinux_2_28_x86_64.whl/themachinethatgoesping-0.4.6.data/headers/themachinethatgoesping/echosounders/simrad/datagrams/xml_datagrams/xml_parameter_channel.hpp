// SPDX-FileCopyrightText: 2022 Tim Weiß, GEOMAR Helmholtz Centre for Ocean
// Research Kiel SPDX-FileCopyrightText: 2022 Peter Urban, GEOMAR Helmholtz
// Centre for Ocean Research Kiel SPDX-FileCopyrightText: 2022 Peter Urban,
// Ghent University
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
struct XML_Parameter_Channel
{
    std::string ChannelID;
    int64_t     ChannelMode     = -1;
    double      PulseForm       = NAN; ///< 0 means cw, ?1 means chirp?
    double      FrequencyStart  = NAN; ///< used used for chirp pulse (PulseForm > 0)
    double      FrequencyEnd    = NAN; ///< used used for chirp pulse (PulseForm > 0)
    double      BandWidth       = NAN; ///< TODO: when is this one used
    double      Frequency       = NAN; ///< used for cv ( PulseForm == 0)
    double      PulseDuration   = NAN; ///< used used for chirp pulse (PulseForm > 0)
    double      PulseLength     = NAN; ///< used for cv ( PulseForm == 0)
    double      SampleInterval  = NAN;
    double      TransducerDepth = NAN; ///< when is this one used? only old format?
    double      TransmitPower   = NAN;
    double      Slope           = NAN;
    double      SoundVelocity   = NAN;
    std::string PingId; ///< this is used in the InitialParameter datagram

    int32_t unknown_children   = 0;
    int32_t unknown_attributes = 0;

  public:
    // ----- constructors -----
    XML_Parameter_Channel() = default;
    XML_Parameter_Channel(const pugi::xml_node& node) { initialize(node); }
    ~XML_Parameter_Channel() = default;

    void initialize_channel_structure(const pugi::xml_node& node)
    {
        for (const auto& attr : node.attributes())
        {
            std::string_view name = attr.name();
            if (name == "ChannelID")
            {
                ChannelID = attr.value();
                continue;
            }
            if (name == "ChannelMode")
            {
                ChannelMode = std::stoi(attr.value());
                continue;
            }
            if (name == "PulseForm")
            {
                PulseForm = tools::helper::string_to_double(attr.value());
                continue;
            }
            if (name == "FrequencyStart")
            {
                FrequencyStart = tools::helper::string_to_double(attr.value());
                continue;
            }
            if (name == "FrequencyEnd")
            {
                FrequencyEnd = tools::helper::string_to_double(attr.value());
                continue;
            }
            if (name == "BandWidth")
            {
                BandWidth = tools::helper::string_to_double(attr.value());
                continue;
            }
            if (name == "Frequency")
            {
                Frequency = tools::helper::string_to_double(attr.value());
                continue;
            }
            if (name == "PulseDuration")
            {
                PulseDuration = tools::helper::string_to_double(attr.value());
                continue;
            }
            if (name == "PulseLength")
            {
                PulseLength = tools::helper::string_to_double(attr.value());
                continue;
            }
            if (name == "SampleInterval")
            {
                SampleInterval = tools::helper::string_to_double(attr.value());
                continue;
            }
            if (name == "TransducerDepth")
            {
                TransducerDepth = tools::helper::string_to_double(attr.value());
                continue;
            }
            if (name == "TransmitPower")
            {
                TransmitPower = tools::helper::string_to_double(attr.value());
                continue;
            }
            if (name == "Slope")
            {
                Slope = tools::helper::string_to_double(attr.value());
                continue;
            }
            if (name == "SoundVelocity")
            {
                SoundVelocity = tools::helper::string_to_double(attr.value());
                continue;
            }
            if (name == "PingId")
            {
                PingId = attr.value();
                continue;
            }
            std::cerr << "WARNING: [ParameterChannel] Unknown attribute: " << name << std::endl;
            unknown_attributes += 1;
        }
    }

    void initialize(const pugi::xml_node& root_node)
    {
        if (strcmp(root_node.name(), "Parameter"))
        {
            throw std::runtime_error(std::string("XML_Parameter_Channel: wrong root node type '") +
                                     root_node.name() + "'");
        }
        unknown_attributes = 0;
        unknown_children   = 0; // there should only be one child for this node
        bool parsed        = false;

        // there should only be one child for this node
        for (const auto& node : root_node.children())
        {
            if (parsed || strcmp(node.name(), "Channel"))
            {
                std::cerr << "WARNING: [ParameterChannel] Unknown child: " << node.name()
                          << std::endl;

                unknown_children = 1;

                continue;
            }

            parsed = true;

            initialize_channel_structure(node);
        }
    }

    bool parsed_completely() const { return unknown_children == 0 && unknown_attributes == 0; }

    // ----- file I/O -----
    static XML_Parameter_Channel from_stream(std::istream& is)
    {
        XML_Parameter_Channel xml;
        xml.ChannelID = tools::classhelper::stream::container_from_stream<std::string>(is);
        is.read(reinterpret_cast<char*>(&xml.ChannelMode), sizeof(xml.ChannelMode));
        is.read(reinterpret_cast<char*>(&xml.PulseForm), sizeof(xml.PulseForm) * 12);
        xml.PingId = tools::classhelper::stream::container_from_stream<std::string>(is);
        is.read(reinterpret_cast<char*>(&xml.unknown_children), sizeof(xml.unknown_children));
        is.read(reinterpret_cast<char*>(&xml.unknown_attributes), sizeof(xml.unknown_attributes));

        return xml;
    }

    void to_stream(std::ostream& os) const
    {
        tools::classhelper::stream::container_to_stream(os, ChannelID);
        os.write(reinterpret_cast<const char*>(&ChannelMode), sizeof(ChannelMode));
        os.write(reinterpret_cast<const char*>(&PulseForm), sizeof(PulseForm) * 12);
        tools::classhelper::stream::container_to_stream(os, PingId);
        os.write(reinterpret_cast<const char*>(&unknown_children), sizeof(unknown_children));
        os.write(reinterpret_cast<const char*>(&unknown_attributes), sizeof(unknown_attributes));
    }

    // ----- operators -----
    bool operator==(const XML_Parameter_Channel& other) const
    {
        using tools::helper::approx;
        return ChannelID == other.ChannelID && ChannelMode == other.ChannelMode &&
               approx(PulseForm, other.PulseForm) && approx(FrequencyStart, other.FrequencyStart) &&
               approx(FrequencyEnd, other.FrequencyEnd) && approx(BandWidth, other.BandWidth) &&
               approx(Frequency, other.Frequency) && approx(PulseDuration, other.PulseDuration) &&
               approx(PulseLength, other.PulseLength) &&
               approx(SampleInterval, other.SampleInterval) &&
               approx(TransducerDepth, other.TransducerDepth) &&
               approx(TransmitPower, other.TransmitPower) && approx(Slope, other.Slope) &&
               approx(SoundVelocity, other.SoundVelocity) && PingId == other.PingId;
        // && unknown_children == other.unknown_children &&
        // unknown_attributes == other.unknown_attributes;
    }
    bool operator!=(const XML_Parameter_Channel& other) const { return !operator==(other); }

    bool operator<(const XML_Parameter_Channel& other) const
    {
        if (ChannelID < other.ChannelID)
            return true;
        if (ChannelID > other.ChannelID)
            return false;
        if (ChannelMode < other.ChannelMode)
            return true;
        if (ChannelMode > other.ChannelMode)
            return false;
        if (PulseForm < other.PulseForm)
            return true;
        if (PulseForm > other.PulseForm)
            return false;
        if (FrequencyStart < other.FrequencyStart)
            return true;
        if (FrequencyStart > other.FrequencyStart)
            return false;
        if (FrequencyEnd < other.FrequencyEnd)
            return true;
        if (FrequencyEnd > other.FrequencyEnd)
            return false;
        if (BandWidth < other.BandWidth)
            return true;
        if (BandWidth > other.BandWidth)
            return false;
        if (Frequency < other.Frequency)
            return true;
        if (Frequency > other.Frequency)
            return false;
        if (PulseDuration < other.PulseDuration)
            return true;
        if (PulseDuration > other.PulseDuration)
            return false;
        if (PulseLength < other.PulseLength)
            return true;
        if (PulseLength > other.PulseLength)
            return false;
        if (SampleInterval < other.SampleInterval)
            return true;
        if (SampleInterval > other.SampleInterval)
            return false;
        if (TransducerDepth < other.TransducerDepth)
            return true;
        if (TransducerDepth > other.TransducerDepth)
            return false;
        if (TransmitPower < other.TransmitPower)
            return true;
        if (TransmitPower > other.TransmitPower)
            return false;
        if (Slope < other.Slope)
            return true;
        if (Slope > other.Slope)
            return false;
        if (SoundVelocity < other.SoundVelocity)
            return true;
        if (SoundVelocity > other.SoundVelocity)
            return false;
        if (PingId < other.PingId)
            return true;
        if (PingId > other.PingId)
            return false;

        return false;
    }

    // ----- objectprinter -----
    tools::classhelper::ObjectPrinter __printer__(unsigned int float_precision) const
    {
        tools::classhelper::ObjectPrinter printer("EK80 XML0 Parameter Channel", float_precision);
        printer.register_string("ChannelID", ChannelID);
        printer.register_value("ChannelMode", ChannelMode);
        printer.register_value("PulseForm", PulseForm);
        printer.register_value("FrequencyStart", FrequencyStart);
        printer.register_value("FrequencyEnd", FrequencyEnd);
        printer.register_value("BandWidth", BandWidth);
        printer.register_value("Frequency", Frequency);
        printer.register_value("PulseDuration", PulseDuration);
        printer.register_value("PulseLength", PulseLength);
        printer.register_value("SampleInterval", SampleInterval);
        printer.register_value("TransducerDepth", TransducerDepth);
        printer.register_value("TransmitPower", TransmitPower);
        printer.register_value("Slope", Slope);
        printer.register_value("SoundVelocity", SoundVelocity);
        printer.register_value("PingId", PingId);
        printer.register_value("unknown_children", unknown_children);
        printer.register_value("unknown_attributes", unknown_attributes);

        return printer;
    }

    xxh::hash_t<64> slow_hash() const
    {
        // hash streaming
        xxh::hash3_state_t<64> hash_stream; 
        
        hash_stream.update(ChannelID);
        hash_stream.update(&ChannelMode, sizeof(ChannelMode) + 12 * sizeof(double));
        hash_stream.update(PingId);

        return hash_stream.digest();
    }

    // ----- class helper macros -----
    __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__ __STREAM_DEFAULT_TOFROM_BINARY_FUNCTIONS_NO_HASH__(
        XML_Parameter_Channel)
};

}
}
}
}
}

namespace std {
  template <> struct hash<themachinethatgoesping::echosounders::simrad::datagrams::xml_datagrams::XML_Parameter_Channel>
  {
    size_t operator()(const themachinethatgoesping::echosounders::simrad::datagrams::xml_datagrams::XML_Parameter_Channel & arg) const
    {
        return arg.slow_hash();
    }
  };
}