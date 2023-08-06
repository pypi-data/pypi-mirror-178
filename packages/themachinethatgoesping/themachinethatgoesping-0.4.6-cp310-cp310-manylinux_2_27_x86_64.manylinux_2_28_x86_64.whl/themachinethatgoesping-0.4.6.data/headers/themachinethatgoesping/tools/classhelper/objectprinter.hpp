// SPDX-FileCopyrightText: 2022 Peter Urban, Ghent University
// SPDX-FileCopyrightText: (c)2019 Michael Tesch. tesch1@gmail.com (struct
// fmt::formatter<std::complex<T>,Char> : public fmt::formatter<T,Char>)
//
// SPDX-License-Identifier: MPL-2.0

/**
 * @brief An object that allows for easy pretty printing of class members
 * usage:
 *  1. Implement a __printer__ function as public class member this function should return a
 *     ObjectPrinter object. Register all, values, containers, objects that are to be printed.
 *  2. Add the __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__ macro to the public functions.
 *     This macro implements std::string info_string() and print(std::ostream) functions using the
 * object printer
 *  3. Add the __PYCLASS_DEFAULT_PRINTING__ to the python module defintion. This macro implements
 *     __str__(), __repr__(), info_string() and print() as python functions
 *
 */

#pragma once

#include <algorithm>
#include <fmt/core.h>
#include <fmt/format.h>
#include <fmt/ostream.h>
#include <limits>
#include <magic_enum.hpp>
#include <numeric>

#include "../classhelper/bitsery.hpp"
#include <bitsery/traits/string.h>

// source https://gitlab.com/tesch1/cppduals/blob/master/duals/dual#L1379-1452
/// std::complex<> Formatter for libfmt https://github.com/fmtlib/fmt
///
/// libfmt does not provide a formatter for std::complex<>, although
/// one is proposed for c++20.  Anyway, at the expense of a k or two,
/// you can define CPPDUALS_LIBFMT_COMPLEX and get this one.
///
/// The standard iostreams formatting of complex numbers is (a,b),
/// where a and b are the real and imaginary parts.  This formats a
/// complex number (a+bi) as (a+bi), offering the same formatting
/// options as the underlying type - with the addition of three
/// optional format options, only one of which may appear directly
/// after the ':' in the format spec (before any fill or align): '$'
/// (the default if no flag is specified), '*', and ','.  The '*' flag
/// adds a * before the 'i', producing (a+b*i), where a and b are the
/// formatted value_type values.  The ',' flag simply prints the real
/// and complex parts separated by a comma (same as iostreams' format).
/// As a concrete exmple, this formatter can produce either (3+5.4i)
/// or (3+5.4*i) or (3,5.4) for a complex<double> using the specs {:g}
/// | {:$g}, {:*g}, or {:,g}, respectively.  (this implementation is a
/// bit hacky - glad for cleanups).
///
template<typename T, typename Char>
struct fmt::formatter<std::complex<T>, Char> : public fmt::formatter<T, Char>
{
    typedef fmt::formatter<T, Char> base;
    enum style
    {
        expr,
        star,
        pair
    } style_ = expr;
    fmt::detail::dynamic_format_specs<Char> specs_;
    FMT_CONSTEXPR auto parse(format_parse_context& ctx) -> decltype(ctx.begin())
    {
        using handler_type = fmt::detail::dynamic_specs_handler<format_parse_context>;
        auto                                     type = fmt::detail::type_constant<T, Char>::value;
        fmt::detail::specs_checker<handler_type> handler(handler_type(specs_, ctx), type);
        auto                                     it = ctx.begin();
        if (it != ctx.end())
        {
            switch (*it)
            {
                case '$':
                    style_ = style::expr;
                    ctx.advance_to(++it);
                    break;
                case '*':
                    style_ = style::star;
                    ctx.advance_to(++it);
                    break;
                case ',':
                    style_ = style::pair;
                    ctx.advance_to(++it);
                    break;
                default:
                    break;
            }
        }
        parse_format_specs(ctx.begin(), ctx.end(), handler);
        // todo: fixup alignment
        return base::parse(ctx);
    }
    template<typename FormatCtx>
    auto format(const std::complex<T>& x, FormatCtx& ctx) -> decltype(ctx.out())
    {
        format_to(ctx.out(), "(");
        if (style_ == style::pair)
        {
            base::format(x.real(), ctx);
            format_to(ctx.out(), ",");
            base::format(x.imag(), ctx);
            return format_to(ctx.out(), ")");
        }
        if (x.real() || !x.imag())
            base::format(x.real(), ctx);
        if (x.imag())
        {
            if (x.real() && x.imag() >= 0 && specs_.sign != sign::plus)
                format_to(ctx.out(), "+");
            base::format(x.imag(), ctx);
            if (style_ == style::star)
                format_to(ctx.out(), "*i");
            else
                format_to(ctx.out(), "i");
            if (std::is_same<typename std::decay<T>::type, float>::value)
                format_to(ctx.out(), "f");
            if (std::is_same<typename std::decay<T>::type, long double>::value)
                format_to(ctx.out(), "l");
        }
        return format_to(ctx.out(), ")");
    }
};

