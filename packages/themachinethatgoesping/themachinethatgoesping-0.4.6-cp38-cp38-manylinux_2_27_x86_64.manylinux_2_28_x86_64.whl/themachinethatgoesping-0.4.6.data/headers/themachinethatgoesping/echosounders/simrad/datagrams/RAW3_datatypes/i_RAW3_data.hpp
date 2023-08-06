// SPDX-FileCopyrightText: 2022 Tim Weiß, GEOMAR Helmholtz Centre for Ocean Research Kiel
// SPDX-FileCopyrightText: 2022 Peter Urban, GEOMAR Helmholtz Centre for Ocean Research Kiel
// SPDX-FileCopyrightText: 2022 Peter Urban, Ghent University
//
// SPDX-License-Identifier: MPL-2.0

#pragma once

// std includes
#include <bitset>
#include <string>
#include <unordered_map>
#include <vector>

#include <boost/algorithm/string.hpp>

// xtensor includes
#include <xtensor/xadapt.hpp>
#include <xtensor/xarray.hpp>
#include <xtensor/xview.hpp>

// themachinethatgoesping import
#include <themachinethatgoesping/tools/classhelper/objectprinter.hpp>
#include <themachinethatgoesping/tools/helper.hpp>
#include <themachinethatgoesping/tools/timeconv.hpp>

#include "t_RAW3_datatype.hpp"

namespace themachinethatgoesping {
namespace echosounders {
namespace simrad {
namespace datagrams {
namespace RAW3_datatypes {

class i_RAW3_Data
{
    std::string_view _name;

  public:
    // ----- constructors -----
    i_RAW3_Data(std::string_view name)
        : _name(name)
    {
    }
    virtual ~i_RAW3_Data() = default;

    // ----- class interface -----
    std::string_view get_name() const { return _name; }

    virtual bool has_power() const { return false; }
    virtual bool has_angle() const { return false; }

    virtual xt::xtensor<simrad_float, 1> get_power([[maybe_unused]] bool dB = false) const
    {
        throw std::runtime_error("get_power() not implemented for " + std::string(_name));
    }
    virtual xt::xtensor<simrad_float, 2> get_angle() const
    {
        throw std::runtime_error("get_angle() not implemented for " + std::string(_name));
    }
};

}
}
}
}
}