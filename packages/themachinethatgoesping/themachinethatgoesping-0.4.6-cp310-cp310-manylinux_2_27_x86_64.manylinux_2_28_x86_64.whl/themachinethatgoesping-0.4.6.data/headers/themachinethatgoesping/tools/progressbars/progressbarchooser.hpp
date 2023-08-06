// SPDX-FileCopyrightText: 2022 Peter Urban, Ghent University
//
// SPDX-License-Identifier: MPL-2.0

#pragma once

#include <variant>

#include "consoleprogressbar.hpp"
#include "noindicator.hpp"
#include "progressindicator.hpp"

namespace themachinethatgoesping {
namespace tools {
namespace progressbars {

static enum class t_BuiltInProgressBar {
    pbar_NoIndicator,
    pbar_Indicator,
    pbar_Classic
} DefaultProgressBarType = t_BuiltInProgressBar::pbar_Indicator;

using v_BuiltInProgressBar = std::variant<NoIndicator, ProgressIndicator, ConsoleProgressBar>;

/**
 * @brief This class allows choosing between different progress bars
 * It will be extended in the future to allow setting the default progressbar using a configuration
 * file
 */
class ProgressBarChooser
{
    // I would prefer to derive from std::variant, but this is not supported by g++-11
    v_BuiltInProgressBar builtin_progress_bar;

  public:
    ProgressBarChooser() = default;

    /**
     * @brief Construct a new Progress Bar Chooser. This will select the default progress bar type
     * if show_progress is true and NoIndicator otherwise.
     *
     * @param show_progress
     */
    ProgressBarChooser(bool show_progress)
    {
        if (show_progress)
        {
            switch (DefaultProgressBarType)
            {
                case t_BuiltInProgressBar::pbar_Indicator:
                    builtin_progress_bar.emplace<ProgressIndicator>();
                    break;
                case t_BuiltInProgressBar::pbar_Classic:
                    builtin_progress_bar.emplace<ConsoleProgressBar>();
                    break;
                case t_BuiltInProgressBar::pbar_NoIndicator:
                    builtin_progress_bar.emplace<NoIndicator>();
                    break;
                default:
                    throw std::runtime_error("Unknown progress bar type");
            }
        }
        // else //(variants default is NoIndicator )
        // {
        //     builtin_progress_bar.emplace<NoIndicator>();
        // }
    }
    // ProgressBarChooser(t_BuiltInProgressBar progress_bar_type)
    // {
    //     switch (progress_bar_type)
    //     {
    //         case t_BuiltInProgressBar::pbar_Indicator:
    //             builtin_progress_bar.emplace<ProgressIndicator>();
    //             break;
    //         case t_BuiltInProgressBar::pbar_Classic:
    //             builtin_progress_bar.emplace<ConsoleProgressBar>();
    //             break;
    //         case t_BuiltInProgressBar::pbar_NoIndicator:
    //             builtin_progress_bar.emplace<NoIndicator>();
    //             break;
    //     }
    // }

    ~ProgressBarChooser() = default;

    /**
     * @brief This is the visitor function that implicitly converts t_ProgressBar to I_ProgressBar
     * (the common interface)
     *
     * @tparam t_ProgressBar
     * @param progress_bar ProgressBar class that is derived from I_ProgressBar
     * @return I_ProgressBar&
     */
    template<typename t_ProgressBar>
    I_ProgressBar& operator()(t_ProgressBar& progress_bar) const
    {
        return progress_bar;
    }

    /**
     * @brief get the ProgressBarInterface
     *
     * @return I_ProgressBar&
     */
    I_ProgressBar& get() { return std::visit(ProgressBarChooser{}, builtin_progress_bar); }
};

// I_ProgressBar& get(ProgressBar& progress_bar)
// {
//     return std::visit(ProgressBarVisitor{}, progress_bar);
// }

} // namespace progressbars
} // namespace tools
} // namespace themachinethatgoesping