// --- print functions (need objectprinter __printer__ function that returns an ObjectPrinter) ---
#define __CLASSHELPER_PRINTER_INFO_STRING__                                                        \
    /**                                                                                            \
     * @brief return an info string using the class __printer__ object                             \
     * @param float_precision number of digits for floating point values                           \
     * @return std::string                                                                         \
     */                                                                                            \
    std::string info_string(unsigned int float_precision = 2) const                                \
    {                                                                                              \
        return this->__printer__(float_precision).create_str();                                    \
    }

#define __CLASSHELPER_PRINTER_PRINT__                                                              \
    /**                                                                                            \
     * @brief print the object information to the given outpustream                                \
     *                                                                                             \
     * @param os output stream, e.g. file stream or std::out or std::cerr                          \
     * @param float_precision number of digits for floating point values                           \
     */                                                                                            \
    void print(std::ostream& os, unsigned int float_precision = 2) const                           \
    {                                                                                              \
        os << this->__printer__(float_precision).create_str() << std::endl;                        \
    }

#define __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__                                                 \
    __CLASSHELPER_PRINTER_INFO_STRING__ __CLASSHELPER_PRINTER_PRINT__

namespace themachinethatgoesping {
namespace tools {
namespace classhelper {

/**
 * @brief Class that allows for easy pretty printing of class members
 * usage:
 *  1. Implement a __printer__ function as public class member this function should return a
 *     ObjectPrinter object. Register all, values, containers, objects that are to be printed.
 *  2. Add the __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__ macro to the public functions.
 *     This macro implements std::string info_string() and print(std::ostream) functions using the
 * object printer
 *  3. Add the __PYCLASS_DEFAULT_PRINTING__ to the python module defintion. This macro implements
 *     __str__(), __repr__(), info_string() and print() as python functions
 *
 */

class ObjectPrinter
{
    /**
     * @brief internal, describe the value type for implementing different printing strategies
     *
     */
    enum class t_field
    {
        tvalue,     ///< double or integer
        tenum,      ///< enumerator
        tcontainer, ///< 1D container (floating point or integer)
        tstring,    ///< formatted string field
        tsection    ///< section break
    };

    std::string                           _name;        ///< name of the class that is to be printed
    std::vector<std::string>              _fields;      ///< variable names
    std::vector<t_field>                  _field_types; ///< variable types
    std::vector<std::vector<std::string>> _lines;       ///< first line is typically the field value
    std::vector<std::string>              _value_infos; ///< additional info (printed in [])
    std::vector<char>                     _section_underliner; ///< additional info (printed in [])

