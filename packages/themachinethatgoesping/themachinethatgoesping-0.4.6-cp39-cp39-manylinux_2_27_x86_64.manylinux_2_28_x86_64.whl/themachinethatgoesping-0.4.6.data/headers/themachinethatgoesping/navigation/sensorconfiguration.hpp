// SPDX-FileCopyrightText: 2022 Peter Urban, Sven Schorge, GEOMAR Helmholtz Centre for Ocean
// Research Kiel SPDX-FileCopyrightText: 2022 Peter Urban, Ghent University
//
// SPDX-License-Identifier: MPL-2.0

#pragma once
#include <cmath>
#include <exception>
#include <iostream>
#include <math.h>
#include <string>

#include <bitsery/ext/std_map.h>

#include <GeographicLib/Geocentric.hpp>
#include <GeographicLib/Geodesic.hpp>
#include <GeographicLib/LocalCartesian.hpp>

#include <themachinethatgoesping/tools/classhelper/bitsery.hpp>
#include <themachinethatgoesping/tools/classhelper/objectprinter.hpp>
#include <themachinethatgoesping/tools/rotationfunctions/quaternions.hpp>
#include <themachinethatgoesping/tools/vectorinterpolators.hpp>

#include "datastructures.hpp"

namespace themachinethatgoesping {
namespace navigation {

/**
 * @brief A coordinate system that allows for specifying sensor offsets (e.g. gps antenna and
 * attitude sensor) and target offsets (e.g. MBES). Call the class and specify target_id and current
 * sensor data to derive the geolocation and attitude of the specified targets
 *
 */
class SensorConfiguration
{
    std::unordered_map<std::string, datastructures::PositionalOffsets>
        _target_offsets; ///< TargetId (position in vector) for each registered target_id

    datastructures::PositionalOffsets
        _offsets_attitude_source; ///< Static Roll,Pitch,Yaw (installation) offsets of the attitude
                                  ///< sensor
    datastructures::PositionalOffsets
        _offsets_heading_source; ///< Static Yaw (installation) Offsets of CompassOffsets
    datastructures::PositionalOffsets
        _offsets_position_source; ///< Static x,y,z (installation) Offsets of the PositionSystem
    datastructures::PositionalOffsets
        _offsets_depth_source; ///< Static xy,z (installation) Offsets of the depth sensor
                               // Static Position of Heave Sensor
                               // Offsets _HeaveSensorOffsets;

  public:
    /**
     * @brief Construct a new, empty Sensor Coordinate System object
     * After construction: add sensor offsets and targets (offsets)
     * Then compute target positions for sensor data
     *
     */
    SensorConfiguration(std::string_view default_sensor_name = "zero-referenced")
    {
        _offsets_attitude_source.name = default_sensor_name;
        _offsets_heading_source.name  = default_sensor_name;
        _offsets_position_source.name = default_sensor_name;
        _offsets_depth_source.name    = default_sensor_name;
    }

    /**
     * @brief Return the SensorConfiguration object without registered targets
     *
     * @return SensorConfiguration
     */
    SensorConfiguration without_targets() const
    {
        SensorConfiguration result(*this);
        result.remove_targets();
        return result;
    }

    /**
     * @brief Check if the given SensorConfiguration includes a target (offsets) that is
     * incompatible with the given SensorConfiguration targets
     *
     * @return false if the same target_id is registered with different offsets, true otherwise
     */
    bool can_merge_targets_with(const SensorConfiguration& other) const
    {
        /* check for incompatible targets */
        for (const auto& [target_id, offsets] : _target_offsets)
        {
            if (other._target_offsets.find(target_id) != other._target_offsets.end())
            {
                if (offsets != other._target_offsets.at(target_id))
                    return false;
            }
        }

        return true;
    }

