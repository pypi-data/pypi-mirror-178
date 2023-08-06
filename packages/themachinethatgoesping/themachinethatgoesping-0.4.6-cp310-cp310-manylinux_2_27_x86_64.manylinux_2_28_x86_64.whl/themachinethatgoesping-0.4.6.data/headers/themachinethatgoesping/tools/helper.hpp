// SPDX-FileCopyrightText: 2022 Peter Urban, Ghent University
// SPDX-FileCopyrightText: 2022 Drew Dormann (stackoverflow)
//
// SPDX-License-Identifier: MPL-2.0

#pragma once

#include <cmath>
#include <complex>
#include <string>
#include <variant>
#include <vector>

#include "fast_float/fast_float.h"

#include "helper/defaultmap.hpp"
#include "helper/defaultsharedpointermap.hpp"

namespace themachinethatgoesping {
namespace tools {
namespace helper {

// source https://gist.github.com/s3rvac/d1f30364ce1f732d75ef0c89a1c8c1ef
template<typename... Ts>
struct make_overload : Ts...
{
    using Ts::operator()...;
};
template<typename... Ts>
make_overload(Ts...) -> make_overload<Ts...>;

template<typename Variant, typename... Alternatives>
decltype(auto) visit_variant(Variant&& variant, Alternatives&&... alternatives)
{
    return std::visit(make_overload{ std::forward<Alternatives>(alternatives)... },
                      std::forward<Variant>(variant));
}

// usage:
//  visit_variant(v,
//          [](int i) { std::cout << i << '\n'; },
//          [](double d) { std::cout << d << '\n'; },
//          [](const std::string& s) { std::cout << s << '\n'; }
//      );

/**
 * @brief compare to floats using a relative difference factor
 *
 * @tparam t_float floating point type
 * @param f1 float/double 1
 * @param f2 float/double 1
 * @param relative_difference_factor relative factor by which the 2 numbers must be comparable
 * (default 0.01%)
 * @return true/false
 */
template<typename t_float>
bool approx(t_float f1, t_float f2, t_float relative_difference_factor = 0.0001 // 0.01%
)
{
    // if both are NAN return true
    if (std ::isnan(f1))
        if (std::isnan(f2))
            return true;

    // if both are inf (and same sign) return true
    if (std::isinf(f1))
        if (std::isinf(f2))
        {
            if (f1 < 0)
            {
                if (f2 < 0)
                    return true;
            }
            else
            {
                if (f2 > 0)
                    return true;
            }
        }

    // if the difference between both is smaller than the relative difference factor (compared to
    // the larger float) return true
    return std::abs(f1 - f2) <= relative_difference_factor * std::max(std::abs(f1), std::abs(f2));
}

template<typename t_float>
bool approx_complex(std::complex<t_float> f1,
                    std::complex<t_float> f2,
                    t_float               relative_difference_factor = 0.0001 /* 0.01% */)
{
    return approx(f1.real(), f2.real(), relative_difference_factor) &&
           approx(f1.imag(), f2.imag(), relative_difference_factor);
}

template<typename t_container>
bool approx_container(const t_container&               c1,
                      const t_container&               c2,
                      typename t_container::value_type relative_difference_factor = 0.0001 // 0.01%
)
{
    if (c1.size() != c2.size())
        return false;

    for (size_t i = 0; i < c1.size(); i++)
        if (!approx(c1[i], c2[i], relative_difference_factor))
            return false;

    return true;
}

template<typename t_container>
bool approx_container_complex(
    const t_container&                           c1,
    const t_container&                           c2,
    typename t_container::value_type::value_type relative_difference_factor = 0.0001f /* 0.01% */
)
{
    if (c1.size() != c2.size())
        return false;

    for (size_t i = 0; i < c1.size(); i++)
        if (!approx_complex(c1[i], c2[i], relative_difference_factor))
            return false;

    return true;
}

/**
 * @brief convert a string to float using fast_float::from_chars
 * Fast_float conforms to std::from_chars (c++17, but not completely implemented in clang yet)
 * The conversion is locale independent (. is the decimal separator)
 * see also: https://github.com/fastfloat/fast_float
 *
 * @param str if empty or non-numeric a NAN is returned
 * @return double
 */
inline double string_to_double(std::string_view str)
{
    if (str.empty())
        return std::numeric_limits<double>::quiet_NaN();

    double result;
    auto   answer = fast_float::from_chars(str.data(), str.data() + str.size(), result);

    if (answer.ec != std::errc())
        return std::numeric_limits<double>::quiet_NaN();

    return result;
}

inline std::vector<double> string_to_double_vector(std::string_view std, char delim = ',')
{
    std::vector<double>         result;
    std::string_view::size_type pos = 0;
    while (pos != std::string_view::npos)
    {
        auto next_pos = std.find(delim, pos);
        auto str      = std.substr(pos, next_pos - pos);
        result.push_back(string_to_double(str));
        pos = next_pos;
        if (pos != std::string_view::npos)
            pos++;
    }
    return result;
}

template<typename int_type>
inline std::string int_as_string(int_type value)
{
    std::string valueAsString;
    valueAsString.resize(sizeof(value));
    memcpy(valueAsString.data(), &value, sizeof(value));

    return valueAsString;
}

template<typename int_type>
inline int_type string_as_int(std::string_view value)
{
    int_type valueAsFourByteInt;
    memcpy(&valueAsFourByteInt, value.data(), sizeof(valueAsFourByteInt));
    return valueAsFourByteInt;
}

} // namespace helper
} // namespace tools
} // namespace themachinethatgoesping
