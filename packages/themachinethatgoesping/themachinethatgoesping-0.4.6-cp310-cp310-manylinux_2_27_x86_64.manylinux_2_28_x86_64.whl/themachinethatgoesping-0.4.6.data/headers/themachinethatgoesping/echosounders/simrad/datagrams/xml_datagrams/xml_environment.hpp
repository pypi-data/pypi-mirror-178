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
#include "xml_environment_transducer.hpp"
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
struct XML_Environment
{
    double              WaterLevelDraft        = NAN;
    bool                DropKeelOffsetIsManual = false;
    double              DropKeelOffset         = NAN;
    std::vector<double> SoundVelocityProfile;
    bool                WaterLevelDraftIsManual = false;
    double              Latitude                = NAN;
    double              SoundSpeed              = NAN;
    double              Salinity                = NAN;
    std::string         SoundVelocitySource;
    double              Acidity     = NAN;
    double              Temperature = NAN;
    double              Depth       = NAN;

    bool   TowedBodyDepthIsManual = false;
    double TowedBodyDepth         = NAN;

    std::vector<XML_Environment_Transducer> Transducers;

    int32_t unknown_children   = 0;
    int32_t unknown_attributes = 0;

  public:
    // ----- constructors -----
    XML_Environment() = default;
    XML_Environment(const pugi::xml_node& node) { initialize(node); }
    ~XML_Environment() = default;

    void initialize(const pugi::xml_node& root_node)
    {
        if (strcmp(root_node.name(), "Environment"))
        {
            throw std::runtime_error(std::string("XML_Environment: wrong root node type '") +
                                     root_node.name() + "'");
        }
        unknown_attributes = 0;
        unknown_children   = 0; // there should only be one child for this node

        // there should only be one child for this node
        for (const auto& node : root_node.children())
        {
            if (strcmp(node.name(), "Transducer"))
            {
                std::cerr << "WARNING: [Environment] Unknown child: " << node.name() << std::endl;

                unknown_children = 1;

                continue;
            }

            Transducers.emplace_back(node);
        }

        for (auto& attr : root_node.attributes())
        {
            std::string_view name = attr.name();
            if (name == "WaterLevelDraft")
            {
                WaterLevelDraft = tools::helper::string_to_double(attr.value());
                continue;
            }
            if (name == "DropKeelOffsetIsManual")
            {
                DropKeelOffsetIsManual = std::stoi(
                    attr.value()); // TODO: can this value only be 0 and 1 or also true and false?
                continue;
            }
            if (name == "DropKeelOffset")
            {
                DropKeelOffset = tools::helper::string_to_double(attr.value());
                continue;
            }
            if (name == "SoundVelocityProfile")
            {
                SoundVelocityProfile = tools::helper::string_to_double_vector(attr.value(), ';');
                continue;
            }
            if (name == "WaterLevelDraftIsManual")
            {
                WaterLevelDraftIsManual = std::stoi(
                    attr.value()); // TODO: can this value only be 0 and 1 or also true and false?
                continue;
            }
            if (name == "Latitude")
            {
                Latitude = tools::helper::string_to_double(attr.value());
                continue;
            }
            if (name == "SoundSpeed")
            {
                SoundSpeed = tools::helper::string_to_double(attr.value());
                continue;
            }
            if (name == "Salinity")
            {
                Salinity = tools::helper::string_to_double(attr.value());
                continue;
            }
            if (name == "SoundVelocitySource")
            {
                SoundVelocitySource = attr.value();
                continue;
            }
            if (name == "Acidity")
            {
                Acidity = tools::helper::string_to_double(attr.value());
                continue;
            }
            if (name == "Temperature")
            {
                Temperature = tools::helper::string_to_double(attr.value());
                continue;
            }
            if (name == "Depth")
            {
                Depth = tools::helper::string_to_double(attr.value());
                continue;
            }
            if (name == "TowedBodyDepthIsManual")
            {
                TowedBodyDepthIsManual = std::stoi(attr.value());
                continue;
            }
            if (name == "TowedBodyDepth")
            {
                TowedBodyDepth = tools::helper::string_to_double(attr.value());
                continue;
            }

            std::cerr << "WARNING: [Environment] Unknown attribute: " << name << std::endl;
            unknown_attributes += 1;
        }
    }

    bool parsed_completely() const { return unknown_children == 0 && unknown_attributes == 0; }

    // ----- file I/O -----
    static XML_Environment from_stream(std::istream& is)
    {
        XML_Environment xml;

        is.read(reinterpret_cast<char*>(&xml.WaterLevelDraft), sizeof(xml.WaterLevelDraft));
        is.read(reinterpret_cast<char*>(&xml.DropKeelOffsetIsManual),
                sizeof(xml.DropKeelOffsetIsManual));
        is.read(reinterpret_cast<char*>(&xml.DropKeelOffset), sizeof(xml.DropKeelOffset));
        xml.SoundVelocityProfile =
            tools::classhelper::stream::container_from_stream<std::vector<double>>(is);
        is.read(reinterpret_cast<char*>(&xml.WaterLevelDraftIsManual),
                sizeof(xml.WaterLevelDraftIsManual));
        is.read(reinterpret_cast<char*>(&xml.Latitude), sizeof(xml.Latitude));
        is.read(reinterpret_cast<char*>(&xml.SoundSpeed), sizeof(xml.SoundSpeed));
        is.read(reinterpret_cast<char*>(&xml.Salinity), sizeof(xml.Salinity));
        xml.SoundVelocitySource =
            tools::classhelper::stream::container_from_stream<std::string>(is);
        is.read(reinterpret_cast<char*>(&xml.Acidity), sizeof(xml.Acidity));
        is.read(reinterpret_cast<char*>(&xml.Temperature), sizeof(xml.Temperature));
        is.read(reinterpret_cast<char*>(&xml.Depth), sizeof(xml.Depth));
        is.read(reinterpret_cast<char*>(&xml.TowedBodyDepthIsManual),
                sizeof(xml.TowedBodyDepthIsManual));
        is.read(reinterpret_cast<char*>(&xml.TowedBodyDepth), sizeof(xml.TowedBodyDepth));

        size_t size;
        is.read(reinterpret_cast<char*>(&size), sizeof(size));
        xml.Transducers.resize(size);
        for (auto& value : xml.Transducers)
        {
            value = XML_Environment_Transducer::from_stream(is);
        }

        is.read(reinterpret_cast<char*>(&xml.unknown_children), sizeof(xml.unknown_children));
        is.read(reinterpret_cast<char*>(&xml.unknown_attributes), sizeof(xml.unknown_attributes));

        return xml;
    }

