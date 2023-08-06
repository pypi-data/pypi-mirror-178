// SPDX-FileCopyrightText: 2022 Peter Urban, Ghent University
// SPDX-FileCopyrightText: 2022 Peter Urban, GEOMAR Helmholtz Centre for Ocean
// Research Kiel
//
// SPDX-License-Identifier: MPL-2.0

/**
 * @brief (Modified) akima interpolator class. Uses boost makima interpolator
 *
 * @authors Peter Urban
 *
 */

#pragma once

#include <array>
#include <boost/math/interpolators/makima.hpp>
#include <iostream>
#include <unordered_map>
#include <vector>

#include "i_interpolator.hpp"
#include "linearinterpolator.hpp"

#include "../classhelper/bitsery.hpp"
#include "../classhelper/objectprinter.hpp"
#include "../helper.hpp"

namespace themachinethatgoesping {
namespace tools {
namespace vectorinterpolators {

/**
 * @brief Interpolator class to perform a (modified) akima interpolation. Uses
 * boost makima interpolator. Note: this interpolator acts as linear interpolator if less than 4
 * values are stored.
 *
 */
class AkimaInterpolator : public I_Interpolator<double>
{
    // boost akima spline currently does not allow for accessing the internal data
    // therefore we need to keep synchronized copies of the data here as well to allow get_X and
    // get_Y functions
    std::vector<double> _X;
    std::vector<double> _Y;

    // initialize these interpolators with non-sense (will be initialized by calling set_data_XY)
    LinearInterpolator _min_linearextrapolator = LinearInterpolator();
    LinearInterpolator _max_linearextrapolator = LinearInterpolator();
    boost::math::interpolators::makima<std::vector<double>> _akima_spline =
        boost::math::interpolators::makima<std::vector<double>>({ 0, 1, 2, 3 }, { 0, 0, 0, 0 });

  public:
    /**
     * @brief Construct a new (uninitialized) Akima Interpolator object
     *
     */
    AkimaInterpolator(t_extr_mode extrapolation_mode = t_extr_mode::extrapolate)
        : I_Interpolator<double>(extrapolation_mode, "AkimaInterpolator")
    {
        // set_data_XY({ 0, 1, 2, 3 }, { 0, 1, 2, 3 });
    }

    /**
     * @brief Construct a new Akima Spline Interpolator object from a vector of
     * pairs This class uses the modified akima interpolation of boost c++
     * https://www.boost.org/doc/libs/1_79_0/libs/math/doc/html/math_toolkit/makima.html
     * usage: interpolated_y_value = interpolator(x_value)
     *
     * @param X X vector; must be unique and sorted in ascending order. same
     * size as Y!
     * @param Y Y vector; must be unique and sorted in ascending order. same
     * size as X!
     * @param extrapolation_mode :py:class:`t_extr_mode
     * <themachinethatgoesping.tools.vectorinterpolators.t_extr_mode>` object
     * that describes the extrapolation mode
     */
    AkimaInterpolator(std::vector<double> X,
                      std::vector<double> Y,
                      t_extr_mode         extrapolation_mode = t_extr_mode::extrapolate)
        : I_Interpolator<double>(extrapolation_mode, "AkimaInterpolator")
    {
        set_data_XY(std::move(X), std::move(Y));
    }
    ~AkimaInterpolator() = default;

    /**
     * @brief check if the interpolator contains data
     */
    bool empty() const { return _X.empty(); }

    static std::string type_to_string() { return "AkimaInterpolator"; }

    // -- convenience functions --
    bool operator!=(const AkimaInterpolator& rhs) const { return !(rhs == *this); }
    bool operator==(const AkimaInterpolator& rhs) const
    {
        // compare extrapolation mode
        if (_extr_mode != rhs.get_extrapolation_mode())
            return false;

        // compare data
        if (!helper::approx_container(_X, rhs._X))
            return false;
        if (!helper::approx_container(_Y, rhs._Y))
            return false;

        return true;
    }