    unsigned int _float_precision = 2;

    // serialization support using bitsery
    /**
     * @brief Construct a new Object Printer object
     *
     * @param float_precision default 2, set number of digits for floating point values
     */
    ObjectPrinter() = default;

    friend bitsery::Access;

    template<typename S>
    void serialize(S& s)
    {
        s.text1b(_name, 100);
        s.container(_fields, 1000, [](S& s_, std::string& str) { s_.text1b(str, 100); });
        s.container4b(_field_types, 1000);
        s.container(_lines, 1000, [](S& s_, std::vector<std::string>& str_vec) {
            s_.container(str_vec, 1000, [](S& s__, std::string& str) { s__.text1b(str, 100); });
        });
        s.container(_value_infos, 1000, [](S& s_, std::string& str) { s_.text1b(str, 100); });
        s.container1b(_section_underliner, 1000);
        s.value4b(_float_precision);
    }

  public:
    __BITSERY_DEFAULT_TOFROM_BINARY_FUNCTIONS__(ObjectPrinter)
    __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__

    ObjectPrinter __printer__(unsigned int float_precision) const
    {
        ObjectPrinter printer("ObjectPrinter", float_precision);

        printer.register_value("name", _name);
        printer.register_container("fields", _fields);
        printer.register_container("field_types", _field_types);

        // convert lines to string
        std::vector<std::string> lines;
        for (const auto& strl : _lines)
        {
            std::string str;
            for (const auto& s : strl)
            {
                if (str.size() != 0)
                    str += "; ";
                str += s;
            }
            lines.push_back(str);
        }
        printer.register_value("lines", fmt::format("... {} elements", _lines.size()));

        printer.register_container("value_infos", _value_infos);
        printer.register_container("section_underliner", _section_underliner);
        printer.register_value("float_precision", _float_precision);

        return printer;
    }

  public:
    /**
     * @brief Construct a new Object Printer object
     *
     * @param name name of the class that is to be printed
     */
    ObjectPrinter(std::string_view name, unsigned int float_precision)
        : _name(std::string(name))
        , _float_precision(float_precision)
    {
    }

    /**
     * @brief Remove all existing sections
     *
     */
    void remove_sections()
    {
        for (size_t i = 0; i < _field_types.size(); i++)
        {
            if (_field_types[i] == t_field::tsection)
            {
                _fields.erase(_fields.begin() + i);
                _field_types.erase(_field_types.begin() + i);
                _lines.erase(_lines.begin() + i);
                _value_infos.erase(_value_infos.begin() + i);
                _section_underliner.erase(_section_underliner.begin() + i);
                i--;
            }
        }
    }

    /**
     * @brief Append the fields of an existing object printer
     *
     * @param printer printer to be appended
     */
    void append(ObjectPrinter printer, char remove_sections = false, char section_underliner = 0)
    {
        if (remove_sections)
            printer.remove_sections();

        _fields.insert(_fields.end(), printer._fields.begin(), printer._fields.end());
        _field_types.insert(
            _field_types.end(), printer._field_types.begin(), printer._field_types.end());
        _lines.insert(_lines.end(), printer._lines.begin(), printer._lines.end());
        _value_infos.insert(
            _value_infos.end(), printer._value_infos.begin(), printer._value_infos.end());

        if (!section_underliner)
            _section_underliner.insert(_section_underliner.end(),
                                       printer._section_underliner.begin(),
                                       printer._section_underliner.end());
        else
            for ([[maybe_unused]] const auto& c : printer._section_underliner)
                _section_underliner.push_back(section_underliner);
    }

    // --- functions to register values for printing ----

