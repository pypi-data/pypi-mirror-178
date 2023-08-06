// SPDX-FileCopyrightText: 2022 Peter Urban, Sven Schorge, GEOMAR Helmholtz Centre for Ocean
// Research Kiel SPDX-FileCopyrightText: 2022 Peter Urban, Ghent University
//
// SPDX-License-Identifier: MPL-2.0

#pragma once

#include <themachinethatgoesping/tools/classhelper/bitsery.hpp>
#include <themachinethatgoesping/tools/classhelper/objectprinter.hpp>
#include <themachinethatgoesping/tools/vectorinterpolators.hpp>

#include "datastructures.hpp"
#include "sensorconfiguration.hpp"

namespace themachinethatgoesping {
namespace navigation {

/**
 * @brief The NavInterpolator class: Interpolate attitude information and transform the
 * values using the offsets specified in the sensor configuration class
 * This is an interface class that specifies attitude information but not the position
 */
class I_NavigationInterpolator
{
    std::string_view _name;

  protected:
    std::string_view get_name() const { return _name; }

    SensorConfiguration _sensor_configuration; ///< sensor configuration that stores the offsets

    // SlerpInterpolator that stores timestamp, roll, pitch, yaw -> Attitude of Vessel on the Water
    tools::vectorinterpolators::SlerpInterpolator
        _interpolator_attitude; ///< interpolator that stores attitude data (pitch and roll)
    tools::vectorinterpolators::SlerpInterpolator
        _interpolator_heading; ///< interpolator that stores compass data (yaw/heading) [°]

    // LinearInterpolator for the depth in the world coordinate system
    tools::vectorinterpolators::AkimaInterpolator
        _interpolator_heave; ///< interpolator that stores heave data (relative change in depth,
                             ///< positive upwards) [m]
    // tools::vectorinterpolators::AkimaInterpolator // bad results for noisy data
    tools::vectorinterpolators::LinearInterpolator
        _interpolator_depth; ///< interpolator that stores depth data (depth, positive downwards)
                             ///< [m]

  public:
    /**
     * @brief Construct a new i navigationinterpolator interface
     *
     * @param extrapolation_mode extrapolate, fail or nearest
     */
    I_NavigationInterpolator(const SensorConfiguration&              sensor_configuration,
                             tools::vectorinterpolators::t_extr_mode extrapolation_mode =
                                 tools::vectorinterpolators::t_extr_mode::extrapolate,
                             std::string_view name = "I_NavigationInterpolator")
        : _name(name)
        , _sensor_configuration(sensor_configuration)
    {
        set_extrapolation_mode(extrapolation_mode);
    }

    virtual ~I_NavigationInterpolator() = default;

    // ----- merge data from another interpolator
    /**
     * @brief Merge data from another interpolator. Only works of the SensorConfiguration is
     * compatible.
     *
     * @param other
     */
    void merge(const I_NavigationInterpolator& other)
    {
        
        /* compare sensor operations, without targets */
        if (this->_sensor_configuration.without_targets() != other._sensor_configuration.without_targets())
        {
            throw std::runtime_error(
                fmt::format("ERROR[{}]: Incompatible sensor configurations!", this->get_name()));
        }

        // check if sensor configuration can be merged
        if (!_sensor_configuration.can_merge_targets_with(other.get_sensor_configuration()))
        {
            throw std::runtime_error(
                fmt::format("ERROR[{}]: Incompatible target offsets!", this->get_name()));
        }

        // merge sensor configuration by adding targets
        _sensor_configuration.add_targets(other.get_sensor_configuration().get_targets());

        // merge data
        _interpolator_attitude.insert(other._interpolator_attitude.get_data_X(),
                                      other._interpolator_attitude.get_data_Y());
        _interpolator_heading.insert(other._interpolator_heading.get_data_X(),
                                     other._interpolator_heading.get_data_Y());
        _interpolator_heave.insert(other._interpolator_heave.get_data_X(),
                                   other._interpolator_heave.get_data_Y());
        _interpolator_depth.insert(other._interpolator_depth.get_data_X(),
                                   other._interpolator_depth.get_data_Y());
    }

    // ----- set extrapolation mode -----
    /**
     * @brief Set the extrapolation mode for the attitude, compass, heave and depth interpolators
     *
     * @param extrapolation_mode extrapolate, fail or nearest
     */
    virtual void set_extrapolation_mode(tools::vectorinterpolators::t_extr_mode extrapolation_mode =
                                            tools::vectorinterpolators::t_extr_mode::extrapolate)
    {
        _interpolator_attitude.set_extrapolation_mode(extrapolation_mode);
        _interpolator_heading.set_extrapolation_mode(extrapolation_mode);

        _interpolator_heave.set_extrapolation_mode(extrapolation_mode);
        _interpolator_depth.set_extrapolation_mode(extrapolation_mode);
    }

    //----- operators -----
    bool operator==(const I_NavigationInterpolator& other) const
    {
        return _sensor_configuration == other._sensor_configuration &&
               _interpolator_attitude == other._interpolator_attitude &&
               _interpolator_heading == other._interpolator_heading &&
               _interpolator_heave == other._interpolator_heave &&
               _interpolator_depth == other._interpolator_depth;
    }
    bool operator!=(const I_NavigationInterpolator& other) const { return !(*this == other); }

    //----- set sensor data -----
    /**
     * @brief Set the depth data
     *
     * @param timestamp in seconds since epoch
     * @param depth in meters, positive downwards
     */
    void set_data_depth(const std::vector<double>& timestamp, const std::vector<double>& depth)
    {
        _interpolator_depth.set_data_XY(timestamp, depth);
    }

