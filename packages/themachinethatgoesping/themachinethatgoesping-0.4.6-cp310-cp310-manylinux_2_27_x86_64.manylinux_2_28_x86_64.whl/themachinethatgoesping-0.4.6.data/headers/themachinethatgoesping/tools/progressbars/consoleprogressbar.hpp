// SPDX-FileCopyrightText: Peter Urban, 2022 GEOMAR Helmholtz Centre for Ocean Research Kiel
// SPDX-FileCopyrightText: 2022 Peter Urban, Ghent University
//
// SPDX-License-Identifier: MPL-2.0

#pragma once

#include "i_progressbartimed.hpp"
#include <iostream>

namespace themachinethatgoesping {
namespace tools {
namespace progressbars {

/**
 * @brief Old-school progress bar that prints to terminal. For reference only, might be removed in
 * the future.
 *
 * This class is based in I_ProgressBarTimed such that the callbacks are guarded by a timer.
 */
class ConsoleProgressBar : public I_ProgressBarTimed
{
    std::ostream& _os; ///< output stream

    // internal state
    double       _first;       ///< starting value
    double       _last;        ///< ending value
    double       _current;     ///< current value
    unsigned int _currentStep; ///< step (step "/" of _numOf_steps)

    const unsigned int _numOf_steps = 50; ///< steps till 100% (equals linesize)

    bool _initialized = false; ///< flag to control if the progressbar is initialized

  public:
    ConsoleProgressBar(std::ostream& os = std::cout)
        : _os(os)
    {
    }

  private:
    // ----- I_ProgressBarTimed interface -----
    void callback_init(double first, double last, const std::string& name = "process") override
    {
        /* check if _initialized already */
        if (_initialized)
            I_ProgressBarTimed::close();
        // throw(std::runtime_error("ERROR[ConsoleProgressBar]: Can't start StatusBar! StatusBar "
        //                          "is already _initialized!"));

        /* check conditions */
        if (first > last)
            throw(std::runtime_error("ERROR[ConsoleProgressBar]: last !> first! [" +
                                     std::to_string(last) + " !> " + std::to_string(first) + "]"));

        _first       = first;
        _last        = last;
        _current     = first;
        _initialized = true;
        _currentStep = 0;

        std::string out;
        std::string prc          = "... " + name + " ... ";
        std::string prc_progress = "                                             100%|";
        std::string progress     = "\n0%                    50%                    100%|";

        if (prc.size() < 45)
            out = prc_progress.replace(0, prc.size(), prc);
        else
            out = prc + progress;

        _os << out << "\n" << std::flush;
    }

    void callback_close(const std::string& msg = "done") override
    {
        /* check if _initialized already */
        if (!_initialized)
            throw(
                std::runtime_error("ERROR[DSMToolsLib::Status::ConsoleProgressBar::last))]: Can't "
                                   "stop StatusBar! StatusBar is not _initialized yet!"));

        for (unsigned int i = 1; i < _numOf_steps - _currentStep; i++)
            _os << "\\" << std::flush;

        _os << "| [ " << msg << " ]" << std::endl;

        _initialized = false;
    }

    void callback_set_progress(double new_progress) override
    {
        /* check if _initialized already */
        if (!_initialized)
            throw(
                std::runtime_error("ERROR[DSMToolsLib::Status::ConsoleProgressBar::update))]: Not "
                                   "possible to call update! StatusBar is not _initialized yet!"));

        if (new_progress < _current)
            // throw(std::runtime_error("ERROR[DSMToolsLib::Status::ConsoleProgressBar::update]: new
            // status is less than old status! [" + std::to_string(new_progress) + " < " +
            // std::to_string(_current) + "]"));
            std::cerr
                << "WARNING[DSMToolsLib::Status::ConsoleProgressBar::update]: new status is less "
                   "than old status! [" +
                       std::to_string(new_progress) + " < " + std::to_string(_current) + "]"
                << std::endl;

        if (new_progress > _last)
            // throw(std::runtime_error("ERROR[DSMToolsLib::Status::ConsoleProgressBar::update]:
            // statusOverflow! \n\t- current status :" + std::to_string(new_progress) + "\n\t- last
            // status: " + std::to_string(_last) + "]"));
            std::cerr
                << "ERROR[DSMToolsLib::Status::ConsoleProgressBar::update]: statusOverflow! \n\t- "
                   "current status :" +
                       std::to_string(new_progress) +
                       "\n\t- last status: " + std::to_string(_last) + "]"
                << std::endl;

        _current = new_progress;

        unsigned int status_steps = (unsigned int)std::round(
            ((double)_numOf_steps - 1) * (_current - _first) / (_last - _first));

        while (_currentStep < status_steps)
        {
            _currentStep++;
            _os << "/" << std::flush;
        }
    }
    void callback_set_postfix([[maybe_unused]] const std::string& postfix) override{};

    void callback_tick(double increment = 1) override
    {
        callback_set_progress(_current + increment);
    }

    double callback_current() const override { return _current; }
};

}
}
}
