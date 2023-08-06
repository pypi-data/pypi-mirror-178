// SPDX-FileCopyrightText: 2022 Tim Weiß, GEOMAR Helmholtz Centre for Ocean Research Kiel
// SPDX-FileCopyrightText: 2022 Peter Urban, GEOMAR Helmholtz Centre for Ocean Research Kiel
// SPDX-FileCopyrightText: 2022 Peter Urban, Ghent University
//
// SPDX-License-Identifier: MPL-2.0

#pragma once

/* library includes */
#include <magic_enum.hpp>

/* themachinethatgoesping includes */
#include <themachinethatgoesping/navigation/navigationinterpolatorlatlon.hpp>
#include <themachinethatgoesping/tools/classhelper/objectprinter.hpp>
#include <themachinethatgoesping/tools/helper.hpp>
#include <themachinethatgoesping/tools/progressbars.hpp>

#include "../fileinterfaces/i_inputfile.hpp"
#include "../fileinterfaces/i_pingcontainer.hpp"

#include "simradannotationdatainterface.hpp"
#include "simradconfigurationdatainterface.hpp"
#include "simradenvironmentdatainterface.hpp"
#include "simradnavigationdatainterface.hpp"
#include "simradotherdatainterface.hpp"
#include "simradpingdatainterface.hpp"

#include "simraddatagraminterface.hpp"
#include "simradping.hpp"

#include "simrad_datagrams.hpp"
#include "simrad_types.hpp"

