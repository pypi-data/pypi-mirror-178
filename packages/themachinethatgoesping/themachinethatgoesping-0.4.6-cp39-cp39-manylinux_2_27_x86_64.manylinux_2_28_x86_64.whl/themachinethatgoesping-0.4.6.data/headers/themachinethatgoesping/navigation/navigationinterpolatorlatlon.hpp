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
 * @brief The NavInterpolator class: Interpolate navigation (lat/lon) values and attitude
 * information and transform the values using the offsets specified in the sensor configuration
 * class
 */
class NavigationInterpolatorLatLon : public I_NavigationInterpolator
{

    // LinearInterpolator for the depth in the world coordinate system
    tools::vectorinterpolators::AkimaInterpolator
        _interpolator_latitude; ///< interpolator for the latitude data
    tools::vectorinterpolators::AkimaInterpolator
        _interpolator_longitude; ///< interpolator for the longitude data

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

        _interpolator_latitude.set_extrapolation_mode(extrapolation_mode);
        _interpolator_longitude.set_extrapolation_mode(extrapolation_mode);
    }

  public:
    /**
     * @brief Construct a new i navigationinterpolator interface
     *
     * @param extrapolation_mode extrapolate, fail or nearest
     */

    NavigationInterpolatorLatLon(const SensorConfiguration&              sensor_configuration,
                                 tools::vectorinterpolators::t_extr_mode extrapolation_mode =
                                     tools::vectorinterpolators::t_extr_mode::extrapolate)
        : I_NavigationInterpolator(sensor_configuration,
                                   extrapolation_mode,
                                   "NavigationInterpolatorLatLon")
    {
        set_extrapolation_mode(extrapolation_mode);
    }
    virtual ~NavigationInterpolatorLatLon() = default;

    //----- operators -----
    bool operator==(const NavigationInterpolatorLatLon& other) const
    {

        return _interpolator_latitude == other._interpolator_latitude &&
               _interpolator_longitude == other._interpolator_longitude &&
               I_NavigationInterpolator::operator==(other);
    }
    bool operator!=(const NavigationInterpolatorLatLon& other) const { return !(*this == other); }

    //----- set sensor data -----
    /**
     * @brief Set the data of the position system (latitude, longitude)
     *
     * @param timestamp in seconds since epoch
     * @param latitude latitude in °
     * @param longitude longitude in °
     */
    void set_data_position(const std::vector<double>& timestamp,
                           const std::vector<double>& latitude,
                           const std::vector<double>& longitude)
    {
        _interpolator_latitude.set_data_XY(timestamp, latitude);
        _interpolator_longitude.set_data_XY(timestamp, longitude);
    }

    /**
     * @brief direct reference to the latitude interpolator object
     *
     * @return interpolator_latitude&
     */
    tools::vectorinterpolators::AkimaInterpolator& interpolator_latitude()
    {
        return _interpolator_latitude;
    }

    /**
     * @brief direct reference to the longitude interpolator object
     *
     * @return interpolator_longitude&
     */
    tools::vectorinterpolators::AkimaInterpolator& interpolator_longitude()
    {
        return _interpolator_longitude;
    }

    //----- merge interpolators -----
    /**
     * @brief see documentation of I_NavigationInterpolator::merge
     */
    void merge(const NavigationInterpolatorLatLon& other)
    {
        I_NavigationInterpolator::merge(other);

        // merge data
        _interpolator_latitude.insert(other._interpolator_latitude.get_data_X(),
                                      other._interpolator_latitude.get_data_Y());
        _interpolator_longitude.insert(other._interpolator_longitude.get_data_X(),
                                       other._interpolator_longitude.get_data_Y());
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
    datastructures::GeoLocationLatLon operator()(const std::string& target_id, double timestamp)
    {
        return _sensor_configuration.compute_target_position(target_id, get_sensor_data(timestamp));
    }

    /**
     * @brief Compute the position of the target "target_id" based on the sensor data for the given
     * timestamp stamp
     *
     * @param target_id name of the target (e.g. "MBES")
     * @param timestamp timestamp in seconds since epoch
     * @return data structure that contains the position of the target in the world coordinate
     * system
     */
    datastructures::GeoLocationLatLon compute_target_position(const std::string& target_id,
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
    datastructures::SensorDataLatLon get_sensor_data(double timestamp)
    {
        datastructures::SensorDataLatLon sensor_data;
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

        sensor_data.latitude  = _interpolator_latitude(timestamp);
        sensor_data.longitude = _interpolator_longitude(timestamp);

        return sensor_data;
    }

  public:
    // __printer__ function is necessary to support print() info_string() etc (defined by
    // __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__ macro below)
    tools::classhelper::ObjectPrinter __printer__(unsigned int float_precision) const
    {
        tools::classhelper::ObjectPrinter printer(this->get_name(), float_precision);

        printer.append(I_NavigationInterpolator::__printer__(float_precision));

        printer.register_section("Position system latitude", '*');
        printer.append(_interpolator_latitude.__printer__(float_precision), true);

        printer.register_section("Position system longitude", '*');
        printer.append(_interpolator_longitude.__printer__(float_precision), true);

        return printer;
    }

  private:
    // serialization support using bitsery
    friend class bitsery::Access;

    NavigationInterpolatorLatLon() = default; // bitsery needs a default constructor

    template<typename S>
    void serialize(S& s)
    {
        // serialize base class
        s.ext(*this, bitsery::ext::BaseClass<I_NavigationInterpolator>{});

        // data
        s.object(_interpolator_latitude);
        s.object(_interpolator_longitude);
    }

  public:
    // -- class helper function macros --
    // define to_binary and from_binary functions (needs the serialize function)
    __BITSERY_DEFAULT_TOFROM_BINARY_FUNCTIONS__(NavigationInterpolatorLatLon)
    // define info_string and print functions (needs the __printer__ function)
    __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__
};

} // namespace navigation
} // namespace themachinethatgoesping
