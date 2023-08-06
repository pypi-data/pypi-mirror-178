// SPDX-FileCopyrightText: 2022 Peter Urban, GEOMAR Helmholtz Centre for Ocean Research Kiel
// SPDX-FileCopyrightText: 2022 Sven Schorge, GEOMAR Helmholtz Centre for Ocean Research Kiel
// SPDX-FileCopyrightText: 2022 Peter Urban, Ghent University
//
// SPDX-License-Identifier: MPL-2.0
//

#pragma once

#include <fstream>
#include <limits>
#include <memory>
#include <unordered_map>
#include <vector>

/* memory mapping */
#include <boost/iostreams/device/mapped_file.hpp> // for mmap
#include <boost/iostreams/stream.hpp>             // for stream
#include <boost/sort/sort.hpp>                    // for sort

#include <fmt/core.h>
#include <themachinethatgoesping/tools/classhelper/objectprinter.hpp>
#include <themachinethatgoesping/tools/helper.hpp>
#include <themachinethatgoesping/tools/progressbars.hpp>
#include <themachinethatgoesping/tools/pyhelper/pyindexer.hpp>

#include "datagram_info_types.hpp"
#include "datagram_types.hpp"

namespace themachinethatgoesping {
namespace echosounders {
namespace fileinterfaces {

template<typename t_DatagramType,
         typename t_DatagramIdentifier,
         typename t_ifstream,
         typename t_DatagramTypeFactory = t_DatagramType>
class I_DatagramContainer
{
  protected:
    std::string _name;

    /* header positions */
    std::vector<DatagramInfo_ptr<t_DatagramIdentifier, t_ifstream>> _datagram_infos;
    tools::pyhelper::PyIndexer                                      _pyindexer;

  public:
    /**
     * @brief Construct a new empty I_DatagramContainer object
     *
     */
    I_DatagramContainer(std::string_view name = "I_DatagramContainer")
        : _name(name)
        , _pyindexer(0)
    {
    }

    I_DatagramContainer(
        std::vector<DatagramInfo_ptr<t_DatagramIdentifier, t_ifstream>> datagram_infos,
        std::string_view name = "I_DatagramContainer")
        : _name(name)
        , _datagram_infos(std::move(datagram_infos))
        , _pyindexer(_datagram_infos.size())
    {
    }

    ~I_DatagramContainer() = default;

    void add_datagram_info(DatagramInfo_ptr<t_DatagramIdentifier, t_ifstream> datagram_info)
    {
        this->_datagram_infos.push_back(std::move(datagram_info));
        _pyindexer.reset(_datagram_infos.size());
    }

    void add_datagram_infos(
        const std::vector<DatagramInfo_ptr<t_DatagramIdentifier, t_ifstream>>& datagram_infos)
    {
        this->_datagram_infos.insert(
            this->_datagram_infos.end(), datagram_infos.begin(), datagram_infos.end());
        _pyindexer.reset(_datagram_infos.size());
    }

    void set_datagram_infos(
        std::vector<DatagramInfo_ptr<t_DatagramIdentifier, t_ifstream>> datagram_infos)
    {
        _datagram_infos = std::move(datagram_infos);
        _pyindexer.reset(_datagram_infos.size());
    }

    const std::vector<DatagramInfo_ptr<t_DatagramIdentifier, t_ifstream>>& get_datagram_infos()
        const
    {
        return _datagram_infos;
    }

    // ----- iterator interface -----
    I_DatagramContainer reversed() const
    {
        return this->operator()(_pyindexer.reversed().to_slice());
    }

    I_DatagramContainer operator()(const tools::pyhelper::PyIndexer::Slice& slice) const
    {
        I_DatagramContainer sliced_container(*this);

        tools::pyhelper::PyIndexer pyindexer(_datagram_infos.size(), slice);

        std::vector<DatagramInfo_ptr<t_DatagramIdentifier, t_ifstream>> datagram_infos;
        datagram_infos.reserve(pyindexer.size());

        for (size_t i : pyindexer)
        {
            datagram_infos.push_back(_datagram_infos[i]);
        }

        sliced_container.set_datagram_infos(std::move(datagram_infos));

        return sliced_container;
    }

