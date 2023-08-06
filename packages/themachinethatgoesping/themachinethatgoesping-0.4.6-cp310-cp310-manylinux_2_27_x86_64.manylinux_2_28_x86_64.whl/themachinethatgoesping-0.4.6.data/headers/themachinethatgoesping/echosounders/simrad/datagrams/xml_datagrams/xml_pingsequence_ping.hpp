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
struct XML_PingSequence_Ping
{
    std::string ChannelID;

    int32_t unknown_children   = 0;
    int32_t unknown_attributes = 0;

  public:
    // ----- constructors -----
    XML_PingSequence_Ping() = default;
    XML_PingSequence_Ping(const pugi::xml_node& node) { initialize(node); }
    ~XML_PingSequence_Ping() = default;

    void initialize(const pugi::xml_node& root_node)
    {
        if (strcmp(root_node.name(), "Ping"))
        {
            throw std::runtime_error(std::string("XML_PingSequence_Ping: wrong root node type '") +
                                     root_node.name() + "'");
        }
        unknown_attributes = 0;
        unknown_children   = 0; // there should only be one child for this node

        // there should only be one child for this node
        for (const auto& node : root_node.children())
        {
            std::cerr << "WARNING: [PingSequence_Ping] Unknown child: " << node.name() << std::endl;

            unknown_children = 1;

            continue;
        }

        for (auto& attr : root_node.attributes())
        {
            std::string_view name = attr.name();
            if (name == "ChannelID")
            {
                ChannelID = attr.value();
                continue;
            }

            std::cerr << "WARNING: [PingSequence_Ping] Unknown attribute: " << name << std::endl;
            unknown_attributes += 1;
        }
    }

    bool parsed_completely() const { return unknown_children == 0 && unknown_attributes == 0; }

    // ----- file I/O -----
    static XML_PingSequence_Ping from_stream(std::istream& is)
    {
        XML_PingSequence_Ping xml;
        xml.ChannelID = tools::classhelper::stream::container_from_stream<std::string>(is);
        is.read(reinterpret_cast<char*>(&xml.unknown_children), sizeof(xml.unknown_children));
        is.read(reinterpret_cast<char*>(&xml.unknown_attributes), sizeof(xml.unknown_attributes));

        return xml;
    }

    void to_stream(std::ostream& os) const
    {
        tools::classhelper::stream::container_to_stream(os, ChannelID);
        os.write(reinterpret_cast<const char*>(&unknown_children), sizeof(unknown_children));
        os.write(reinterpret_cast<const char*>(&unknown_attributes), sizeof(unknown_attributes));
    }

    // ----- operators -----
    bool operator==(const XML_PingSequence_Ping& other) const
    {
        return ChannelID == other.ChannelID;
        // && unknown_children == other.unknown_children &&
        // unknown_attributes == other.unknown_attributes;
    }
    bool operator!=(const XML_PingSequence_Ping& other) const { return !operator==(other); }

    // ----- objectprinter -----
    tools::classhelper::ObjectPrinter __printer__(unsigned int float_precision) const
    {
        tools::classhelper::ObjectPrinter printer("EK80 XML0 PingSequence_Ping", float_precision);
        printer.register_string("ChannelID", ChannelID);
        printer.register_value("unknown_children", unknown_children);
        printer.register_value("unknown_attributes", unknown_attributes);

        return printer;
    }

    // ----- class helper macros -----
    __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__ __STREAM_DEFAULT_TOFROM_BINARY_FUNCTIONS__(
        XML_PingSequence_Ping)
};

}
}
}
}
}