    /**
     * @brief Set the heave data
     *
     * @param timestamp in seconds since epoch
     * @param heave in meters, positive upwards
     */
    void set_data_heave(const std::vector<double>& timestamp, const std::vector<double>& heave)
    {
        _interpolator_heave.set_data_XY(timestamp, heave);
    }

    /**
     * @brief Set the attitude data (no yaw, ythis is set in set_data_heading)
     *
     * @param timestamp in seconds since epoch
     * @param pitch in °, positive is bow up
     * @param roll in °, positive is port up
     */
    void set_data_attitude(const std::vector<double>& timestamp,
                           const std::vector<double>& pitch,
                           const std::vector<double>& roll)
    {
        std::vector<double> yaw(timestamp.size(), 0.0);
        _interpolator_attitude.set_data_XYPR(timestamp, yaw, pitch, roll);
    }

    /**
     * @brief Set the compass data
     *
     * @param timestamp in seconds since epoch
     * @param heading in °, positive clockwise (north is 0°)
     */
    void set_data_heading(const std::vector<double>& timestamp, const std::vector<double>& heading)
    {
        std::vector<double> pr(heading.size(), 0.0);
        _interpolator_heading.set_data_XYPR(timestamp, heading, pr, pr);
    }

    /**
     * @brief direct reference to the depth data interpolator
     *
     * @return interpolator_depth&
     */
    tools::vectorinterpolators::LinearInterpolator& interpolator_depth()
    {
        return _interpolator_depth;
    }

    /**
     * @brief direct reference to the depth data interpolator
     *
     * @return interpolator_depth&
     */
    tools::vectorinterpolators::AkimaInterpolator& interpolator_heave()
    {
        return _interpolator_heave;
    }

    /**
     * @brief direct reference to the attitude data interpolator
     *
     * @return interpolator_attitude&
     */
    tools::vectorinterpolators::SlerpInterpolator& interpolator_attitude()
    {
        return _interpolator_attitude;
    }

    /**
     * @brief direct reference to the compass data interpolator
     *
     * @return interpolator_heading&
     */
    tools::vectorinterpolators::SlerpInterpolator& interpolator_heading()
    {
        return _interpolator_heading;
    }

    //----- pass through functions -----
    /**
     * @brief add a target sensor with positional offsets
     *
     * @param target_id name of the target sensor
     * @param x x position of the sensor in m, positive forward
     * @param y y position of the sensor in m, positive starboard
     * @param z z position of the sensor in m, positive down
     * @param yaw yaw angle of the sensor in °, positive clockwise
     * @param pitch pitch angle of the sensor in °, positive is bow up
     * @param roll roll angle of the sensor in °, positive is port up
     */
    void add_target(const std::string& target_id,
                    double             x,
                    double             y,
                    double             z,
                    double             yaw,
                    double             pitch,
                    double             roll)
    {
        _sensor_configuration.add_target(target_id, x, y, z, yaw, pitch, roll);
    }

    /**
     * @brief add a target sensor with positional offsets
     *
     * @param target_id name of the target sensor
     * @param sensor_offsets structure that contains the sensor position
     */
    void add_target(const std::string&                       target_id,
                    const datastructures::PositionalOffsets& target_offsets)
    {
        _sensor_configuration.add_target(target_id, target_offsets);
    }

    //------------------------------------- set vessel functions ----------------------------------
    /**
     * @brief direct reference to the sensor configuration
     *
     * @return SensorConfiguration&
     */
    const SensorConfiguration& get_sensor_configuration() const { return _sensor_configuration; }
    void                       set_sensor_configuration(SensorConfiguration sensor_configuration)
    {
        _sensor_configuration = std::move(sensor_configuration);
    }

  public:
    // __printer__ function is necessary to support print() info_string() etc (defined by
    // __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__ macro below)
    tools::classhelper::ObjectPrinter __printer__(unsigned int float_precision) const
    {
        tools::classhelper::ObjectPrinter printer(this->get_name(), float_precision);

        printer.register_section("Sensor offset configuration", '*');
        printer.append(_sensor_configuration.__printer__(float_precision));

        printer.register_section("Attitude data", '*');
        printer.append(_interpolator_attitude.__printer__(float_precision), true);

        printer.register_section("Compass data", '*');
        printer.append(_interpolator_heading.__printer__(float_precision), true);

        printer.register_section("Heave data", '*');
        printer.append(_interpolator_heave.__printer__(float_precision), true);

        printer.register_section("Depth data", '*');
        printer.append(_interpolator_depth.__printer__(float_precision), true);

        return printer;
    }

  protected:
    // serialization support using bitsery
    friend class bitsery::Access;

    I_NavigationInterpolator() = default; // bitsery needs a default constructor

    template<typename S>
    void serialize(S& s)
    {
        // // data
        s.object(_sensor_configuration);
        s.object(_interpolator_attitude);
        s.object(_interpolator_heading);
        s.object(_interpolator_heave);
        s.object(_interpolator_depth);
    }

  public:
    // -- class helper function macros --
    // define to_binary and from_binary functions (needs the serialize function)
    __BITSERY_DEFAULT_TOFROM_BINARY_FUNCTIONS__(I_NavigationInterpolator)
    // define info_string and print functions (needs the __printer__ function)
    __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__
};

} // namespace navigation
} // namespace themachinethatgoesping