    /**
     * @brief register an enumeration for printing
     *
     * @tparam t_value enumerator
     * @param name name of the variable
     * @param value value of the variable
     * @param value_info additional info (is printed in [] behind the variable)
     * @param pos position where the value is registers (if negative, the value is appended)
     */
    template<typename t_value>
    void register_enum(const std::string& name,
                       t_value            value,
                       std::string        value_info = "",
                       int                pos        = -1)
    {
        std::string str;

        // convert enum value to string using magic_enum library
        str = magic_enum::enum_name(value);

        // create string of all possible enum values
        constexpr auto enum_values = magic_enum::enum_names<t_value>();
        for (unsigned int i = 0; i < enum_values.size(); ++i)
        {
            if (i != 0)
                value_info += ", ";

            value_info += enum_values[i];
        }

        // attach all possible enum values as value_info
        std::string value_info_str = "";
        if (value_info.size() > 0)
            value_info_str = fmt::format("[{}]", value_info);

        if (pos < 0 || pos >= int(_fields.size()))
        {
            _fields.push_back(name);
            _lines.push_back({ str }); // only one line (value)
            _field_types.push_back(t_field::tenum);
            _value_infos.push_back(value_info_str);
            _section_underliner.push_back(' ');
        }
        else
        {
            _fields.insert(_fields.begin() + pos, name);
            _lines.insert(_lines.begin() + pos, { str }); // only one line (value)
            _field_types.insert(_field_types.begin() + pos, t_field::tenum);
            _value_infos.insert(_value_infos.begin() + pos, value_info_str);
            _section_underliner.insert(_section_underliner.begin() + pos, ' ');
        }
    }

    /**
     * @brief register a single integer of floating point value for printing
     *
     * @tparam t_value double or floating point
     * @param name name of the variable
     * @param value value of the variable
     * @param value_info additional info (is printed in [] behind the variable)
     * @param pos position where the value is registers (if negative, the value is appended)
     */
    template<typename t_value>
    void register_value(const std::string& name,
                        t_value            value,
                        std::string        value_info = "",
                        int                pos        = -1)
    {
        std::string str;

        // convert value to string
        if constexpr (std::is_floating_point<t_value>())
            str = fmt::format("{:.{}f}", value, _float_precision);
        else
            str = fmt::format("{}", value);

        // add value information
        std::string value_info_str = "";
        if (value_info.size() > 0)
            value_info_str = fmt::format("[{}]", value_info);

        if (pos < 0 || pos >= int(_fields.size()))
        {
            _fields.push_back(name);
            _lines.push_back({ str });
            _field_types.push_back(t_field::tvalue);
            _value_infos.push_back(value_info_str);
            _section_underliner.push_back(' ');
        }
        else
        {
            _fields.insert(_fields.begin() + pos, name);
            _lines.insert(_lines.begin() + pos, { str });
            _field_types.insert(_field_types.begin() + pos, t_field::tvalue);
            _value_infos.insert(_value_infos.begin() + pos, value_info_str);
            _section_underliner.insert(_section_underliner.begin() + pos, ' ');
        }
    }