    void to_stream(std::ostream& os) const
    {
        os.write(reinterpret_cast<const char*>(&WaterLevelDraft), sizeof(WaterLevelDraft));
        os.write(reinterpret_cast<const char*>(&DropKeelOffsetIsManual),
                 sizeof(DropKeelOffsetIsManual));
        os.write(reinterpret_cast<const char*>(&DropKeelOffset), sizeof(DropKeelOffset));
        tools::classhelper::stream::container_to_stream(os, SoundVelocityProfile);
        os.write(reinterpret_cast<const char*>(&WaterLevelDraftIsManual),
                 sizeof(WaterLevelDraftIsManual));
        os.write(reinterpret_cast<const char*>(&Latitude), sizeof(Latitude));
        os.write(reinterpret_cast<const char*>(&SoundSpeed), sizeof(SoundSpeed));
        os.write(reinterpret_cast<const char*>(&Salinity), sizeof(Salinity));
        tools::classhelper::stream::container_to_stream(os, SoundVelocitySource);
        os.write(reinterpret_cast<const char*>(&Acidity), sizeof(Acidity));
        os.write(reinterpret_cast<const char*>(&Temperature), sizeof(Temperature));
        os.write(reinterpret_cast<const char*>(&Depth), sizeof(Depth));
        os.write(reinterpret_cast<const char*>(&TowedBodyDepthIsManual),
                 sizeof(TowedBodyDepthIsManual));
        os.write(reinterpret_cast<const char*>(&TowedBodyDepth), sizeof(TowedBodyDepth));

        size_t size = Transducers.size();
        os.write(reinterpret_cast<const char*>(&size), sizeof(size));
        for (const auto& value : Transducers)
        {
            value.to_stream(os);
        }

        os.write(reinterpret_cast<const char*>(&unknown_children), sizeof(unknown_children));
        os.write(reinterpret_cast<const char*>(&unknown_attributes), sizeof(unknown_attributes));
    }

    // ----- operators -----
    bool operator==(const XML_Environment& other) const
    {
        using namespace tools::helper;

        return approx(WaterLevelDraft, other.WaterLevelDraft) &&
               DropKeelOffsetIsManual == other.DropKeelOffsetIsManual &&
               approx(DropKeelOffset, other.DropKeelOffset) &&
               approx_container(SoundVelocityProfile, other.SoundVelocityProfile) &&
               WaterLevelDraftIsManual == other.WaterLevelDraftIsManual &&
               approx(Latitude, other.Latitude) && approx(SoundSpeed, other.SoundSpeed) &&
               approx(Salinity, other.Salinity) &&
               SoundVelocitySource == other.SoundVelocitySource && approx(Acidity, other.Acidity) &&
               approx(Temperature, other.Temperature) && approx(Depth, other.Depth) &&
               TowedBodyDepthIsManual == other.TowedBodyDepthIsManual &&
               approx(TowedBodyDepth, other.TowedBodyDepth) && Transducers == other.Transducers;

        // && unknown_children == other.unknown_children &&
        // unknown_attributes == other.unknown_attributes;
    }
    bool operator!=(const XML_Environment& other) const { return !operator==(other); }

    // ----- objectprinter -----
    tools::classhelper::ObjectPrinter __printer__(unsigned int float_precision) const
    {
        tools::classhelper::ObjectPrinter printer("EK80 XML0 Environment", float_precision);

        printer.register_section("children (Transducers / Future use)");
        printer.register_value("Transducers", Transducers.size());

        printer.register_section("attributes");

        printer.register_value("WaterLevelDraft", WaterLevelDraft, "m");
        printer.register_value("DropKeelOffsetIsManual", DropKeelOffsetIsManual);
        printer.register_value("DropKeelOffset", DropKeelOffset, "m");
        printer.register_container(
            "SoundVelocityProfile", SoundVelocityProfile, "z[m], c[m/s], ...");
        printer.register_value("WaterLevelDraftIsManual", WaterLevelDraftIsManual);
        printer.register_value("Latitude", Latitude, "°");
        printer.register_value("SoundSpeed", SoundSpeed, "m/s");
        printer.register_value("Salinity", Salinity);
        printer.register_string("SoundVelocitySource", SoundVelocitySource);
        printer.register_value("Acidity", Acidity);
        printer.register_value("Temperature", Temperature, "C°");
        printer.register_value("Depth", Depth, "m");
        printer.register_value("TowedBodyDepthIsManual", TowedBodyDepthIsManual);
        printer.register_value("TowedBodyDepth", TowedBodyDepth, "m");

        printer.register_value("unknown_children", unknown_children);
        printer.register_value("unknown_attributes", unknown_attributes);

        return printer;
    }

    // ----- class helper macros -----
    __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__ __STREAM_DEFAULT_TOFROM_BINARY_FUNCTIONS__(
        XML_Environment)
};

}
}
}
}
}