    // ----- compute_target_position -----
    /**
     * @brief Compute the position of the target "target_id" based on the sensor data "sensor_data"
     *
     * @param target_id name of the target (e.g. "MBES")
     * @param sensor_data SensorDataLatLon / this structure includes latitude and longitude
     * information
     * @return datastructures::GeoLocationLatLon  / this structure includes latitude and longitude
     * information
     */
    datastructures::GeoLocationLatLon compute_target_position(
        const std::string&                      target_id,
        const datastructures::SensorDataLatLon& sensor_data) const;

    /**
     * @brief Compute the position of the target "target_id" based on the sensor data "sensor_data"
     *
     * @param target_id name of the target (e.g. "MBES")
     * @param sensor_data SensorDataUTM / this structure includes northing/easting and utm zone or
     * hemisphere information
     * @return datastructures::GeoLocationUTM  / this structure includes northing/easting and utm
     * zone or hemisphere information
     */
    datastructures::GeoLocationUTM compute_target_position(
        const std::string&                   target_id,
        const datastructures::SensorDataUTM& sensor_data) const;

    /**
     * @brief Compute the position of the target "target_id" based on the sensor data "sensor_data"
     *
     * @param target_id name of the target (e.g. "MBES")
     * @param sensor_data SensorDataLocal / this structure includes northing/easting but no zone or
     * hemisphere information
     * @return datastructures::GeoLocationLocal  / this structure includes northing/easting but no
     * zone or hemisphere information
     */
    datastructures::GeoLocationLocal compute_target_position(
        const std::string&                     target_id,
        const datastructures::SensorDataLocal& sensor_data) const;

    /**
     * @brief Compute the position of the target "target_id" based on the sensor data "sensor_data"
     *
     * @param target_id name of the target (e.g. "MBES")
     * @param sensor_data SensorData / this structure includes no coordinate information
     * @return datastructures::GeoLocationLocal  / this structure includes northing and east, which
     * are set relative to the sensor coordinate system center
     */
    datastructures::GeoLocationLocal compute_target_position(
        const std::string&                target_id,
        const datastructures::SensorData& sensor_data) const;

    // ----- get/set target offsets -----
    /**
     * @brief add a target (e.g. MBES) with offsets to the sensor position system
     *
     * @param target_id name of the target for reference
     * @param x x-offset of the target (in meters, positive forward)
     * @param y y-offset of the target (in meters, positive starboard)
     * @param z z-offset of the target (in meters, positive down)
     * @param yaw yaw offset of the target (right-handed around the z-axis) (in degrees, 90° = east)
     * @param pitch pitch offset of the target (right-handed around the y-axis) (in degrees,
     * positive = bow up)
     * @param roll roll offset of the target (right-handed around the x-axis) (in degrees, positive
     * = port up)
     */
    void add_target(const std::string& target_id,
                    double             x,
                    double             y,
                    double             z,
                    double             yaw,
                    double             pitch,
                    double             roll);

    /**
     * @brief add a target (e.g. MBES) with offsets to the sensor position system
     *
     * @param target_id name of the target for reference
     * @param target_offsets mounting offsets of the target
     */
    void add_target(const std::string&                       target_id,
                    const datastructures::PositionalOffsets& target_offsets);

    /**
     * @brief add targets (e.g. MBES) with given target_ids and offsets to the sensor position
     * system
     *
     * @param targets map<target_id, target_offsets> of target offsets
     */
    void add_targets(
        const std::unordered_map<std::string, datastructures::PositionalOffsets>& targets);

    /**
     * @brief Get stored target offsets of a specified target
     *
     * @param target_id name of the registered target
     * @return const datastructures::PositionalOffsets& offsets of the target
     */
    const datastructures::PositionalOffsets& get_target(const std::string& target_id) const;

    /**
     * @brief Get the map of stored target offsets objects
     *
     * @return const std::unordered_map<std::string, datastructures::PositionalOffsets>&
     */
    const std::unordered_map<std::string, datastructures::PositionalOffsets>& get_targets() const;

