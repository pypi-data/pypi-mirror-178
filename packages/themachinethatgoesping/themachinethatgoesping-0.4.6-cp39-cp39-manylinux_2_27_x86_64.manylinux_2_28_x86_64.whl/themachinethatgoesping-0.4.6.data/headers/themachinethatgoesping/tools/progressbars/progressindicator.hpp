// SPDX-FileCopyrightText: 2022 Peter Urban, Ghent University
//
// SPDX-License-Identifier: MPL-2.0

#pragma once

#include "i_progressbartimed.hpp"

#include <iostream>
#include <memory>
#include <thread>

#include <indicators/block_progress_bar.hpp>
#include <indicators/progress_spinner.hpp>

namespace themachinethatgoesping {
namespace tools {
namespace progressbars {

/**
 * @brief Text based ProgressBar that uses the indicators library.
 * (https://github.com/p-ranav/indicators)
 *
 * This class is based in I_ProgressBarTimed such that the callbacks are guarded by a timer.
 */
class ProgressIndicator : public I_ProgressBarTimed
{
    double _first = 0.0; ///< first value of the progressbar range

    std::unique_ptr<indicators::ProgressSpinner>
        _indicator; ///< indicator progressbar implementation
                    // std::unique_ptr<indicators::BlockProgressBar> _indicator;

  public:
    ProgressIndicator()  = default;
    ~ProgressIndicator() = default;

  private:
    // ----- I_ProgressBarTimed interface -----
    void callback_init(double first, double last, const std::string& name = "process") override
    {
        // set the _first state to support ranges that do not start at 0.0
        _first = first;

        // initialize the indicator progressbar
        _indicator = std::make_unique<indicators::ProgressSpinner>();
        //_indicator = std::make_unique<indicators::BlockProgressBar>();

        // set the possible spinner states
        _indicator->set_option(indicators::option::SpinnerStates{
            std::vector<std::string>{ "⠈", "⠐", "⠠", "⢀", "⡀", "⠄", "⠂", "⠁" } });

        // set indicator progressbar options
        _indicator->set_option(indicators::option::ForegroundColor{ indicators::Color::yellow });

        _indicator->set_option(indicators::option::FontStyles{
            std::vector<indicators::FontStyle>{ indicators::FontStyle::bold } });

        _indicator->set_option(indicators::option::ShowPercentage{ true });
        _indicator->set_option(indicators::option::ShowElapsedTime{ true });
        _indicator->set_option(indicators::option::ShowRemainingTime{ true });

        _indicator->set_option(indicators::option::PrefixText{ name + " " });
        _indicator->set_option(indicators::option::MaxProgress{ size_t(ceil(last - first)) });
    }

    void callback_close(const std::string& msg = "done") override
    {
        // close the indicator progressbar
        _indicator->set_option(indicators::option::PostfixText{ "[" + msg + "]" });
        _indicator->mark_as_completed();
    }

    void callback_set_progress(double new_progress) override
    {
        // set the progress of the indicator progressbar
        _indicator->set_progress(size_t(new_progress - _first));
    }
    void callback_set_postfix(const std::string& postfix) override
    {
        // set the postfix of the indicator progressbar
        _indicator->set_option(indicators::option::PostfixText{ "[" + postfix + "]" });
    }

    void callback_tick(double increment = 1) override
    {
        // tick the indicator progressbar using set_progress to support incrementing by a value
        // other than 1
        callback_set_progress(_indicator->current() + increment);
    }

    double callback_current() const override
    {
        // return the current progress of the indicator progressbar
        return double(_indicator->current());
    }
};

}
}
}
