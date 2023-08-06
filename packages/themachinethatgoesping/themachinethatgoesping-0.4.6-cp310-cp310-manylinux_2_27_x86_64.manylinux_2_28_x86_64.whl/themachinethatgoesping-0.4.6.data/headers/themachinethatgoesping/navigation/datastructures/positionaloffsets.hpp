// SPDX-FileCopyrightText: 2022 Peter Urban, Sven Schorge GEOMAR Helmholtz
// Centre for Ocean Research Kiel SPDX-FileCopyrightText: 2022 Peter Urban,
// Ghent University
//
// SPDX-License-Identifier: MPL-2.0

#pragma once

#include <themachinethatgoesping/tools/classhelper/bitsery.hpp>
#include <themachinethatgoesping/tools/classhelper/objectprinter.hpp>
#include <themachinethatgoesping/tools/helper.hpp>
#include <themachinethatgoesping/tools/rotationfunctions/quaternions.hpp>

namespace themachinethatgoesping {
namespace navigation {
namespace datastructures {

/**
 * @brief A structure to store positional offsets (e.g. of a sensor) relative to
 * the vessel coordinate system
 *
 */
struct PositionalOffsets
{
    std::string name;        ///< The name of the sensor
    double      x     = 0.0; ///< in m, positive forward
    double      y     = 0.0; ///< in m, positive starboard
    double      z     = 0.0; ///< in m, positive downwards
    double      yaw   = 0.0; ///< in °, positive means clockwise rotation
    double      pitch = 0.0; ///< in °, positive means bow up
    double      roll  = 0.0; ///< in °, positive means port up

    /**
     * @brief Construct a new Sensor Position object (all offsets set to 0)
     *
     */
    PositionalOffsets() = default;

    /**
     * @brief Construct a new PositionalOffsets object
     *
     * @param name The name of the sensor
     * @param x in m, positive forward
     * @param y in m, positive starboard
     * @param z in m, positive downwards
     * @param yaw positive means clockwise rotation
     * @param pitch in °, positive means bow up
     * @param roll in °, positive means port up
     */
    PositionalOffsets(std::string_view name,
                      double           x,
                      double           y,
                      double           z,
                      double           yaw,
                      double           pitch,
                      double           roll)
        : name(std::string(name))
        , x(x)
        , y(y)
        , z(z)
        , yaw(yaw)
        , pitch(pitch)
        , roll(roll)
    {
    }

    bool operator!=(const PositionalOffsets& rhs) const { return !(operator==(rhs)); }
    bool operator==(const PositionalOffsets& rhs) const
    {
        if (name == rhs.name)
            if (tools::helper::approx(x, rhs.x))
                if (tools::helper::approx(y, rhs.y))
                    if (tools::helper::approx(z, rhs.z))
                        if (tools::helper::approx(yaw, rhs.yaw))
                            if (tools::helper::approx(pitch, rhs.pitch))
                                if (tools::helper::approx(roll, rhs.roll))
                                    return true;

        return false;
    }

  private:
    // serialization support using bitsery
    friend bitsery::Access;
    template<typename S>
    void serialize(S& s)
    {
        s.container1b(name, 100);
        s.value8b(x);
        s.value8b(y);
        s.value8b(z);
        s.value8b(yaw);
        s.value8b(pitch);
        s.value8b(roll);
    }

  public:
    tools::classhelper::ObjectPrinter __printer__(unsigned int float_precision) const
    {
        tools::classhelper::ObjectPrinter printer("PositionalOffsets", float_precision);

        printer.register_string("name", name, "The name of the sensor");
        printer.register_value("x", x, "positive forwards, m");
        printer.register_value("y", y, "positive starboard, m");
        printer.register_value("z", z, "positive downwards, m");
        printer.register_value("yaw", yaw, "° positive means clockwise rotation");
        printer.register_value("pitch", pitch, "° positive means bow up");
        printer.register_value("roll", roll, "° positive means port up");

        return printer;
    }

  public:
    // -- class helper function macros --
    // define to_binary and from_binary functions (needs the serialize function)
    __BITSERY_DEFAULT_TOFROM_BINARY_FUNCTIONS__(PositionalOffsets)
    // define info_string and print functions (needs the __printer__ function)
    __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__
};

} // namespace datastructures
} // namespace navigation
} // namespace themachinethatgoesping