    /**
     * @brief register a 1D container for printing
     *
     * @tparam t_value integer or floating point
     * @param name name of the container
     * @param value container values
     * @param value_info additional info (is printed in [] behind the variable)
     * @param pos position where the value is registers (if negative, the value is appended)
     */
    template<typename t_container>
    void register_container(const std::string& name,
                            const t_container& values,
                            std::string        value_info = "",
                            int                pos        = -1)
    {
        static const size_t max_visible_elements = 9; // maximum values to display for a vector
        std::string         str, format;
        using t_value = typename t_container::value_type;

        // define value to string format
        if constexpr (std::is_floating_point<typename t_container::value_type>())
            format = "{:.6g}"; // 6 characters, automatic scientific notation depending on magnitude
        else if constexpr (std::is_base_of<t_value, std::string>())
            format = "\"{}\"";
        else
            format = "{}";

        // add values to {} list
        str = "{";
        for (size_t i = 0; i < values.size(); ++i)
        {
            if (i != 0)
                str += ", ";

            // don't print entire list of > max_visible_elements in vector
            if (values.size() > max_visible_elements)
                if (i == size_t(max_visible_elements / 2) - 1)
                {
                    str += "..., ..., ...";
                    i = values.size() - size_t(max_visible_elements / 2);
                    continue;
                }
            if constexpr (std::is_enum<t_value>())
                str += magic_enum::enum_name(values[i]);
            else
                str += fmt::format(format, values[i]);
        }
        str += "}";

        // add value information
        std::string value_info_str = "";
        if (value_info.size() > 0)
            value_info_str = fmt::format("[{}]", value_info);

        if (pos < 0 || pos >= int(_fields.size()))
        {
            _fields.push_back(name);
            _lines.push_back({ str });
            _field_types.push_back(t_field::tcontainer);
            _value_infos.push_back(value_info_str);
            _section_underliner.push_back(' ');
        }
        else
        {
            _fields.insert(_fields.begin() + pos, name);
            _lines.insert(_lines.begin() + pos, { str });
            _field_types.insert(_field_types.begin() + pos, t_field::tcontainer);
            _value_infos.insert(_value_infos.begin() + pos, value_info_str);
            _section_underliner.insert(_section_underliner.begin() + pos, ' ');
        }

        auto& line_ref = _lines.back();
        if (pos >= 0 || pos >= int(_fields.size()))
            line_ref = _lines.at(pos);

        // add vector statistics if not all elements are displayed
        if (values.size() > max_visible_elements)
        {
            // begin statistics for numbers
            if constexpr (std::is_floating_point<t_value>() || std::is_integral<t_value>())
            {

                {
                    // copy vector once to modify it
                    std::vector<t_value> v;
                    size_t               cnt_nan   = 0; ///< number of nan values
                    size_t               cnt_inf   = 0; ///< number of positive infinity values
                    size_t               cnt_inf_n = 0; ///< number of negative infinity values

                    // count nans and infs and copy normal values to v
                    if constexpr (std::is_floating_point<t_value>())
                    {
                        for (const auto& value : values)
                        {
                            if (std::isnan(value))
                            {
                                ++cnt_nan;
                                continue;
                            }

                            if (std::isinf(value))
                            {
                                if (value < 0)
                                    ++cnt_inf_n;
                                else
                                    ++cnt_inf;
                                continue;
                            }

                            v.push_back(value);
                        }
                    }
                    else
                    // copy all values to v
                    {
                        v.resize(values.size());
                        std::copy(values.begin(), values.end(), v.begin());
                    }

                    // get statistics from nan/inf cleaned lists
                    auto minmax = std::minmax_element(std::begin(v), std::end(v));
                    auto mean   = std::reduce(std::begin(v), std::end(v)) / v.size();

                    // compute median
                    size_t n_2 = v.size() / 2;
                    std::nth_element(v.begin(), v.begin() + n_2, v.end());

                    // -- print statistics 1 --
                    std::string line_format =
                        fmt::format("... Min:  {} | Max: {} | Mean: {}", format, format, format);
                    line_ref.push_back(
                        fmt::format(line_format, *(minmax.first), *(minmax.second), mean));

                    // print median (special case for even numbers)
                    if (v.size() % 2)
                    {
                        std::nth_element(v.begin(), v.begin() + n_2 + 1, v.end());
                        line_ref.back() +=
                            fmt::format("| Median: " + format, (v[n_2] + v[n_2 + 1]) / 2);
                    }
                    else
                    {
                        line_ref.back() += fmt::format(" | Median: " + format, v[n_2]);
                    }

                    // -- print statistics 2 --
                    // value count
                    line_ref.push_back(fmt::format("... {} elements", values.size()));

                    // for floating point vectors, add number of nan/inf elements to info
                    if constexpr (std::is_floating_point<t_value>())
                    {
                        if (cnt_nan || cnt_inf || cnt_inf_n)
                        {
                            line_ref.back() += fmt::format(" ! NAN elements: ");

                            if (cnt_nan)
                            {
                                line_ref.back() += fmt::format("nan({})", cnt_nan);
                                if (cnt_inf || cnt_inf_n)
                                    line_ref.back() += ", ";
                            }
                            if (cnt_inf_n)
                            {
                                line_ref.back() += fmt::format("-inf({})", cnt_inf_n);
                                if (cnt_inf)
                                    line_ref.back() += ", ";
                            }
                            if (cnt_inf)
                            {
                                line_ref.back() += fmt::format("+inf({})", cnt_inf);
                            }
                        }
                    }
                }
            }
            else // end number statistics
            {
                // statistics also for not number containers
                line_ref.push_back(fmt::format("... {} elements", values.size()));
            }
        }
    }