namespace themachinethatgoesping {
namespace echosounders {
namespace simrad {

template<typename t_ifstream>
using SimradPingContainer = fileinterfaces::I_PingContainer<SimradPing<t_ifstream>>;

template<typename t_ifstream>
class FileSimradRaw
    : public fileinterfaces::I_InputFile<datagrams::SimradDatagram,
                                         SimradDatagramInterface<t_ifstream>>
{
    using t_base =
        fileinterfaces::I_InputFile<datagrams::SimradDatagram, SimradDatagramInterface<t_ifstream>>;

    SimradPingContainer<t_ifstream> _ping_container;
    tools::helper::DefaultSharedPointerMap<std::string, SimradPingContainer<t_ifstream>>
        _ping_container_by_channel;

    std::shared_ptr<SimradConfigurationDataInterface<t_ifstream>> _configuration_interface =
        std::make_shared<SimradConfigurationDataInterface<t_ifstream>>();
    std::shared_ptr<SimradNavigationDataInterface<t_ifstream>> _navigation_interface =
        std::make_shared<SimradNavigationDataInterface<t_ifstream>>(_configuration_interface);
    std::shared_ptr<SimradEnvironmentDataInterface<t_ifstream>> _environment_interface =
        std::make_shared<SimradEnvironmentDataInterface<t_ifstream>>(_navigation_interface);
    std::shared_ptr<SimradPingDataInterface<t_ifstream>> _ping_interface =
        std::make_shared<SimradPingDataInterface<t_ifstream>>(_environment_interface);

    std::shared_ptr<SimradAnnotationDataInterface<t_ifstream>> _annotation_interface =
        std::make_shared<SimradAnnotationDataInterface<t_ifstream>>();
    std::shared_ptr<SimradOtherDataInterface<t_ifstream>> _otherdata_interface =
        std::make_shared<SimradOtherDataInterface<t_ifstream>>();

  public:
    // inherit constructors
    // This does not work, because I_InputFile calls append before the callback functions are
    // overwritten Thus inheriting constructors would lead to calling the callback functions of the
    // base class using fileinterfaces::I_InputFile<datagrams::SimradDatagram,
    // t_SimradDatagramIdentifier, t_ifstream>::
    //     I_InputFile;

    FileSimradRaw(const std::string& file_path, bool show_progress = true)
    {
        this->append_file(file_path, show_progress);
    }
    FileSimradRaw(const std::string& file_path, tools::progressbars::I_ProgressBar& progress_bar)
    {
        this->append_file(file_path, progress_bar);
    }

    FileSimradRaw(const std::vector<std::string>& file_paths, bool show_progress)
    {
        this->append_files(file_paths, show_progress);
    }
    FileSimradRaw(const std::vector<std::string>&     file_paths,
                  tools::progressbars::I_ProgressBar& progress_bar)
    {
        this->append_files(file_paths, progress_bar);
    }
    ~FileSimradRaw() = default;

    SimradConfigurationDataInterface<t_ifstream>& configuration_interface()
    {
        return *_configuration_interface;
    }
    SimradNavigationDataInterface<t_ifstream>& navigation_interface()
    {
        return *_navigation_interface;
    }
    SimradEnvironmentDataInterface<t_ifstream>& environment_interface()
    {
        return *_environment_interface;
    }
    SimradPingDataInterface<t_ifstream>&       ping_interface() { return *_ping_interface; }
    SimradAnnotationDataInterface<t_ifstream>& annotation_interface()
    {
        return *_annotation_interface;
    }
    SimradOtherDataInterface<t_ifstream>& otherdata_interface() { return *_otherdata_interface; }

    SimradPingContainer<t_ifstream> pings() const { return _ping_container; }

    SimradPingContainer<t_ifstream> pings(const std::string& channel_id) const
    {
        return *_ping_container_by_channel.at_const(channel_id);
    }
    SimradPingContainer<t_ifstream> pings(const std::vector<std::string>& channel_ids) const
    {
        return _ping_container(channel_ids);
    }
    std::vector<std::string> channel_ids() const
    {
        std::vector<std::string> channel_ids;
        for (const auto& [k, v] : _ping_container_by_channel)
        {
            channel_ids.push_back(k);
        }

        return channel_ids;
    }

  protected:
    struct
    {
        std::map<std::string, std::shared_ptr<datagrams::xml_datagrams::XML_Parameter_Channel>>
            channel_parameters_per_channel_id;
        std::unordered_map<datagrams::xml_datagrams::XML_Parameter_Channel,
                           std::shared_ptr<datagrams::xml_datagrams::XML_Parameter_Channel>>
            channel_parameters;
    } _packet_buffer;

    void callback_scan_new_file_begin([[maybe_unused]] const std::string& file_path,
                                      [[maybe_unused]] size_t             file_paths_cnt) final
    {
        _configuration_interface->add_file_interface(file_paths_cnt);
        _navigation_interface->add_file_interface(file_paths_cnt);
        _environment_interface->add_file_interface(file_paths_cnt);
        _ping_interface->add_file_interface(file_paths_cnt);
    }
    void callback_scan_new_file_end([[maybe_unused]] const std::string& file_path,
                                    [[maybe_unused]] size_t             file_paths_cnt) final
    {
        if (_configuration_interface->per_file(file_paths_cnt).empty())
            fmt::print(std::cerr,
                       "WARNING: No configuration datagrams found in file {}: {}\n",
                       file_paths_cnt,
                       file_path);
        else
            _configuration_interface->per_file(file_paths_cnt).init_from_file();

        if (_navigation_interface->per_file(file_paths_cnt).empty())
            fmt::print(std::cerr,
                       "WARNING: No navigation datagrams found in file {}: {}\n",
                       file_paths_cnt,
                       file_path);
        else
            _navigation_interface->per_file(file_paths_cnt).init_from_file();
    }

    fileinterfaces::DatagramInfo_ptr<t_SimradDatagramIdentifier, t_ifstream> callback_scan_packet(
        t_ifstream&                   ifs,
        typename t_ifstream::pos_type pos,
        size_t                        file_paths_cnt) final
    {
        auto header = datagrams::SimradDatagram::from_stream(ifs);
        auto type   = header.get_datagram_identifier();

        auto datagram_info =
            std::make_shared<fileinterfaces::DatagramInfo<t_SimradDatagramIdentifier, t_ifstream>>(
                file_paths_cnt,
                pos,
                this->_input_file_manager,
                header.get_timestamp(),
                header.get_datagram_identifier());

        // auto datagram_info =
        // std::make_shared<fileinterfaces::DatagramInfo<t_SimradDatagramIdentifier>>();
        // datagram_info->file_nr             = file_paths_cnt;
        // datagram_info->file_pos            = pos;
        // datagram_info->timestamp           = header.get_timestamp();
        // datagram_info->datagram_identifier = header.get_datagram_identifier();

        switch (type)
        {
            case t_SimradDatagramIdentifier::NME0:
                [[fallthrough]];
            case t_SimradDatagramIdentifier::MRU0: {
                _navigation_interface->add_datagram_info(datagram_info);
                header.skip(ifs);
                break;
            }
            case t_SimradDatagramIdentifier::XML0: {

                auto xml = datagrams::XML0::from_stream(ifs, header);

                if (!ifs.good())
                    break;

                auto xml_type = xml.get_xml_datagram_type();

                if (xml_type == "Parameter")
                {
                    auto channel =
                        std::get<datagrams::xml_datagrams::XML_Parameter>(xml.decode()).Channels[0];

                    // add channel_ptr if channel is not in in _packet_buffer.channel_parameters
                    // keys
                    if (_packet_buffer.channel_parameters.find(channel) ==
                        _packet_buffer.channel_parameters.end())
                    {
                        auto channel_ptr =
                            std::make_shared<datagrams::xml_datagrams::XML_Parameter_Channel>(
                                channel);
                        _packet_buffer.channel_parameters[channel] = channel_ptr;
                        _packet_buffer.channel_parameters_per_channel_id[channel.ChannelID] =
                            channel_ptr;
                    }
                    else
                    {
                        // update channel_ptr if channel is in in _packet_buffer.channel_parameters
                        // keys
                        auto channel_ptr = _packet_buffer.channel_parameters[channel];
                        _packet_buffer.channel_parameters_per_channel_id[channel.ChannelID] =
                            channel_ptr;
                    }

                    _ping_interface->add_channel_parameter(channel, channel.ChannelID);
                    _ping_interface->add_datagram_info(datagram_info);
                }
                else if (xml_type == "InitialParameter")
                {
                    auto channels =
                        std::get<datagrams::xml_datagrams::XML_InitialParameter>(xml.decode())
                            .Channels;

                    for (const auto& channel : channels)
                    {
                        // add channel_ptr if channel is not in in _packet_buffer.channel_parameters
                        // keys
                        if (_packet_buffer.channel_parameters.find(channel) ==
                            _packet_buffer.channel_parameters.end())
                        {
                            auto channel_ptr =
                                std::make_shared<datagrams::xml_datagrams::XML_Parameter_Channel>(
                                    channel);
                            _packet_buffer.channel_parameters[channel] = channel_ptr;
                            _packet_buffer.channel_parameters_per_channel_id[channel.ChannelID] =
                                channel_ptr;
                        }
                        else
                        {
                            // update channel_ptr if channel is in in
                            // _packet_buffer.channel_parameters keys
                            auto channel_ptr = _packet_buffer.channel_parameters[channel];
                            _packet_buffer.channel_parameters_per_channel_id[channel.ChannelID] =
                                channel_ptr;
                        }
                        _ping_interface->add_channel_parameter(channel, channel.ChannelID);
                    }
                    _ping_interface->add_datagram_info(datagram_info);
                }
                else if (xml_type == "Configuration")
                {
                    auto xml_datagram =
                        std::get<datagrams::xml_datagrams::XML_Configuration>(xml.decode());

                    _configuration_interface->add_datagram_info(datagram_info);
                }
                else if (xml_type == "Environment")
                {
                    _environment_interface->add_datagram_info(datagram_info);
                }
                else
                {
                    _otherdata_interface->add_datagram_info(datagram_info);
                }

                break;
            }
            case t_SimradDatagramIdentifier::RAW3: {
                auto ping = std::make_shared<SimradPing<t_ifstream>>(
                    datagram_info, datagrams::RAW3::from_stream(ifs, header, true));

                if (!ifs.good())
                    break;

                ping->raw().add_parameter(
                    _packet_buffer.channel_parameters_per_channel_id[ping->get_channel_id()]);

                _ping_container.add_ping(ping);
                _ping_container_by_channel.at(ping->get_channel_id())->add_ping(ping);

                _ping_interface->add_datagram_info(datagram_info);
                break;
            }
            case t_SimradDatagramIdentifier::FIL1: {
                auto datagram = datagrams::FIL1::from_stream(ifs, header);

                if (!ifs.good())
                    break;

                _configuration_interface->add_datagram_info(datagram_info);
                break;
            }
            case t_SimradDatagramIdentifier::TAG0: {
                auto datagram = datagrams::TAG0::from_stream(ifs, header);

                if (!ifs.good())
                    break;

                _annotation_interface->add_datagram_info(datagram_info);
                break;
            }
            default: {
                _otherdata_interface->add_datagram_info(datagram_info);
                header.skip(ifs);
                break;
            }
        }
        return datagram_info;
    }

  public:
    // ----- objectprinter -----
    tools::classhelper::ObjectPrinter __printer__(unsigned int float_precision) const
    {
        tools::classhelper::ObjectPrinter printer("FileSimradRaw", float_precision);

        auto interface_printer = t_base::__printer__(float_precision);

        printer.append(interface_printer);

        printer.register_section("Detected Pings");
        printer.append(_ping_container.__printer__(float_precision), false, '^');
        // printer.register_value("Detected Pings", _ping_container.size(), "RAW3");

        return printer;
    }

  public:
    // -- class helper function macros --
    // define info_string and print functions (needs the __printer__ function)
    __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__
};

} // namespace simrad
} // namespace echosounders
} // namespace themachinethatgoesping
