// Kiel SPDX-FileCopyrightText: 2022 Peter Urban, Ghent University
//
// SPDX-License-Identifier: MPL-2.0

#pragma once

/**
 * @brief Some navigation helper functions that allow converting different lat/lon formats (decimal,
 * minute / decimal degrees etc) and utm coordinates to lat/lon decimal degrees and back
 *
 */

#include <stdexcept>
#include <tuple>
#include <vector>

#include <GeographicLib/UTMUPS.hpp>
#include <fmt/core.h>

namespace themachinethatgoesping {
namespace navigation {
namespace navtools {

/**
 * @brief lat/lon format specifications
 *
 */
enum class t_latlon_format
{
    degrees = 0, ///< lat/lon will be converted to degrees.degrees°N/S E/W
    minutes = 1, ///< lat/lon will be converted to degrees°minutes.minutes'E/S E/W
    seconds = 2  ///< lat/lon will be converted to degrees°minutes'seconds.seconds''E/S E/W
};

inline std::string dms_to_string(double          dms_value,
                                 t_latlon_format format,
                                 size_t          precision,
                                 char            sign)
{
    dms_value = std::abs(dms_value);

    switch (format)
    {
        case t_latlon_format::degrees:
            return fmt::format("{:.{}f}°{}", dms_value, precision, sign);
        case t_latlon_format::minutes: {
            int    degrees = int(dms_value);
            double minutes = (dms_value - double(degrees)) * 60;
            return fmt::format("{}°{:.{}f}'{}", degrees, minutes, precision, sign);
        }
        case t_latlon_format::seconds: {
            int    degrees = int(dms_value);
            double minutes = (dms_value - double(degrees)) * 60;
            double seconds = (minutes - double(int(minutes))) * 60;
            return fmt::format(
                "{}°{}'{:.{}f}\"{}", degrees, int(minutes), seconds, precision, sign);
        }
        default:
            throw std::runtime_error("ERROR[latitude/longitude_to_string]: Unknown ENUM type!");
    }
}

/**
 * @brief convert a latitude value to a string
 *
 * @param latitude value to be converted
 * @param precision number of digits behind the .
 * @param format latlon format (degrees°N/S, degrees°minutes'N/S or degrees°minutes'seconds''N/S)
 * @return converted latitude string
 */
inline std::string latitude_to_string(double          latitude,
                                      t_latlon_format format    = t_latlon_format::minutes,
                                      size_t          precision = 6)
{
    char sign = 'N';
    if (latitude < 0)
        sign = 'S';

    return dms_to_string(latitude, format, precision, sign);
}

/**
 * @brief convert a latitude value to a string
 *
 * @param latitude value to be converted
 * @param precision number of digits behind the .
 * @param format latlon format (degrees°N/S, degrees°minutes'N/S or degrees°minutes'seconds''N/S)
 * @return converted latitude string
 */
inline std::string longitude_to_string(double          longitude,
                                       t_latlon_format format    = t_latlon_format::minutes,
                                       size_t          precision = 6)
{
    char sign = 'E';
    if (longitude < 0)
        sign = 'W';

    return dms_to_string(longitude, format, precision, sign);
}

/**
 * @brief Convert utm coordinates to latitude longitude using Geographic lib
 *
 * @param northing northing in meters
 * @param easting easting in meters
 * @param zone utm zone number (1-60)
 * @param northern_hemisphere if true, northern hemisphere, else southern hemisphere
 * @return (list of latitude, list of longitudes)
 */
inline std::pair<std::vector<double>, std::vector<double>> utm_to_latlon(
    const std::vector<double>& northing,
    const std::vector<double>& easting,
    int                        zone,
    bool                       northern_hemisphere)
{
    // check if vector sizes are the same
    if (easting.size() != northing.size())
        throw std::runtime_error(
            "ERROR[utm_to_latlon]: easting and northing vector sizes are not the same!");

    // initialize output vectors
    std::vector<double> lat, lon;
    lat.resize(northing.size());
    lon.resize(northing.size());

    // loop through data and convert using GeographicLib
    for (size_t i = 0; i < easting.size(); i++)
    {
        GeographicLib::UTMUPS::Reverse(
            zone, northern_hemisphere, easting[i], northing[i], lat[i], lon[i]);
    }

    return std::make_pair(lat, lon);
}

/**
 * @brief Convert utm coordinates to latitude longitude using Geographic lib
 *
 * @param northing northing in meters
 * @param easting easting in meters
 * @param zone utm zone number (1-60)
 * @param northern_hemisphere if true, northern hemisphere, else southern hemisphere
 * @return (list of latitude, list of longitudes)
 */
inline std::pair<std::vector<double>, std::vector<double>> utm_to_latlon(
    const std::vector<double>& northing,
    const std::vector<double>& easting,
    const std::vector<int>&    zone,
    const std::vector<bool>&   northern_hemisphere)
{
    // check if vector sizes are the same
    if (easting.size() != northing.size() && easting.size() != zone.size() &&
        easting.size() != northern_hemisphere.size())
        throw std::runtime_error("ERROR[utm_to_latlon]: easting, northing, zone and "
                                 "northern_hemisphere vector sizes are not the same!");

    // initialize output vectors
    std::vector<double> lat, lon;
    lat.resize(northing.size());
    lon.resize(northing.size());

    // loop through data and convert using GeographicLib
    for (size_t i = 0; i < easting.size(); i++)
    {
        GeographicLib::UTMUPS::Reverse(
            zone[i], northern_hemisphere[i], easting[i], northing[i], lat[i], lon[i]);
    }

    return std::make_pair(lat, lon);
}

/**
 * @brief Convert latitudes and longitudes to utm coordinates using GeographicLib
 *
 * @param lat list of latitudes
 * @param lon list of longitudes
 * @param setzone utm output zone number (1-60), default (-1) determines zone using mean latitude
 * and longitude
 * @return std::tuple<std::vector<double>, std::vector<double>, int, bool>
 */
inline std::tuple<std::vector<double>, std::vector<double>, int, bool>
latlon_to_utm(const std::vector<double>& lat, const std::vector<double>& lon, int setzone = -1)
{
    // check if vector sizes are the same
    if (lat.size() != lon.size())
        throw std::runtime_error(
            "ERROR[latlon_to_utm]: lat and lon vector sizes are not the same!");

    // determine setzone using mean of latitudes and longitudes
    if (setzone == -1)
    {
        double mean_lat = 0;
        double mean_lon = 0;
        for (size_t i = 0; i < lat.size(); i++)
        {
            mean_lat += lat[i];
            mean_lon += lon[i];
        }
        mean_lat /= double(lat.size());
        mean_lon /= double(lat.size());
        setzone = GeographicLib::UTMUPS::StandardZone(mean_lat, mean_lon);
    }

    // initialize output data
    std::vector<double> northing, easting;
    northing.resize(lat.size());
    easting.resize(lat.size());
    int  zone;
    bool northern_hemisphere;

    // loop through data and convert using GeographicLib
    for (size_t i = 0; i < lat.size(); i++)
    {
        GeographicLib::UTMUPS::Forward(
            lat[i], lon[i], zone, northern_hemisphere, easting[i], northing[i], setzone);
    }
    return std::make_tuple(northing, easting, zone, northern_hemisphere);
}

}
}
}