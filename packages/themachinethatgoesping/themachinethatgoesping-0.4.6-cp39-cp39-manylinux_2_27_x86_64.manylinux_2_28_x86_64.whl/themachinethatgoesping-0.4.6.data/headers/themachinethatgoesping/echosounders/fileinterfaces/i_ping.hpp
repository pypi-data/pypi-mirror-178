// SPDX-FileCopyrightText: 2022 Peter Urban, GEOMAR Helmholtz Centre for Ocean Research Kiel
// SPDX-FileCopyrightText: 2022 Sven Schorge, GEOMAR Helmholtz Centre for Ocean Research Kiel
// SPDX-FileCopyrightText: 2022 Peter Urban, Ghent University
//
// SPDX-License-Identifier: MPL-2.0
//

#pragma once

/* std includes */
#include <filesystem>
#include <fstream>
#include <unordered_map>
#include <vector>

#include <fmt/core.h>

// xtensor includes
#include <xtensor/xadapt.hpp>
#include <xtensor/xarray.hpp>
#include <xtensor/xio.hpp>
#include <xtensor/xview.hpp>

/* themachinethatgoesping includes */
#include <themachinethatgoesping/tools/classhelper/objectprinter.hpp>
#include <themachinethatgoesping/tools/progressbars.hpp>

namespace themachinethatgoesping {
namespace echosounders {
namespace fileinterfaces {

class I_Ping
{
    std::string_view _name;

  public:
    I_Ping(std::string_view name)
        : _name(name)
    {
    }
    virtual ~I_Ping() = default;

    //------ interface ------//
    virtual void load_data() { throw not_implemented("load_data", _name); }
    virtual void release_data() { throw not_implemented("release_data", _name); }

    virtual size_t get_number_of_samples() const
    {
        throw not_implemented("get_number_of_samples", _name);
    }

    virtual xt::xtensor<float, 2> get_sv([[maybe_unused]] bool dB = false)
    {
        throw not_implemented("get_sv", _name);
    }
    virtual xt::xtensor<float, 1> get_sv_stacked([[maybe_unused]] bool dB = false)
    {
        throw not_implemented("get_sv_stacked", _name);
    }

    virtual xt::xtensor<float, 2> get_angle() { throw not_implemented("get_angle", _name); }

  private:
    struct not_implemented : public std::runtime_error
    {
        not_implemented(std::string_view method_name, std::string_view name)
            : std::runtime_error(
                  fmt::format("method {} not implemented for ping type '{}'", method_name, name))
        {
        }
    };
};

} // namespace fileinterfaces
} // namespace echosounders
} // namespace themachinethatgoesping