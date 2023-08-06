// SPDX-FileCopyrightText: 2022 Peter Urban, Ghent University
// SPDX-FileCopyrightText: 2022 Peter Urban, GEOMAR Helmholtz Centre for Ocean
// Research Kiel
//
// SPDX-License-Identifier: MPL-2.0

/**
 * @brief Nearest neighbor vector interpolator class.
 *
 * @authors Peter Urban
 *
 */

#pragma once

#include <array>
#include <iostream>
#include <unordered_map>
#include <vector>

#include "i_pairinterpolator.hpp"

#include "../classhelper/bitsery.hpp"
#include "../classhelper/objectprinter.hpp"
#include "../helper.hpp"

namespace themachinethatgoesping {
namespace tools {
namespace vectorinterpolators {

/**
 * @brief Interpolator class to find nearest neighbors within vector data
 *
 */
class NearestInterpolator : public I_PairInterpolator<double>
{
  public:
    NearestInterpolator(t_extr_mode extrapolation_mode = t_extr_mode::extrapolate)
        : I_PairInterpolator<double>(extrapolation_mode, "NearestInterpolator")
    {
    }

    /**
     * @brief Construct a new Nearest Interpolator object from a vector of pairs
     * usage: interpolated_y_value = interpolator.interpolate(x_value)
     *
     * @param X X vector; must be unique and sorted in ascending order. same size as Y!
     * @param Y Y vector; must be unique and sorted in ascending order. same size as X!
     * @param extrapolation_mode extrapolation mode (nearest or fail)
     */
    NearestInterpolator(const std::vector<double>& X,
                        const std::vector<double>& Y,
                        t_extr_mode                extrapolation_mode = t_extr_mode::extrapolate)
        : I_PairInterpolator<double>(X, Y, extrapolation_mode, "NearestInterpolator")
    {
    }
    ~NearestInterpolator() = default;

    static std::string type_to_string() { return "NearestInterpolator"; }

    bool operator!=(const NearestInterpolator& rhs) const { return !(rhs == *this); }
    bool operator==(const NearestInterpolator& rhs) const
    {
        // compare extrapolation mode
        if (_extr_mode != rhs.get_extrapolation_mode())
            return false;

        // compare data
        if (!helper::approx_container(_X, rhs._X))
            return false;
        if (!helper::approx_container(_Y, rhs._Y))
            return false;

        return true;
    }

    /**
     * @brief Interpolate interpolation between two values
     * @param target_x: the target point [0.0 - 1.0]
     * @param y1     : first y value (target_x = 0)
     * @param y2     : second value (target_x = 01)
     * between)
     * @return Interpolated value for target position
     */
    double interpolate_pair(double target_x, double y1, double y2) const final
    {
        if (target_x < 0.5)
            return y1;

        return y2;
    }

  private:
    // serialization support using bitsery
    friend bitsery::Access;
    template<typename S>
    void serialize(S& s)
    {
        s.value4b(_extr_mode);
        s.object(_last_x_pair);
        s.container8b(_X, SERIALIZER_DEFAULT_MAX_CONTAINER_SIZE);
        s.container8b(_Y, SERIALIZER_DEFAULT_MAX_CONTAINER_SIZE);
    }

  public:
    classhelper::ObjectPrinter __printer__(unsigned int float_precision) const
    {
        classhelper::ObjectPrinter printer(this->get_name(), float_precision);

        printer.register_enum("extr_mode", _extr_mode);
        printer.register_section("data lists");
        printer.register_container("X", _X);
        printer.register_container("Y", _Y);

        return printer;
    }

  public:
    // -- class helper function macros --
    // define to_binary and from_binary functions (needs the serialize function)
    __BITSERY_DEFAULT_TOFROM_BINARY_FUNCTIONS__(NearestInterpolator)
    // define info_string and print functions (needs the __printer__ function)
    __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__
};

} // namespace interpolation
} // namespace tools
} // namespace themachinethatgoesping
