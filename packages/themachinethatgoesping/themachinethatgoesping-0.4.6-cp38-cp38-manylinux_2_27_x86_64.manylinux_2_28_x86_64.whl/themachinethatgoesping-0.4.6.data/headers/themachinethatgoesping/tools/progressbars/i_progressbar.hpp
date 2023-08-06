// SPDX-FileCopyrightText: 2022 Peter Urban, GEOMAR Helmholtz Centre for Ocean Research Kiel
// SPDX-FileCopyrightText: 2022 Peter Urban, Ghent University
//
// SPDX-License-Identifier: MPL-2.0

#pragma once
#include <string>

namespace themachinethatgoesping {
namespace tools {
namespace progressbars {

/**
 * @brief This is a generic (abstract) class for progress bars.
 * Usage: call init() and close() to initialize and finalize the progress bar.
 * Then call set_progress() or tick() to update the progress bar.
 * set_postfix() can be used to set a postfix message.
 *
 * Note: Functions the set_progress and tick functions can significantly slow down processes that
 * use the progressbar. Consider using the ProgressBarTimed interface instead.
 */
class I_ProgressBar
{
  public:
    /**
     * @brief Construct a new i progressbar object
     *
     */
    I_ProgressBar()          = default;
    virtual ~I_ProgressBar() = default;

    virtual bool is_initialized() const = 0;

    /**
     * @brief Initialize a new progressbar within the given range
     *
     * @param first lowest number in the range (typically 0.0)
     * @param last highest number in the range (typically 100.0)
     * @param process_name Name of the progress
     */
    virtual void init(double first, double last, const std::string& process_name = "process") = 0;

    /**
     * @brief Finalize the progressbar
     *
     * @param msg A message that can be appended as postfix
     */
    virtual void close(const std::string& msg = "done") = 0;

    /**
     * @brief Increment the progress state by the given amount
     *
     * @param increment Number of steps to increment the progress by
     */
    virtual void tick(double increment = 1) = 0;

    /**
     * @brief Set the progress state to the given value.
     * Note some implementations may require the new_progress to be higher than the current
     * progress!
     *
     * @param new_progress New progress state (within the given first/last range)
     */
    virtual void set_progress(double new_progress) = 0;

    /**
     * @brief Append a postfix message to the progressbar
     *
     * @param postfix postfix message
     */
    virtual void set_postfix(const std::string& postfix) = 0;

    /**
     * @brief Get the current progress state
     *
     * @return progress state
     */
    virtual double current() const = 0;
};

}
}
}