    /**
     * @brief Remove the target with the specified target_id
     *
     * @param target_id name of the registered target
     */
    void remove_target(const std::string& target_id);

    /**
     * @brief Remove all stored targets
     *
     */
    void remove_targets();

    // ----- get/set sensor offsets -----
    /**
     * @brief Set the attitude sensor offsets
     *
     * @param sensor_offsets offsets structure (only yaw, pitch and roll are used)
     */
    void set_attitude_source(const datastructures::PositionalOffsets& sensor_offsets);

    /**
     * @brief Set the attitude sensor offsets
     *
     * @param yaw yaw offset of the attitude sensor (right-handed around the z-axis) (in degrees,
     * 90° = east)
     * @param pitch pitch offset of the attitude sensor (right-handed around the y-axis) (in
     * degrees, positive = bow up)
     * @param roll roll offset of the attitude sensor (right-handed around the x-axis) (in degrees,
     * positive = port up)
     */
    void set_attitude_source(std::string_view name, double yaw, double pitch, double roll);

    /**
     * @brief Get the attitude sensor offsets
     *
     * @return const datastructures::PositionalOffsets& offsets of the attitude sensor
     */
    datastructures::PositionalOffsets get_attitude_source() const;

    /**
     * @brief Set the compass offsets
     *
     * @param yaw yaw offset of the compass (right-handed around the z-axis) (in degrees, 90° =
     * east)
     */
    void set_heading_source(std::string_view name, double yaw);

    /**
     * @brief Set the compass offsets
     *
     * @param sensor_offsets offsets structure (only yaw is used)
     */
    void set_heading_source(const datastructures::PositionalOffsets& sensor_offsets);

    /**
     * @brief Get the registered compass offsets
     *
     * @return const datastructures::PositionalOffsets& offsets of the compass
     */
    datastructures::PositionalOffsets get_heading_source() const;

    /**
     * @brief Set the depth sensor offsets
     *
     * @param x x-offset of the depth sensor (in meters, positive forward)
     * @param y y-offset of the depth sensor (in meters, positive starboard)
     * @param z z-offset of the depth sensor (in meters, positive down)
     */
    void set_depth_source(std::string_view name, double x, double y, double z);

    /**
     * @brief Set the depth sensor offsets
     *
     * @param sensor_offsets offsets structure (only x, y and z are used)
     */
    void set_depth_source(const datastructures::PositionalOffsets& sensor_offsets);

    /**
     * @brief Get the registered depth sensor offsets
     *
     * @return const datastructures::PositionalOffsets& offsets of the depth sensor
     */
    datastructures::PositionalOffsets get_depth_source() const;

    /**
     * @brief Set the position system offsets
     *
     * @param x x-offset of the depth sensor (in meters, positive forward)
     * @param y y-offset of the depth sensor (in meters, positive starboard)
     * @param z z-offset of the depth sensor (in meters, positive down)
     */
    void set_position_source(std::string_view name, double x, double y, double z);

    /**
     * @brief Set the position system offsets
     *
     * @param sensor_offsets offsets structure (only x, y and z are used)
     */
    void set_position_source(const datastructures::PositionalOffsets& sensor_offsets);

    /**
     * @brief Get the registered position system offsets
     *
     * @return const datastructures::PositionalOffsets& offsets of the position system
     */
    datastructures::PositionalOffsets get_position_source() const;

    /**
     * @brief Get the ids of the registered targets
     *
     * @return std::vector<std::string_view>
     */
    std::vector<std::string_view> get_target_ids() const
    {
        std::vector<std::string_view> target_ids;
        for (const auto& target : _target_offsets)
        {
            target_ids.push_back(target.first);
        }
        return target_ids;
    }

