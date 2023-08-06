// SPDX-FileCopyrightText: 2022 Peter Urban, Sven Schorge, GEOMAR Helmholtz Centre for Ocean
// Research Kiel SPDX-FileCopyrightText: 2022 Peter Urban, Ghent University
//
// SPDX-License-Identifier: MPL-2.0

#pragma once

#include <bitsery/ext/inheritance.h>

#include <themachinethatgoesping/tools/classhelper/bitsery.hpp>
#include <themachinethatgoesping/tools/classhelper/objectprinter.hpp>
#include <themachinethatgoesping/tools/vectorinterpolators.hpp>

#include "datastructures.hpp"
#include "i_navigationinterpolator.hpp"
#include "sensorconfiguration.hpp"

namespace themachinethatgoesping {
namespace navigation {

/**
 * @brief The NavInterpolator class: Interpolate navigation (northing/easting no zone specified)
 * values and attitude information and transform the values using the offsets specified in the
 * sensor configuration class
 */
class NavigationInterpolatorLocal : public I_NavigationInterpolator
{

    // LinearInterpolator for the depth in the world coordinate system
    tools::vectorinterpolators::AkimaInterpolator
        _interpolator_northing; ///< interpolator for the northing data
    tools::vectorinterpolators::AkimaInterpolator
        _interpolator_easting; ///< interpolator for the easting data

  public:
    /**
     * @brief Set the extrapolation mode for all interpolators
     *
     * @param extrapolation_mode extrapolate, fail or nearest
     */
    void set_extrapolation_mode(tools::vectorinterpolators::t_extr_mode extrapolation_mode =
                                    tools::vectorinterpolators::t_extr_mode::extrapolate)
    {
        I_NavigationInterpolator::set_extrapolation_mode(extrapolation_mode);

        _interpolator_northing.set_extrapolation_mode(extrapolation_mode);
        _interpolator_easting.set_extrapolation_mode(extrapolation_mode);
    }

  public:
    /**
     * @brief Construct a new i navigationinterpolator interface
     *
     * @param extrapolation_mode extrapolate, fail or nearest
     */
    NavigationInterpolatorLocal(const SensorConfiguration&              sensor_configuration,
                                tools::vectorinterpolators::t_extr_mode extrapolation_mode =
                                    tools::vectorinterpolators::t_extr_mode::extrapolate)
        : I_NavigationInterpolator(sensor_configuration,
                                   extrapolation_mode,
                                   "NavigationInterpolatorLocal")
    {
        set_extrapolation_mode(extrapolation_mode);
    }
    virtual ~NavigationInterpolatorLocal() = default;

    //----- operators -----
    bool operator==(const NavigationInterpolatorLocal& other) const
    {

        return _interpolator_northing == other._interpolator_northing &&
               _interpolator_easting == other._interpolator_easting &&
               I_NavigationInterpolator::operator==(other);
    }
    bool operator!=(const NavigationInterpolatorLocal& other) const { return !(*this == other); }

    //----- set sensor data -----
    /**
     * @brief Set the data of the position system (northing, easting)
     *
     * @param timestamp in seconds since epoch
     * @param northing northing in meters
     * @param easting easting in meters
     */
    void set_data_position(const std::vector<double>& timestamp,
                           const std::vector<double>& northing,
                           const std::vector<double>& easting)
    {
        _interpolator_northing.set_data_XY(timestamp, northing);
        _interpolator_easting.set_data_XY(timestamp, easting);
    }

    /**
     * @briefSet the data of the position system (northing, easting) and the offsets of the
     * position system
     *
     * @param timestamp in seconds since epoch
     * @param northing in meters
     * @param easting in meters
     * @param name of the position system
     * @param offset_x in m, positive forward
     * @param offset_y in m, positive starboard
     * @param offset_z in m, positive down
     */
    void set_data_position(const std::vector<double>& timestamp,
                           const std::vector<double>& northing,
                           const std::vector<double>& easting,
                           std::string_view           name,
                           double                     offset_x,
                           double                     offset_y,
                           double                     offset_z)
    {
        _sensor_configuration.set_position_source(name, offset_x, offset_y, offset_z);
        set_data_position(timestamp, northing, easting);
    }

