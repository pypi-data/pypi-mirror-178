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
#include <themachinethatgoesping/tools/timeconv.hpp>

namespace themachinethatgoesping {
namespace echosounders {
namespace simrad {
namespace datagrams {
namespace xml_datagrams {

struct get_walker : pugi::xml_tree_walker
{
    std::string _a;
    std::string _b;

    virtual bool for_each(pugi::xml_node& node)
    {
        // for (int i = 0; i < depth(); ++i) std::cout << "  "; // indentation

        // print node name and value
        auto t = node.type();
        auto n = node.name();
        auto v = node.value();

        (void)t;
        (void)n;
        (void)v;

        // print node attributes
        for (pugi::xml_attribute attr : node.attributes())
        {
            _a = attr.name();
            _b = attr.value();
        }

        return true; // continue traversal
    }
};
struct print_walker : pugi::xml_tree_walker
{
    virtual bool for_each(pugi::xml_node& node)
    {
        std::string indent;
        for (int i = 0; i < depth(); ++i)
            indent += "  "; // indentation

        // print node name and value
        std::cout << indent << node.type() << ": name='" << node.name() << "', value='"
                  << node.value() << "'\n";

        // print node attributes
        for (pugi::xml_attribute attr : node.attributes())
            std::cout << indent << "  - " << attr.name() << " = '" << attr.value() << "'\n";

        return true; // continue traversal
    }
};

struct objectprint_walker : pugi::xml_tree_walker
{
    std::unordered_map<int, std::string> _root_nodes;

    tools::classhelper::ObjectPrinter& _printer;
    objectprint_walker(tools::classhelper::ObjectPrinter& printer)
        : _printer(printer)
    {
    }

    virtual bool for_each(pugi::xml_node& node)
    {
        std::string indent;
        for (int i = 0; i < depth(); ++i)
            indent += "  "; // indentation

        char underliner = '-';
        if (depth() == 1)
            underliner = '^';
        if (depth() > 1)
            underliner = '"';

        _root_nodes[depth()] = node.name();

        std::string section_name = indent + std::to_string(depth()) + ".: " + node.name();
        if (!std::string(node.value()).empty())
            section_name += "(val: " + std::string(node.value()) + ")";
        section_name += " ";

        for (int i = 0; i < depth(); ++i)
            section_name += "[" + _root_nodes[i] + "]";

        _printer.register_section(section_name, underliner);

        // print node attributes
        for (pugi::xml_attribute attr : node.attributes())
            _printer.register_string(attr.name(), attr.value(), node.name());

        return true; // continue traversal
    }
};

} // of namespace xml_datagrams
} // of namespace datagrams
} // of namespace simrad
} // of namespace echosounders
} // of namespace themachinethatgoesping