    I_DatagramContainer operator()(t_DatagramIdentifier datagram_identifier) const
    {
        I_DatagramContainer filtered(*this);

        std::vector<DatagramInfo_ptr<t_DatagramIdentifier, t_ifstream>> datagram_infos;

        for (const auto& datagram_info : _datagram_infos)
        {
            if (datagram_info->get_datagram_identifier() == datagram_identifier)
                datagram_infos.push_back(datagram_info);
        }

        filtered.set_datagram_infos(std::move(datagram_infos));

        return filtered;
    }

    I_DatagramContainer operator()(
        const std::vector<t_DatagramIdentifier>& datagram_identifiers) const
    {
        I_DatagramContainer filtered(*this);

        std::vector<DatagramInfo_ptr<t_DatagramIdentifier, t_ifstream>> datagram_infos;

        for (const auto& datagram_info : _datagram_infos)
        {
            if (std::find(datagram_identifiers.begin(),
                          datagram_identifiers.end(),
                          datagram_info->get_datagram_identifier()) != datagram_identifiers.end())
                datagram_infos.push_back(datagram_info);
        }

        filtered.set_datagram_infos(std::move(datagram_infos));

        return filtered;
    }

    std::map<t_DatagramIdentifier, size_t> count_datagrams_per_type() const
    {
        std::map<t_DatagramIdentifier, size_t> datagram_identifiers;

        for (const auto& datagram_info : _datagram_infos)
        {
            datagram_identifiers[datagram_info->get_datagram_identifier()] += 1;
        }

        return datagram_identifiers;
    }

    std::vector<t_DatagramIdentifier> find_datagram_types() const
    {
        std::set<t_DatagramIdentifier> datagram_identifiers;

        for (const auto& datagram_info : _datagram_infos)
        {
            datagram_identifiers.insert(datagram_info->get_datagram_identifier());
        }

        std::vector<t_DatagramIdentifier> vec;
        std::copy(
            datagram_identifiers.begin(), datagram_identifiers.end(), std::back_inserter(vec));
        return vec;
    }

    std::vector<I_DatagramContainer> break_by_time_diff(double max_time_diff_seconds) const
    {
        std::vector<I_DatagramContainer> containers;

        std::vector<DatagramInfo_ptr<t_DatagramIdentifier, t_ifstream>> datagram_infos;

        for (const auto& datagram_info : _datagram_infos)
        {
            if (!datagram_infos.empty())
            {
                if (datagram_info->get_timestamp() - datagram_infos.back()->get_timestamp() >
                    max_time_diff_seconds)
                {
                    containers.push_back(I_DatagramContainer(datagram_infos));
                    datagram_infos.clear();
                }
            }
            datagram_infos.push_back(datagram_info);
        }

        containers.push_back(I_DatagramContainer(datagram_infos));

        return containers;
    }