    /**
     * @briefSet the data of the position system (northing, easting) and the offsets of the
     * position system
     *
     * @param timestamp in seconds since epoch
     * @param northing in meters
     * @param easting in meters
     * @param sensor_offsets structure containing the offsets of the position system
     */
    void set_data_position(const std::vector<double>&               timestamp,
                           const std::vector<double>&               northing,
                           const std::vector<double>&               easting,
                           const datastructures::PositionalOffsets& sensor_offsets)
    {
        _sensor_configuration.set_position_source(sensor_offsets);
        set_data_position(timestamp, northing, easting);
    }

    /**
     * @brief direct reference to the northing interpolator object
     *
     * @return interpolator_northing&
     */
    tools::vectorinterpolators::AkimaInterpolator& interpolator_northing()
    {
        return _interpolator_northing;
    }

    /**
     * @brief direct reference to the easting interpolator object
     *
     * @return interpolator_easting&
     */
    tools::vectorinterpolators::AkimaInterpolator& interpolator_easting()
    {
        return _interpolator_easting;
    }
    //----- merge interpolators -----
    /**
     * @brief see documentation of I_NavigationInterpolator::merge
     */
    void merge(const NavigationInterpolatorLocal& other)
    {
        I_NavigationInterpolator::merge(other);

        // merge data
        _interpolator_northing.insert(other._interpolator_northing.get_data_X(),
                                      other._interpolator_northing.get_data_Y());
        _interpolator_easting.insert(other._interpolator_easting.get_data_X(),
                                     other._interpolator_easting.get_data_Y());
    }

    //----- compute the position of the target sensors -----
    /**
     * @brief Compute the position of the target "target_id" based on the sensor data for the given
     * timestamp stamp
     *
     * @param target_id name of the target (e.g. "MBES")
     * @param timestamp timestamp in seconds since epoch
     * @return data structure that contains the position of the target in the world coordinate
     * system
     */
    datastructures::GeoLocationLocal compute_target_position(const std::string& target_id,
                                                             double             timestamp)
    {
        return _sensor_configuration.compute_target_position(target_id, get_sensor_data(timestamp));
    }

    //----- compute the position of the target sensors -----
    /**
     * @brief Interpolate the saved sensor data for a specified timestamp stamp
     *
     * @param timestamp timestamp in seconds since epoch
     * @return data structure that contains the sensor data interpolated for the given timestamp
     * stamp
     */
    datastructures::SensorDataLocal get_sensor_data(double timestamp)
    {
        datastructures::SensorDataLocal sensor_data;
        if (!_interpolator_depth.empty()) // default is 0.0
            sensor_data.depth = _interpolator_depth(timestamp);

        if (!_interpolator_heave.empty()) // default is 0.0
            sensor_data.heave = _interpolator_heave(timestamp);

        if (!_interpolator_heading.empty()) // default is 0.0
            sensor_data.heading = _interpolator_heading.ypr(timestamp)[0];

        if (!_interpolator_attitude.empty()) // default is 0.0. 0.0
        {
            auto ypr = _interpolator_attitude.ypr(timestamp);
            // sensor_data.imu_yaw   = ypr[0];
            sensor_data.pitch = ypr[1];
            sensor_data.roll  = ypr[2];
        }

        sensor_data.northing = _interpolator_northing(timestamp);
        sensor_data.easting  = _interpolator_easting(timestamp);

        return sensor_data;
    }

  public:
    // __printer__ function is necessary to support print() info_string() etc (defined by
    // __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__ macro below)
    tools::classhelper::ObjectPrinter __printer__(unsigned int float_precision) const
    {
        tools::classhelper::ObjectPrinter printer(this->get_name(), float_precision);

        printer.append(I_NavigationInterpolator::__printer__(float_precision));

        printer.register_section("Position system northing", '*');
        printer.append(_interpolator_northing.__printer__(float_precision), true);

        printer.register_section("Position system easting", '*');
        printer.append(_interpolator_easting.__printer__(float_precision), true);

        return printer;
    }

  private:
    // serialization support using bitsery
    friend class bitsery::Access;

    NavigationInterpolatorLocal() = default; // bitsery needs a default constructor

    template<typename S>
    void serialize(S& s)
    {
        // data
        s.object(_interpolator_northing);
        s.object(_interpolator_easting);

        // serialize base class
        s.ext(*this, bitsery::ext::BaseClass<I_NavigationInterpolator>{});
    }

  public:
    // -- class helper function macros --
    // define to_binary and from_binary functions (needs the serialize function)
    __BITSERY_DEFAULT_TOFROM_BINARY_FUNCTIONS__(NavigationInterpolatorLocal)
    // define info_string and print functions (needs the __printer__ function)
    __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__
};

} // namespace navigation
} // namespace themachinethatgoesping