    /**
     * @brief get the interpolated y value for given x target
     *
     * @param target_x find the corresponding y value for this x value
     * @return corresponding y value
     */
    double operator()(double target_x) final
    {
        // if less than 4 values are present, act as linear interpolator
        if (_X.size() < 4)
            return _min_linearextrapolator(target_x);

        // check if _X (and _Y) are initialized (_X and _Y should always be the same size)
        if (_X.size() == 0)
            throw(std::domain_error(
                "ERROR[Interpolator::operator()]: data vectors are not initialized!"));

        // if size of _X is 1, return _Y[0]
        if (_X.size() == 1)
            return _Y[0];

        if (target_x < _X[0])
        {
            switch (I_Interpolator::_extr_mode)
            {
                case t_extr_mode::nearest:
                    return _Y[0];

                case t_extr_mode::extrapolate:
                    return _min_linearextrapolator(target_x);

                default: // fail
                    std::string msg;
                    msg += "ERROR[INTERPOLATE]: x value [" + std::to_string(target_x) +
                           "] is out of range (too small)(" + std::to_string(_X[0]) + "/" +
                           std::to_string(_X.back()) + ")! (and fail on extrapolate was set)";
                    throw(std::out_of_range(msg));
            }
        }
        else if (target_x > _X.back())
        {
            switch (I_Interpolator::_extr_mode)
            {
                case t_extr_mode::nearest:
                    return _Y.back();

                case t_extr_mode::extrapolate:
                    return _max_linearextrapolator(target_x);

                default: // fail
                    std::string msg;
                    msg += "ERROR[INTERPOLATE]: x value [" + std::to_string(target_x) +
                           "] is out of range  (too large)(" + std::to_string(_X[0]) + "/" +
                           std::to_string(_X.back()) + ")! (and fail on extrapolate was set)";
                    throw(std::out_of_range(msg));
            }
        }

        return _akima_spline(target_x);
    }

    /**
     * @brief get nearest y values for given x targets (vectorized call)
     *
     * @param targets_x vector of x values. For each of these values find the
     * corrsponding y value
     * @return corresponding y value
     */
    std::vector<double> operator()(const std::vector<double>& targetsX)
    {
        return I_Interpolator<double>::operator()(targetsX);
    }

    /**
     * @brief change the input data to these X and Y vectors
     *
     * @param X: x vector (must be same size)
     * @param Y: y vector (must be same size)
     */
    void set_data_XY(std::vector<double> X, std::vector<double> Y) final
    {
        // check if X and Y are valid
        I_Interpolator<double>::_check_XY(X, Y);

        // copy data to allow get_X and get_Y functions
        _X = X;
        _Y = Y;

        if (_X.size() >= 4) // default case
        {
            _akima_spline =
                boost::math::interpolators::makima<std::vector<double>>(std::move(X), std::move(Y));

            _init_linearextrapolators();
        }
        else // if < 4 values, act as linear interpolator
        {
            _min_linearextrapolator.set_data_XY(std::move(X), std::move(Y));
        }
    }

    void append(double x, double y) final
    {
        if (_X.size() > 0)
            if (x <= _X.back())
            {
                throw(std::domain_error("ERROR[Interpolation::append]: appended x value is not "
                                        "larger than existing x values in the interpolator."));
            }

        if (!std::isfinite(x))
            throw(std::domain_error(
                "ERROR[Interpolator::append]: X contains NAN or INFINITE values!"));
        if (!std::isfinite(y))
            throw(std::domain_error(
                "ERROR[Interpolator::append]: Y contains NAN or INFINITE values!"));

        // copy data to allow get_X and get_Y functions
        _X.push_back(x);
        _Y.push_back(y);

        if (_X.size() > 4) // default case
        {
            _akima_spline.push_back(x, y);
            _init_linearextrapolators();
        }
        else // initialize interpolator if less than 4 values where present before
        {
            set_data_XY(std::move(_X), std::move(_Y));
        }
    }

    void extend(const std::vector<double>& X, const std::vector<double>& Y) final
    {
        if (X.size() != Y.size())
            throw(std::invalid_argument("ERROR[Interpolator::extend]: list sizes do not match"));

        size_t orig_size = _X.size();

        try
        {
            // initialize interpolator if less than 4 values where present before
            if (_X.size() < 4)
            {
                std::copy(X.begin(), X.end(), std::back_inserter(_X));
                std::copy(Y.begin(), Y.end(), std::back_inserter(_Y));

                set_data_XY(std::move(_X), std::move(_Y));
                return;
            }

            for (unsigned int i = 0; i < X.size(); ++i)
            {
                _akima_spline.push_back(X[i], Y[i]);

                // copy data to allow get_X and get_Y functions
                _X.push_back(X[i]);
                _Y.push_back(Y[i]);
            }

            _init_linearextrapolators();
        }
        catch (...)
        {
            // restore original size if something went wrong
            _X.resize(orig_size);
            _Y.resize(orig_size);

            set_data_XY(std::move(_X), std::move(_Y));
            throw;
        }
    }