  private:
    // ----- helper functions -----
    /**
     * @brief Compute the rotation of the sensor coordinate system (relative to the world reference
     * coordinate system) using the sensor data and (rotation) offsets. Note: if
     * heading is used the attitude_source_offset yaw will be used to correct the
     * attitude_source_offset roll and pitch but will not be added to the heading
     *
     * @param sensor_data Sensor data object (used are: heading, pitch,
     * roll)
     * @param offsets_heading_source Offsets of the compass (used is only yaw offset)
     * @param offsets_attitude_source Offsets of the IMU (used are yaw, pitch and roll), if
     * heading is used, yaw is used to correct pitch, and roll but not added to the heading
     * @return Eigen::Quaterniond Rotation of the sensor system compared to the world reference
     * system
     */
    static Eigen::Quaterniond get_system_rotation_as_quat(
        const datastructures::SensorData&        sensor_data,
        const datastructures::PositionalOffsets& offsets_heading_source,
        const datastructures::PositionalOffsets& offsets_attitude_source);

    // serialization support using bitsery
    friend bitsery::Access;
    template<typename S>
    void serialize(S& s)
    {
        // serialize map of PositionOffsets
        s.ext(_target_offsets,
              bitsery::ext::StdMap{ 100 },
              [](S& s, std::string& key, datastructures::PositionalOffsets& value) {
                  s.container1b(key, 100);
                  s.object(value);
              });
        s.object(_offsets_attitude_source);
        s.object(_offsets_heading_source);
        s.object(_offsets_position_source);
        s.object(_offsets_depth_source);
    }

  public:
    /**
     * @brief Compare two SensorConfiguration objects for equality
     *
     * @param other SensorConfiguration object to compare to
     * @return true
     * @return false
     */
    bool operator==(const SensorConfiguration& other) const
    {
        if (_target_offsets.size() != other._target_offsets.size())
        {
            return false;
        }

        for (const auto& [target_id, target_offsets] : _target_offsets)
        {
            if (other._target_offsets.find(target_id) == other._target_offsets.end())
            {
                return false;
            }
            if (target_offsets != other._target_offsets.at(target_id))
            {
                return false;
            }
        }

        return _offsets_attitude_source == other._offsets_attitude_source &&
               _offsets_heading_source == other._offsets_heading_source &&
               _offsets_position_source == other._offsets_position_source &&
               _offsets_depth_source == other._offsets_depth_source;
    }
    /**
     * @brief Compare two SensorConfiguration objects for inequality
     *
     * @param other SensorConfiguration object to compare to
     * @return true
     * @return false
     */
    bool operator!=(const SensorConfiguration& other) const { return !(*this == other); }

    // __printer__ function is necessary to support print() info_string() etc (defined by
    // __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__ macro below)
    tools::classhelper::ObjectPrinter __printer__(unsigned int float_precision) const
    {
        tools::classhelper::ObjectPrinter printer("SensorConfiguration", float_precision);

        for (const auto& [target_id, target_offsets] : _target_offsets)
        {
            printer.register_section("Target offsets \"" + target_id + "\"");
            printer.append(target_offsets.__printer__(float_precision));
        }

        printer.register_section("Attitude sensor offsets");
        printer.append(_offsets_attitude_source.__printer__(float_precision));

        printer.register_section("Compass offsets");
        printer.append(_offsets_heading_source.__printer__(float_precision));

        printer.register_section("Position system offsets");
        printer.append(_offsets_position_source.__printer__(float_precision));

        printer.register_section("Depth sensor offsets");
        printer.append(_offsets_depth_source.__printer__(float_precision));

        return printer;
    }

  public:
    // -- class helper function macros --
    // define to_binary and from_binary functions (needs the serialize function)
    __BITSERY_DEFAULT_TOFROM_BINARY_FUNCTIONS__(SensorConfiguration)
    // define info_string and print functions (needs the __printer__ function)
    __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__
};

} // namespace navigation
} // namespace themachinethatgoesping

template<>
struct std::hash<themachinethatgoesping::navigation::SensorConfiguration>
{
    std::size_t operator()(
        const themachinethatgoesping::navigation::SensorConfiguration& object) const
    {
        return object.slow_hash();
    }
};