    /**
     * @brief register a formatted string field for printing
     *
     * @param name name of the variable
     * @param value value of the variable
     * @param value_info additional info (is printed in [] behind the variable)
     * @param pos position where the value is registers (if negative, the value is appended)
     */
    void register_string(const std::string& name,
                         const std::string& value,
                         std::string        value_info = "",
                         int                pos        = -1)
    {
        if (value_info.size() > 0)
            value_info = fmt::format("[{}]", value_info);

        std::vector<std::string> lines;

        // split string into lines
        std::string::size_type start = 0;
        std::string::size_type end   = 0;
        while ((end = value.find('\n', start)) != std::string::npos)
        {
            lines.push_back(value.substr(start, end - start));
            start = end + 1;
        }
        lines.push_back(value.substr(start));

        if (pos < 0 || pos >= int(_fields.size()))
        {
            _fields.push_back(name);
            _lines.push_back(lines);
            _field_types.push_back(t_field::tstring);
            _value_infos.push_back(value_info);
            _section_underliner.push_back(' ');
        }
        else
        {
            _fields.insert(_fields.begin() + pos, name);
            _lines.insert(_lines.begin() + pos, lines);
            _field_types.insert(_field_types.begin() + pos, t_field::tstring);
            _value_infos.insert(_value_infos.begin() + pos, value_info);
            _section_underliner.insert(_section_underliner.begin() + pos, ' ');
        }

        // if (pos < 0 || pos >= int(_fields.size()))
        // {
        //     _fields.push_back(name);
        //     _lines.push_back({value});
        //     _value_infos.push_back(value_info);
        //     _field_types.push_back(t_field::tstring);
        //     _section_underliner.push_back(' ');
        // }
        // else
        // {
        //     _fields.insert(_fields.begin() + pos, name);
        //     _lines.insert(_lines.begin() + pos, {value});
        //     _value_infos.insert(_value_infos.begin() + pos, value_info);
        //     _field_types.insert(_field_types.begin() + pos, t_field::tstring);
        //     _section_underliner.insert(_section_underliner.begin() + pos, ' ');
        // }
    }

    /**
     * @brief register a section break for printing
     *
     * @param name name of the following section
     * @param underliner character used to underline the section name
     * @param pos position where the value is registers (if negative, the value is appended)
     */
    void register_section(const std::string& name, char underliner = '-', int pos = -1)
    {
        if (pos < 0 || pos >= int(_fields.size()))
        {
            _fields.push_back(name);
            _lines.push_back({ "" });
            _value_infos.push_back({ "" });
            _field_types.push_back(t_field::tsection);
            _section_underliner.push_back(underliner);
        }
        else
        {
            _fields.insert(_fields.begin() + pos, name);
            _lines.insert(_lines.begin() + pos, { "" });
            _value_infos.insert(_value_infos.begin() + pos, { "" });
            _field_types.insert(_field_types.begin() + pos, t_field::tsection);
            _section_underliner.insert(_section_underliner.begin() + pos, underliner);
        }
    }

