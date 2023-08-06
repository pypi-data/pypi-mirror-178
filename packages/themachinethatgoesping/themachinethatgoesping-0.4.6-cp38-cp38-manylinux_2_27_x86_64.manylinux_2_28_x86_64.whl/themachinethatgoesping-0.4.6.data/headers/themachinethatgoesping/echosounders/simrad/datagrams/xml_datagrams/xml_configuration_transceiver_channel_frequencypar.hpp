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
struct XML_Configuration_Transceiver_Channel_FrequencyPar
{

    double Frequency;
    double Gain;
    double Impedance;
    double Phase;
    double BeamWidthAlongship;
    double BeamWidthAthwartship;
    double AngleOffsetAlongship;
    double AngleOffsetAthwartship;

    int32_t unknown_children   = 0;
    int32_t unknown_attributes = 0;

  public:
    // ----- constructors -----
    XML_Configuration_Transceiver_Channel_FrequencyPar() = default;
    XML_Configuration_Transceiver_Channel_FrequencyPar(const pugi::xml_node& node)
    {
        initialize(node);
    }
    ~XML_Configuration_Transceiver_Channel_FrequencyPar() = default;

    void initialize(const pugi::xml_node& root_node)
    {
        if (strcmp(root_node.name(), "FrequencyPar"))
        {
            throw std::runtime_error(
                std::string(
                    "XML_Configuration_Transceiver_Channel_FrequencyPar: wrong root node type '") +
                root_node.name() + "'");
        }
        unknown_attributes = 0;
        unknown_children   = 0; // there should only be one Transducer Node

        // there should only be one child for this node
        for (const auto& node : root_node.children())
        {
            std::cerr << "WARNING: [Configuration_Transceiver_Channel_FrequencyPar] Unknown child: "
                      << node.name() << std::endl;

            unknown_children = 1;
        }

        for (auto& attr : root_node.attributes())
        {
            std::string_view name = attr.name();
            if (name == "Frequency")
            {
                Frequency = tools::helper::string_to_double(attr.value());
                continue;
            }
            else if (name == "Gain")
            {
                Gain = tools::helper::string_to_double(attr.value());
                continue;
            }
            else if (name == "Impedance")
            {
                Impedance = tools::helper::string_to_double(attr.value());
                continue;
            }
            else if (name == "Phase")
            {
                Phase = tools::helper::string_to_double(attr.value());
                continue;
            }
            else if (name == "BeamWidthAlongship")
            {
                BeamWidthAlongship = tools::helper::string_to_double(attr.value());
                continue;
            }
            else if (name == "BeamWidthAthwartship")
            {
                BeamWidthAthwartship = tools::helper::string_to_double(attr.value());
                continue;
            }
            else if (name == "AngleOffsetAlongship")
            {
                AngleOffsetAlongship = tools::helper::string_to_double(attr.value());
                continue;
            }
            else if (name == "AngleOffsetAthwartship")
            {
                AngleOffsetAthwartship = tools::helper::string_to_double(attr.value());
                continue;
            }

            std::cerr
                << "WARNING: [Configuration_Transceiver_Channel_FrequencyPar] Unknown attribute: "
                << name << std::endl;
            unknown_attributes += 1;
        }
    }

    bool parsed_completely() const { return unknown_children == 0 && unknown_attributes == 0; }

    // ----- file I/O -----
    static XML_Configuration_Transceiver_Channel_FrequencyPar from_stream(std::istream& is)
    {
        XML_Configuration_Transceiver_Channel_FrequencyPar xml;

        is.read(reinterpret_cast<char*>(&xml.Frequency), sizeof(xml.Frequency) * 8);

        is.read(reinterpret_cast<char*>(&xml.unknown_children), sizeof(xml.unknown_children));
        is.read(reinterpret_cast<char*>(&xml.unknown_attributes), sizeof(xml.unknown_attributes));

        return xml;
    }

    void to_stream(std::ostream& os) const
    {
        os.write(reinterpret_cast<const char*>(&Frequency), sizeof(Frequency) * 8);

        os.write(reinterpret_cast<const char*>(&unknown_children), sizeof(unknown_children));
        os.write(reinterpret_cast<const char*>(&unknown_attributes), sizeof(unknown_attributes));
    }

    // ----- operators -----
    bool operator==(const XML_Configuration_Transceiver_Channel_FrequencyPar& other) const
    {
        using tools::helper::approx;
        return approx(Frequency, other.Frequency) && approx(Gain, other.Gain) &&
               approx(Impedance, other.Impedance) && approx(Phase, other.Phase) &&
               approx(BeamWidthAlongship, other.BeamWidthAlongship) &&
               approx(BeamWidthAthwartship, other.BeamWidthAthwartship) &&
               approx(AngleOffsetAlongship, other.AngleOffsetAlongship) &&
               approx(AngleOffsetAthwartship, other.AngleOffsetAthwartship);

        // && unknown_children == other.unknown_children &&
        // unknown_attributes == other.unknown_attributes;
    }
    bool operator!=(const XML_Configuration_Transceiver_Channel_FrequencyPar& other) const
    {
        return !operator==(other);
    }

    // ----- objectprinter -----
    tools::classhelper::ObjectPrinter __printer__(unsigned int float_precision) const
    {
        tools::classhelper::ObjectPrinter printer(
            "EK80 XML0 Configuration_Transceiver_Channel_FrequencyPar", float_precision);

        printer.register_section("attributes");
        printer.register_value("Frequency", Frequency);
        printer.register_value("Gain", Gain);
        printer.register_value("Impedance", Impedance);
        printer.register_value("Phase", Phase);
        printer.register_value("BeamWidthAlongship", BeamWidthAlongship);
        printer.register_value("BeamWidthAthwartship", BeamWidthAthwartship);
        printer.register_value("AngleOffsetAlongship", AngleOffsetAlongship);
        printer.register_value("AngleOffsetAthwartship", AngleOffsetAthwartship);

        return printer;
    }

    // ----- class helper macros -----
    __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__ __STREAM_DEFAULT_TOFROM_BINARY_FUNCTIONS__(
        XML_Configuration_Transceiver_Channel_FrequencyPar)
};

}
}
}
}
}