    // sort _datagram_infos by timestamp in _datagram_timestamps
    I_DatagramContainer get_sorted_by_time() const
    {
        I_DatagramContainer sorted(*this);
        // Your function
        auto& datagram_infos = sorted._datagram_infos;
        // sort _datagram_infos by  time, then file_pos then file number
        // TODO: this is faster than std sort, but python sorting (timsort?) seems
        // to be 10x faster for this use case
        boost::sort::pdqsort(
            datagram_infos.begin(), datagram_infos.end(), [](const auto& lhs, const auto& rhs) {
                if (lhs->get_timestamp() < rhs->get_timestamp())
                    return true;
                return false;
            });

        return sorted;
    }
    /**
     * @brief Compute some time statistics for the datagram_infos in the container
     * The is_sorted variable is interpreted as follos:
     *  - 1: the datagram_infos are sorted by time (ascending)
     *  - 0: the datagram_infos are not sorted by time
     * - -1: the datagram_infos are sorted by time (descending)
     *
     * @return std::tuple<min_timestamp, max_timestamp, is_sorted()>
     */
    std::tuple<double, double, int> timeinfo() const
    {
        double min_time  = std::numeric_limits<double>::max();
        double max_time  = std::numeric_limits<double>::min();
        int    is_sorted = 1;

        for (size_t i : _pyindexer)
        {
            const auto& datagram_info = _datagram_infos[i];
            min_time                  = std::min(min_time, datagram_info->get_timestamp());
            max_time                  = std::max(max_time, datagram_info->get_timestamp());

            if (i > 1)
            {
                if (is_sorted == 1)
                {
                    if (datagram_info->get_timestamp() < _datagram_infos[i - 1]->get_timestamp())
                        is_sorted = 0;
                }
                else if (is_sorted == -1)
                {
                    if (datagram_info->get_timestamp() > _datagram_infos[i - 1]->get_timestamp())
                        is_sorted = 0;
                }
            }
            else if (i == 1)
            {
                if (datagram_info->get_timestamp() < _datagram_infos[i - 1]->get_timestamp())
                    is_sorted = -1;
            }
        }

        return std::make_tuple(min_time, max_time, is_sorted);
    }

    size_t size() const { return _pyindexer.size(); }

    t_DatagramType at(long index)
    {
        const auto& datagram_info = _datagram_infos.at(_pyindexer(index));
        try
        {
            return datagram_info
                ->template read_datagram_from_file<t_DatagramType, t_DatagramTypeFactory>();

            // auto& ifs = datagram_info->get_stream_and_seek();

            // return t_DatagramTypeFactory::from_stream(ifs,
            // datagram_info->get_datagram_identifier());
        }
        catch (std::exception& e)
        {
            auto msg = fmt::format("Error reading datagram header: {}\n", e.what());
            msg += fmt::format("index: {}\n", index);
            msg += fmt::format("pyindex: {}\n", _pyindexer(index));
            msg += fmt::format("__datagram_infos.size(): {}\n", _datagram_infos.size());
            msg += fmt::format("pos: {}\n", datagram_info->get_file_pos());
            throw std::runtime_error(msg);
        }
    }

    // ----- printing interface -----
    tools::classhelper::ObjectPrinter __printer__(unsigned int float_precision) const
    {
        tools::classhelper::ObjectPrinter printer(_name, float_precision);

        printer.register_section("Time info (Datagrams)");
        double min_time, max_time;
        int    is_sorted;
        std::tie(min_time, max_time, is_sorted) = timeinfo();
        std::string is_sorted_str               = is_sorted == 1    ? "ascending"
                                                  : is_sorted == -1 ? "descending"
                                                                    : "no";
        std::string time_str_min =
            tools::timeconv::unixtime_to_datestring(min_time, 2, "%d/%m/%Y %H:%M:%S");
        std::string time_str_max =
            tools::timeconv::unixtime_to_datestring(max_time, 2, "%d/%m/%Y %H:%M:%S");
        printer.register_value("Start time", time_str_min);
        printer.register_value("End time", time_str_max);
        printer.register_value("Sorted", is_sorted_str);

        printer.register_section("Contained datagrams");
        auto datagram_identifiers = count_datagrams_per_type();
        if (datagram_identifiers.size() > 1)
        {
            printer.register_value("Total", _datagram_infos.size(), "");
        }
        for (const auto& [type, count] : datagram_identifiers)
        {
            printer.register_value("Datagrams [" + datagram_identifier_to_string(type) + "]",
                                   count,
                                   datagram_identifier_info(type));
        }

        return printer;
    }

    // -- class helper function macros --
    // define info_string and print functions (needs the __printer__ function)
    __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__
};

}
}
}