    /**
     * @brief Get the registered name of the object
     *
     * @return std::string
     */
    std::string get_name() const { return _name; }

    /**
     * @brief Create an info_string from the registered values/sections
     *
     * @return std::string
     */
    std::string create_str() const
    {
        std::vector<std::string> str_lines; // individual lines

        std::vector<size_t> max_len_field = { 0 }; // max string len of field name
        std::vector<size_t> max_len_value = { 0 }; // max string len of field + value

        // get max_len_field for each section
        // this is used for aligning the values for each section
        for (size_t i = 0; i < _fields.size(); ++i)
        {
            if (_field_types[i] == t_field::tsection)
            {
                max_len_field.back() += 1;
                max_len_field.push_back(0);
                continue;
            }

            if (_fields[i].size() > max_len_field.back())
                max_len_field.back() = _fields[i].size();
        }
        max_len_field.back() += 1;

        // create string depending on field type
        auto section_nr = 0;
        for (unsigned int i = 0; i < _fields.size(); ++i)
        {
            std::string prefix = "";
            if (i > 0)
            {
                // add \n if previous element had multiple str_lines
                if (_field_types[i - 1] != t_field::tsection)
                    if (_lines[i - 1].size() > 1)
                        prefix = "\n";
            }
            switch (_field_types[i])
            {

                case t_field::tsection:
                    section_nr += 1;

                    max_len_value.push_back(0);
                    if (i == 0)
                        str_lines.push_back(
                            underline("-\n" + _fields[i] + " ", _section_underliner[i]));
                    else
                        str_lines.push_back(
                            "\n" + underline(" " + _fields[i] + " ", _section_underliner[i]));

                    continue;
                case t_field::tvalue:
                    str_lines.push_back(fmt::format(prefix + "- {:<{}} {}",
                                                    _fields[i] + ':',
                                                    max_len_field[section_nr],
                                                    _lines[i][0]));
                    break;
                case t_field::tstring:
                    str_lines.push_back(fmt::format(prefix + "- {:<{}} {}",
                                                    _fields[i] + ':',
                                                    max_len_field[section_nr],
                                                    _lines[i][0]));
                    break;
                case t_field::tenum:
                    str_lines.push_back(fmt::format(prefix + "- {:<{}} {}",
                                                    _fields[i] + ':',
                                                    max_len_field[section_nr],
                                                    _lines[i][0]));
                    break;
                case t_field::tcontainer:
                    str_lines.push_back(fmt::format(prefix + "- {:<{}} {}",
                                                    _fields[i] + ':',
                                                    max_len_field[section_nr],
                                                    _lines[i][0]));
                    break;

                default:
                    throw(std::runtime_error("ObjectPrinter::str: unknown field type"));
            }

            if (str_lines.back().size() > max_len_value.back())
                max_len_value.back() = str_lines.back().size();
        }

        // If no variables are added, do not underline the object name
        if (str_lines.size() == 0)
            return _name;

        std::string str = underline(_name, '#');
        section_nr      = 0;
        for (size_t i = 0; i < str_lines.size(); ++i)
        {
            if (_field_types[i] == t_field::tsection)
            {
                section_nr += 1;
            }

            str += fmt::format(
                "\n{:<{}} {}", str_lines[i], max_len_value[section_nr], _value_infos[i]);

            for (size_t j = 1; j < _lines[i].size(); ++j)
                // str += fmt::format("\n  {}", _lines[i][j]);
                str += fmt::format("\n{:<{}}  {}", "", max_len_field[section_nr], _lines[i][j]);
        }

        return str;
    }

    /**
     * @brief add a line under a given line string
     *
     * @param line input string
     * @return std::string
     */
    static std::string underline(const std::string& line, char underliner)
    {
        std::string str = line;
        for (unsigned int i = 0; i < line.size(); ++i)
        {
            if (i == 0)
                str += '\n';

            str += underliner;
        }

        return str;
    }
};

}
}
}
