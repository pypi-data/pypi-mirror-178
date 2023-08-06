// SPDX-FileCopyrightText: 2022 Peter Urban, GEOMAR Helmholtz Centre for Ocean Research Kiel
// SPDX-FileCopyrightText: 2022 Tim Weiß, GEOMAR Helmholtz Centre for Ocean Research Kiel
// SPDX-FileCopyrightText: 2022 Peter Urban, Ghent University
//
// SPDX-License-Identifier: MPL-2.0

/**
 * @brief Converting chrono time points / unix timestamps (double) and date time
 * strings to each other. unix timestamps are always treated as UTC
 * @authors Peter Urban
 *
 */

#pragma once

/* std includes */
#include <chrono>
#include <cmath>
#include <string>

namespace themachinethatgoesping {

namespace tools {

namespace timeconv {

//------------------------------------- time conversions
//------------------------------------------
/**
 * @brief unixtime_to_timepoint
 *        IMPORTANT: return value will only have microseconds precision!
 * @param unixtime: Unix time stamp (seconds since 01.01.1970) as double
 * @return chrono::system_clock::time_point
 */
std::chrono::system_clock::time_point unixtime_to_timepoint(double unixtime);

/**
 * @brief timepoint_to_unixtime
 *        IMPORTANT: Conversion does only have microseconds precision!
 * @param TimePoint: chrono::system_clock::time_point
 * @return Unix time stamp (seconds since 01.01.1970) as double
 */
double timepoint_to_unixtime(std::chrono::system_clock::time_point TimePoint);

//------------------------------------- time conversions
//------------------------------------------
/**
 * @brief Converting between date strings and unixtime stamps (ref 1970)
 *
 * @param  DateString: DateString to be converted. Must fit format string.
 * @param  format: Format string to convert Date string.
 *      Default Format: "%z__%d-%m-%Y__%H:%M:%S"
 *      see https://m.cplusplus.com/reference/ctime/strftime/ *
        https://themachinethatgoesping.readthedocs.io/en/latest/modules/tools/timeconv.html#format-string
 * @return unixtime as double (seconds since 01.01.1970)
 */
double datestring_to_unixtime(const std::string& DateString,
                              const std::string& format = "%z__%d-%m-%Y__%H:%M:%S");

/**
 * @brief Converting between date strings and unixtime stamps (ref 1970)
 *
 * @param unixtime: seconds since 01.01.1970 as double
 * @param fractionalSecondsDigits: How many digits to use for the split seconds.
 *          Minimum is 0 (second resolution)
 *          Maximum is 6 (microsecond resolution)
 * @param format: Format string to convert Date string.
 *      Default Format: "%z__%d-%m-%Y__%H:%M:%S"
 *      see: https://m.cplusplus.com/reference/ctime/strftime/ *
        https://themachinethatgoesping.readthedocs.io/en/latest/modules/tools/timeconv.html#format-string
 * @return DateString that fits to the specified format
 */
std::string unixtime_to_datestring(double             unixtime,
                                   unsigned int       fractionalSecondsDigits = 0,
                                   const std::string& format = "%z__%d-%m-%Y__%H:%M:%S");

/**
 * @brief Convert a windows 32bit Filetime to a unix timestamp
 * conversion to unixtime see: http://www.frenk.com/2009/12/convert-filetime-to-unix-timestamp/
 *
 * WARNING: converting to unixtime and then back causes small (100 ns ) rounding error *
 * @param highDateTime
 * @param lowDateTime
 * @return double
 */
inline double windows_filetime_to_unixtime(uint32_t highDateTime, uint32_t lowDateTime)
{
    uint64_t              date = (((int64_t)highDateTime) << 32) + lowDateTime;
    static const uint64_t adjust =
        11644473600000 * 10000; ///< 100-nanoseconds = milliseconds * 10000

    // removes the diff between 1970 and 1601 and convert nanoseconds to seconds
    double unixtime = ((double)(date - adjust)) / 10000000.;

    return unixtime;
}

/**
 * @brief Convert a unix timestamp to a windows 32bit Filetime
 * conversion to 2 x 32 bit word see:
 * https://support.microsoft.com/en-us/help/188768/info-working-with-the-filetime-structure
 *
 * @param unixtime in seconds since 1970
 * @return std::pair<uint32_t, uint32_t>
 */
inline std::pair<uint32_t, uint32_t> unixtime_to_windows_filetime(double unixtime)
{
    /* just reverting the function above */
    static const int64_t adjust = int64_t(11644473600000. * 10000.);

    unixtime *= 10000000.;

    uint64_t date = (uint64_t)std::llround(unixtime) + adjust;

    uint32_t lowDateTime  = (uint32_t)(date & 0xFFFFFFFF);
    uint32_t highDateTime = (uint32_t)(date >> 32);

    return std::make_pair(highDateTime, lowDateTime);
}

} // namespace timeconv

} // namespace tools

} // namespace themachinethatgoesping
