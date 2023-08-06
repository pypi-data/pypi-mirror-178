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

#include <themachinethatgoesping/navigation/datastructures/positionaloffsets.hpp>

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
struct XML_Configuration_Transducer
{
    double      TransducerAlphaX        = 0.;
    double      TransducerAlphaY        = 0.;
    double      TransducerAlphaZ        = 0.;
    double      TransducerOffsetX       = 0.;
    double      TransducerOffsetY       = 0.;
    double      TransducerOffsetZ       = 0.;
    double      HeadingQuickCalibration = 0.; ///< Seems to be used seldomly?
    int         TransducerSerialNumber  = -1;
    std::string TransducerMounting;
    std::string TransducerOrientation;
    std::string TransducerName;
    std::string TransducerCustomName;

    int32_t unknown_children   = 0;
    int32_t unknown_attributes = 0;

  public:
    // ----- constructors -----
    XML_Configuration_Transducer() = default;
    XML_Configuration_Transducer(const pugi::xml_node& node) { initialize(node); }
    ~XML_Configuration_Transducer() = default;

    // ----- methods -----
    /**
     * @brief Return the offsets as navigation::datastructures::PositionalOffsets structure
     *
     * @return navigation::datastructures::PositionalOffsets
     */
    navigation::datastructures::PositionalOffsets get_sensor_offsets() const
    {
        // TODO: check angle directions
        // TODO: include transducer mounting and transducer orientation?
        // TODO: do we need HeadingQuickCalibration? And if so how to use it?
        return navigation::datastructures::PositionalOffsets(TransducerName,
                                                             TransducerOffsetX,
                                                             TransducerOffsetY,
                                                             TransducerOffsetZ,
                                                             TransducerAlphaZ,
                                                             TransducerAlphaY,
                                                             TransducerAlphaX);
    }

    // ----- xml parsing -----

    void initialize(const pugi::xml_node& root_node)
    {
        if (strcmp(root_node.name(), "Transducer"))
        {
            throw std::runtime_error(
                std::string("XML_Configuration_Transducer: wrong root node type '") +
                root_node.name() + "'");
        }
        unknown_attributes = 0;
        unknown_children   = 0; // there should only be TelegramValue nodes

        // there should only be one child for this node
        for (const auto& node : root_node.children())
        {
            std::cerr << "WARNING: [Configuration_Transducer] Unknown child: " << node.name()
                      << std::endl;

            unknown_children = 1;
        }

        for (auto& attr : root_node.attributes())
        {
            std::string_view name = attr.name();
            if (name == "TransducerAlphaX")
            {
                TransducerAlphaX = tools::helper::string_to_double(attr.value());
                continue;
            }
            else if (name == "TransducerAlphaY")
            {
                TransducerAlphaY = tools::helper::string_to_double(attr.value());
                continue;
            }
            if (name == "TransducerAlphaZ")
            {
                TransducerAlphaZ = tools::helper::string_to_double(attr.value());
                continue;
            }
            if (name == "TransducerOffsetX")
            {
                TransducerOffsetX = tools::helper::string_to_double(attr.value());
                continue;
            }
            if (name == "TransducerOffsetY")
            {
                TransducerOffsetY = tools::helper::string_to_double(attr.value());
                continue;
            }
            if (name == "TransducerOffsetZ")
            {
                TransducerOffsetZ = tools::helper::string_to_double(attr.value());
                continue;
            }
            if (name == "HeadingQuickCalibration")
            {
                HeadingQuickCalibration = tools::helper::string_to_double(attr.value());
                continue;
            }
            if (name == "TransducerSerialNumber")
            {
                TransducerSerialNumber = std::stoi(attr.value());
                continue;
            }
            if (name == "TransducerMounting")
            {
                TransducerMounting = attr.value();
                continue;
            }
            if (name == "TransducerOrientation")
            {
                TransducerOrientation = attr.value();
                continue;
            }
            if (name == "TransducerName")
            {
                TransducerName = attr.value();
                continue;
            }
            if (name == "TransducerCustomName")
            {
                TransducerCustomName = attr.value();
                continue;
            }

            std::cerr << "WARNING: [Configuration_Transducer] Unknown attribute: " << name
                      << std::endl;
            unknown_attributes += 1;
        }
    }

    bool parsed_completely() const { return unknown_children == 0 && unknown_attributes == 0; }

