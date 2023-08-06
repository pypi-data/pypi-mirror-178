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
#include <themachinethatgoesping/tools/timeconv.hpp>

#include "helper.hpp"

namespace themachinethatgoesping {
namespace echosounders {
namespace simrad {
namespace datagrams {
namespace xml_datagrams {

/**
 * @brief XML base datagram
 *
 */
class XML_Node
{
    std::string                                            _name;
    std::unordered_map<std::string, std::vector<XML_Node>> _children;
    std::unordered_map<std::string, std::string>           _attributes;

  public:
    // ----- constructors -----
    XML_Node() = default;
    XML_Node(const pugi::xml_node& node) { initialize(node); }
    ~XML_Node() = default;

    void initialize(const pugi::xml_node& node)
    {
        _name = node.name();
        for (const auto& child : node.children())
        {
            _children[child.name()].emplace_back(XML_Node(child));
        }
        for (const auto& attribute : node.attributes())
        {
            _attributes.emplace(attribute.name(), attribute.value());
        }
    }

    // ----- operators -----
    bool operator==(const XML_Node& other) const
    {
        return _name == other._name && _children == other._children &&
               _attributes == other._attributes;
    }
    bool operator!=(const XML_Node& other) const { return !(*this == other); }

    // ----- getter/setter -----
    const std::string name() const { return _name; }
    void              name(std::string name) { _name = std::move(name); }

    const std::unordered_map<std::string, std::vector<XML_Node>>& children() const
    {
        return _children;
    }
    const std::vector<XML_Node>& children(const std::string& key) const
    {
        return _children.at(key);
    }
    const XML_Node& first_child(const std::string& key) const { return _children.at(key).at(0); }

    const std::unordered_map<std::string, std::string>& attributes() const { return _attributes; }
    const std::string& attributes(const std::string& key) const { return _attributes.at(key); }

    // ----- file I/O -----
    static XML_Node from_stream(std::istream& is)
    {
        XML_Node datagram;

        datagram._name = tools::classhelper::stream::container_from_stream<std::string>(is);

        size_t size;
        is.read(reinterpret_cast<char*>(&size), sizeof(size));

        for (size_t i = 0; i < size; ++i)
        {
            std::string key = tools::classhelper::stream::container_from_stream<std::string>(is);
            size_t      size_sub;
            is.read(reinterpret_cast<char*>(&size_sub), sizeof(size_sub));
            for (size_t j = 0; j < size_sub; ++j)
            {
                datagram._children[key].emplace_back(XML_Node::from_stream(is));
            }
        }

        is.read(reinterpret_cast<char*>(&size), sizeof(size));
        for (size_t i = 0; i < size; ++i)
        {
            std::string key   = tools::classhelper::stream::container_from_stream<std::string>(is);
            std::string value = tools::classhelper::stream::container_from_stream<std::string>(is);
            datagram._attributes.emplace(key, value);
        }

        return datagram;
    }

    void to_stream(std::ostream& os) const
    {
        tools::classhelper::stream::container_to_stream(os, _name);

        size_t size = _children.size();
        os.write(reinterpret_cast<const char*>(&size), sizeof(size_t));
        for (const auto& key_node : _children)
        {
            std::string key = key_node.first;
            tools::classhelper::stream::container_to_stream(os, key);

            size_t size_sub = key_node.second.size();
            os.write(reinterpret_cast<const char*>(&size_sub), sizeof(size_t));
            for (const auto& node : key_node.second)
            {
                node.to_stream(os);
            }
        }

        size = _attributes.size();
        os.write(reinterpret_cast<const char*>(&size), sizeof(size_t));
        for (const auto& key_value : _attributes)
        {
            std::string key   = key_value.first;
            std::string value = key_value.second;
            tools::classhelper::stream::container_to_stream(os, key);
            tools::classhelper::stream::container_to_stream(os, value);
        }
    }

    // ----- operators -----
    // bool operator==(const XML_Node& other) const { return _xml_content == other._xml_content; }
    // bool operator!=(const XML_Node& other) const { return !operator==(other); }

    // ----- objectprinter -----
    tools::classhelper::ObjectPrinter __printer__(unsigned int float_precision) const
    {
        tools::classhelper::ObjectPrinter printer("EK80 XML0 node '" + _name + "'",
                                                  float_precision);

        if (!_children.empty())
        {
            printer.register_section("children");
            for (auto& kv : _children)
                printer.register_value(kv.first, kv.second.size());
        }

        if (!_attributes.empty())
        {
            printer.register_section("attributes");

            for (auto& kv : _attributes)
                printer.register_value(kv.first, kv.second);
        }

        return printer;
    }

    // ----- class helper macros -----
    __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__ __STREAM_DEFAULT_TOFROM_BINARY_FUNCTIONS__(XML_Node)
};

}
}
}
}
}