    void insert(const std::vector<double>& X, const std::vector<double>& Y) final
    {
        if (X.size() != Y.size())
            throw(std::domain_error("ERROR[Interpolator::insert]: list sizes do not match"));

        std::vector<std::pair<double, double>> XY;
        XY.reserve(_X.size() + X.size());

        // sort _X and _Y by _X (ascending)
        for (unsigned int i = 0; i < _X.size(); ++i)
        {
            XY.push_back(std::pair<double, double>(_X[i], _Y[i]));
        }
        for (unsigned int i = 0; i < X.size(); ++i)
        {
            XY.push_back(std::pair<double, double>(X[i], Y[i]));
        }

        std::sort(
            XY.begin(), XY.end(), [](const auto& a, const auto& b) { return a.first < b.first; });

        // copy back to _X and _Y
        std::vector<double> X_new;
        std::vector<double> Y_new;
        X_new.resize(XY.size());
        Y_new.resize(XY.size());
        for (unsigned int i = 0; i < XY.size(); ++i)
        {
            X_new[i] = XY[i].first;
            Y_new[i] = XY[i].second;
        }

        set_data_XY(std::move(X_new), std::move(Y_new));
    }

    // -----------------------
    // getter functions
    // -----------------------
    /**
     * @brief return the x component of the internal data vector
     *
     * @return std::vector<double>
     */
    const std::vector<double>& get_data_X() const final { return _X; }

    /**
     * @brief return the y component of the internal data vector
     *
     * @return std::vector<YType>
     */
    const std::vector<double>& get_data_Y() const final { return _Y; }

  private:
    /**
     * @brief internal function to initialize the linear extrapolation objects
     * _X, _Y and the _akima_spline
     * must be set/initialized before calling this function
     *
     */
    void _init_linearextrapolators()
    {
        // interpolated elements just (1%) before the min/max xvalue
        double min_x_dx = _X[0] + (_X[1] - _X[0]) * 0.01;
        double max_x_dx = _X.back() - (_X.back() - _X[_X.size() - 2]) * 0.01;

        _min_linearextrapolator =
            LinearInterpolator({ _X[0], min_x_dx }, { _Y[0], _akima_spline(min_x_dx) });
        _max_linearextrapolator =
            LinearInterpolator({ max_x_dx, _X.back() }, { _akima_spline(max_x_dx), _Y.back() });
    }

    // serialization support using bitsery
    friend bitsery::Access;
    template<typename S>
    void serialize(S& s)
    {
        // serialize internal variables and extra _X and _Y
        s.value4b(_extr_mode);
        s.container8b(_X, SERIALIZER_DEFAULT_MAX_CONTAINER_SIZE);
        s.container8b(_Y, SERIALIZER_DEFAULT_MAX_CONTAINER_SIZE);

        // initialize boost akima on read
        // TODO: this is a hack, think about forking boost makima to get proper access to private X
        // and Y data structures
        if (bitsery_helper::is_input(s))
        {
            this->set_data_XY(std::move(_X), std::move(_Y));
        }
    }

  public:
    classhelper::ObjectPrinter __printer__(unsigned int float_precision) const
    {
        classhelper::ObjectPrinter printer(this->get_name(), float_precision);

        printer.register_enum("extr_mode", _extr_mode);
        printer.register_section("data lists");
        printer.register_container("X", _X);
        printer.register_container("Y", _Y);

        return printer;
    }

  public:
    // -- class helper function macros --
    // define to_binary and from_binary functions (needs the serialize function)
    __BITSERY_DEFAULT_TOFROM_BINARY_FUNCTIONS__(AkimaInterpolator)
    // define info_string and print functions (needs the __printer__ function)
    __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__
};

} // namespace vectorinterpolators
} // namespace tools
} // namespace themachinethatgoesping