    // ----- file I/O -----
    static XML_Configuration_Transducer from_stream(std::istream& is)
    {
        XML_Configuration_Transducer xml;

        is.read(reinterpret_cast<char*>(&xml.TransducerAlphaX), sizeof(xml.TransducerAlphaX) * 6);
        is.read(reinterpret_cast<char*>(&xml.TransducerSerialNumber),
                sizeof(xml.TransducerSerialNumber));
        xml.TransducerMounting = tools::classhelper::stream::container_from_stream<std::string>(is);
        xml.TransducerOrientation =
            tools::classhelper::stream::container_from_stream<std::string>(is);
        xml.TransducerName = tools::classhelper::stream::container_from_stream<std::string>(is);
        xml.TransducerCustomName =
            tools::classhelper::stream::container_from_stream<std::string>(is);

        is.read(reinterpret_cast<char*>(&xml.unknown_children), sizeof(xml.unknown_children));
        is.read(reinterpret_cast<char*>(&xml.unknown_attributes), sizeof(xml.unknown_attributes));

        return xml;
    }

    void to_stream(std::ostream& os) const
    {
        os.write(reinterpret_cast<const char*>(&TransducerAlphaX), sizeof(TransducerAlphaX) * 6);
        os.write(reinterpret_cast<const char*>(&TransducerSerialNumber),
                 sizeof(TransducerSerialNumber));
        tools::classhelper::stream::container_to_stream(os, TransducerMounting);
        tools::classhelper::stream::container_to_stream(os, TransducerOrientation);
        tools::classhelper::stream::container_to_stream(os, TransducerName);
        tools::classhelper::stream::container_to_stream(os, TransducerCustomName);

        os.write(reinterpret_cast<const char*>(&unknown_children), sizeof(unknown_children));
        os.write(reinterpret_cast<const char*>(&unknown_attributes), sizeof(unknown_attributes));
    }

    // ----- operators -----
    bool operator==(const XML_Configuration_Transducer& other) const
    {
        using tools::helper::approx;

        return approx(TransducerAlphaX, other.TransducerAlphaX) &&
               approx(TransducerAlphaY, other.TransducerAlphaY) &&
               approx(TransducerAlphaZ, other.TransducerAlphaZ) &&
               approx(TransducerOffsetX, other.TransducerOffsetX) &&
               approx(TransducerOffsetY, other.TransducerOffsetY) &&
               approx(TransducerOffsetZ, other.TransducerOffsetZ) &&
               approx(HeadingQuickCalibration, other.HeadingQuickCalibration) &&
               TransducerSerialNumber == other.TransducerSerialNumber &&
               TransducerMounting == other.TransducerMounting &&
               TransducerOrientation == other.TransducerOrientation &&
               TransducerName == other.TransducerName &&
               TransducerCustomName == other.TransducerCustomName;

        // && unknown_children == other.unknown_children &&
        // unknown_attributes == other.unknown_attributes;
    }
    bool operator!=(const XML_Configuration_Transducer& other) const { return !operator==(other); }

    // ----- objectprinter -----
    tools::classhelper::ObjectPrinter __printer__(unsigned int float_precision) const
    {
        tools::classhelper::ObjectPrinter printer("EK80 XML0 Configuration_Transducer",
                                                  float_precision);

        printer.register_section("attributes");
        printer.register_value("TransducerAlphaX", TransducerAlphaX);
        printer.register_value("TransducerAlphaY", TransducerAlphaY);
        printer.register_value("TransducerAlphaZ", TransducerAlphaZ);
        printer.register_value("TransducerOffsetX", TransducerOffsetX);
        printer.register_value("TransducerOffsetY", TransducerOffsetY);
        printer.register_value("TransducerOffsetZ", TransducerOffsetZ);
        printer.register_value(
            "HeadingQuickCalibration", HeadingQuickCalibration, "not used so far");
        printer.register_value("TransducerSerialNumber", TransducerSerialNumber);
        printer.register_value("TransducerMounting", TransducerMounting);
        printer.register_value("TransducerOrientation", TransducerOrientation);
        printer.register_value("TransducerName", TransducerName);
        printer.register_value("TransducerCustomName", TransducerCustomName);

        return printer;
    }

    // ----- class helper macros -----
    __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__ __STREAM_DEFAULT_TOFROM_BINARY_FUNCTIONS__(
        XML_Configuration_Transducer)
};

}
}
}
}
}