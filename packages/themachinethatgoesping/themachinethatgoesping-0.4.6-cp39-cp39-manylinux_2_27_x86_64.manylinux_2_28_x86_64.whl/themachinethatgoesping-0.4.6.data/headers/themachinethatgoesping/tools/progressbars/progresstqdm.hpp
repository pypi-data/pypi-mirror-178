// SPDX-FileCopyrightText: 2022 Peter Urban, Ghent University
//
// SPDX-License-Identifier: MPL-2.0

#pragma once

#include "i_progressbartimed.hpp"

#include <iostream>
#include <memory>
#include <thread>

#include <pybind11/pybind11.h>

namespace themachinethatgoesping {
namespace tools {
namespace progressbars {

/**
 * @brief Python ProgressBar that uses the tqdm. This is a test implementation for reference only.
 * Do not use in production! Including this header will result in a compilation error if the
 * project is not linked against pybind11 (not default for themachinethatgoesping_tools).
 *
 * This class is based in I_ProgressBarTimed such that the callbacks are guarded by a timer.
 */
class ProgressTqdm
    : public I_ProgressBarTimed
    , public pybind11::object
{
    double _first = 0;

  public:
    /**
     * @brief Construct a new Progress Tqdm object
     * To initialize a tqdm object call: from tqdm import tqdm, and use tqdm()
     *
     * @param tqdm A python tqdm class object
     */
    ProgressTqdm(pybind11::object tqdm)
        : pybind11::object(tqdm)
    {
    }
    ~ProgressTqdm() = default;

  private:
    // ----- I_ProgressBarTimed interface -----

    void callback_init(double first, double last, const std::string& name = "process") override
    {
        // set the _first state to support ranges that do not start at 0.0
        _first = first;

        // initialize the tqdm progressbar
        attr("set_description")(name);
        attr("reset")(last - first);
    }

    void callback_close(const std::string& msg = "done") override
    {
        // close the tqdm progressbar
        attr("set_postfix_str")("[" + msg + "]");
        attr("close")();
    }

    void callback_set_progress(double new_progress) override
    {
        // set the progress of the tqdm progressbar
        double increment = new_progress - _first - pybind11::cast<double>(attr("n")());
        attr("update")(increment);
    }
    void callback_set_postfix(const std::string& postfix) override
    {
        // set the postfix of the tqdm progressbar
        attr("set_postfix_str")("[" + postfix + "]");
    }

    void callback_tick(double increment = 1) override
    {
        // increment the tqdm progressbar
        attr("update")(increment);
    }

    double callback_current() const override
    {
        // get state of the tqdm progressbar
        return pybind11::cast<double>(attr("n")());
    }
};

}
}
}
