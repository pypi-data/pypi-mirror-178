// SPDX-FileCopyrightText: 2022 Peter Urban, GEOMAR Helmholtz Centre for Ocean Research Kiel
// SPDX-FileCopyrightText: 2022 Sven Schorge, GEOMAR Helmholtz Centre for Ocean Research Kiel
// SPDX-FileCopyrightText: 2022 Peter Urban, Ghent University
//
// SPDX-License-Identifier: MPL-2.0
//

#pragma once

// #include "i_datagram.h"
// #include "i_datagramcontent.h"
// #include "i_datagramheader.h"

/* std includes */
#include <filesystem>
#include <fstream>
#include <unordered_map>
#include <vector>

#include <boost/sort/sort.hpp>
#include <fmt/core.h>

/* themachinethatgoesping includes */
#include <themachinethatgoesping/tools/classhelper/objectprinter.hpp>
#include <themachinethatgoesping/tools/progressbars.hpp>

#include "datagram_info_types.hpp"
#include "i_datagramcontainer.hpp"
#include "i_datagraminterface.hpp"
#include "inputfilemanager.hpp"

namespace themachinethatgoesping {
namespace echosounders {
namespace fileinterfaces {

template<typename t_DatagramBase, ///< the datagram base class which should
                                  ///< contain the header and functions
                                  ///< specified in the DatagramBase interface
         typename t_DatagramInterface>
class I_InputFile
{
  public:
    // member types
    using t_DatagramIdentifier = typename t_DatagramInterface::type_DatagramIdentifier;
    using t_ifstream           = typename t_DatagramInterface::type_ifstream;

  protected:
    std::shared_ptr<InputFileManager<t_ifstream>> _input_file_manager =
        std::make_shared<InputFileManager<t_ifstream>>();

    /* datagram container */
    t_DatagramInterface _datagram_interface;

    I_InputFile() = default;

  public:
    I_InputFile(const std::string& file_path, bool show_progress = true)
    {
        append_file(file_path, show_progress);
    }
    I_InputFile(const std::string& file_path, tools::progressbars::I_ProgressBar& progress_bar)
    {
        append_file(file_path, progress_bar);
    }

    I_InputFile(const std::vector<std::string>& file_paths, bool show_progress)
    {
        append_files(file_paths, show_progress);
    }
    I_InputFile(const std::vector<std::string>&     file_paths,
                tools::progressbars::I_ProgressBar& progress_bar)
    {
        append_files(file_paths, progress_bar);
    }

    virtual ~I_InputFile() = default;

    /* access containers */
    const t_DatagramInterface& datagram_interface() const { return _datagram_interface; }

    void append_files(const std::vector<std::string>& file_paths, bool show_progress = true)
    {
        // defaults to no indicator
        tools::progressbars::ProgressBarChooser progress_bar(show_progress);

        // auto pbar = tools::progressbars::ProgressIndicator();
        append_files(file_paths, progress_bar.get());
    }

    void append_files(const std::vector<std::string>&     file_paths,
                      tools::progressbars::I_ProgressBar& progress_bar)
    {
        // get total file size of all files
        size_t total_file_size = 0;
        size_t datagrams_old   = _datagram_interface.size();

        progress_bar.init(0., double(file_paths.size()), "indexing files");
        for (unsigned int i = 0; i < file_paths.size(); ++i)
        {
            progress_bar.set_postfix(fmt::format("get file size {}/{}", i + 1, file_paths.size()));
            total_file_size += std::filesystem::file_size(file_paths[i]);
        }

        progress_bar.init(0, double(total_file_size), "indexing files");
        for (unsigned int i = 0; i < file_paths.size(); ++i)
        {
            // progress_bar.set_postfix with the last 30 characters of the file path
            auto fp = file_paths[i];
            if (fp.size() > 23)
                fp = ".." + fp.substr(fp.size() - 20);

            progress_bar.set_postfix(fmt::format("{} ({}/{})", fp, i + 1, file_paths.size()));

            append_file(file_paths[i], progress_bar);
        }

        progress_bar.close(std::string("Found: ") +
                           std::to_string(_datagram_interface.size() - datagrams_old) +
                           " datagrams in " + std::to_string(file_paths.size()) + " files (" +
                           std::to_string(int(total_file_size / 1024 / 1024)) + "MB)");
    }

    void append_file(const std::string& file_path, bool show_progress = true)
    {

        tools::progressbars::ProgressBarChooser progress_bar(show_progress);

        append_file(file_path, progress_bar.get());
    }

    void append_file(const std::string& file_path, tools::progressbars::I_ProgressBar& progress_bar)
    {
        auto& ifi = _input_file_manager->append_file(file_path);

        // scan for datagram headers
        DataFileInfo file_info = scan_fo_datagrams(
            file_path, _input_file_manager->get_file_paths()->size() - 1, ifi, progress_bar);

        _datagram_interface.add_datagram_infos(file_info.datagram_infos);
    }

  protected:
    static void reset_ifstream(t_ifstream& ifs)
    {
        ifs.clear();
        ifs.seekg(0);
    }

    virtual void callback_scan_new_file_begin([[maybe_unused]] const std::string& file_path,
                                              [[maybe_unused]] size_t             file_paths_cnt)
    {
    }
    virtual void callback_scan_new_file_end([[maybe_unused]] const std::string& file_path,
                                            [[maybe_unused]] size_t             file_paths_cnt)
    {
    }
    virtual DatagramInfo_ptr<t_DatagramIdentifier, t_ifstream>
    callback_scan_packet(t_ifstream& ifs, typename t_ifstream::pos_type pos, size_t file_paths_cnt)
    {
        auto header = t_DatagramBase::from_stream(ifs);
        header.skip(ifs);

        auto datagram_info = std::make_shared<DatagramInfo<t_DatagramIdentifier, t_ifstream>>(
            file_paths_cnt,
            pos,
            _input_file_manager,
            header.get_timestamp(),
            header.get_datagram_identifier());
        // datagram_info->file_nr             = file_paths_cnt;
        // datagram_info->file_pos            = pos;
        // datagram_info->timestamp           = header.get_timestamp();
        // datagram_info->datagram_identifier = header.get_datagram_identifier();
        return datagram_info;
    }

    // This function must be called at initialization!
    virtual DataFileInfo<t_DatagramIdentifier, t_ifstream> scan_fo_datagrams(
        const std::string&                  file_path,
        size_t                              file_paths_cnt,
        t_ifstream&                         ifs,
        tools::progressbars::I_ProgressBar& progress_bar)
    {

        /* Initialize internal structures */
        DataFileInfo<t_DatagramIdentifier, t_ifstream> file_info;
        file_info.datagram_infos.clear();

        reset_ifstream(ifs);
        callback_scan_new_file_begin(file_path, file_paths_cnt);

        file_info.file_size    = std::filesystem::file_size(file_path);
        bool close_progressbar = false; ///< only close the progressbar if it was
                                        ///< initialized within this function
        if (!progress_bar.is_initialized())
        {
            progress_bar.init(0., double(file_info.file_size), "indexing file");
            close_progressbar = true;
        }
        auto pos = ifs.tellg();

        try
        {
            while (pos < signed(file_info.file_size))
            {
                //  this function may return nonsense...
                // auto header = t_DatagramBase::from_stream(ifs);
                // header.skip(ifs);
                // auto header = callback_scan_packet(ifs);
                auto datagram_info = callback_scan_packet(ifs, pos, file_paths_cnt);

                // this function checks if the datagram content is senseful
                if (ifs.good())
                {
                    // update using tick to allow progressbar that was initialized by
                    // append_files to work
                    auto pos_new = ifs.tellg();
                    progress_bar.tick(double(pos_new - pos));

                    file_info.datagram_infos.push_back(datagram_info);

                    pos = pos_new;
                }
                else
                {
                    break;
                }
            }
        }
        catch (std::runtime_error& e)
        {
            std::cerr << "WARNING(InputFile): File read incompletely. ";
            // print last 100 characters of file_path
            if (file_path.size() > 53)
                std::cerr << fmt::format("[...{}]", file_path.substr(file_path.size() - 50))
                          << std::endl;
            else
                std::cerr << fmt::format("[{}]", file_path) << std::endl;
            double percent = 100.0 * pos / file_info.file_size;
            std::cerr << fmt::format("Stopped after {:.2f} % of the file", percent) << std::endl;
            std::cerr << "Error message: " << e.what() << std::endl;
        }

        reset_ifstream(ifs);

        callback_scan_new_file_end(file_path, file_paths_cnt);

        if (close_progressbar)
            progress_bar.close(std::string("Found: ") +
                               std::to_string(file_info.datagram_infos.size()) + " datagrams");

        return file_info;
    }

  public:
    // ----- objectprinter -----
    tools::classhelper::ObjectPrinter __printer__(unsigned int float_precision) const
    {
        tools::classhelper::ObjectPrinter printer("I_InputFile", float_precision);

        printer.register_section("File infos");
        printer.append(_input_file_manager->__printer__(float_precision));

        printer.register_section("Detected datagrams", '^');
        printer.append(_datagram_interface.__printer__(float_precision), true);
        return printer;
    }

    // -- class helper function macros --
    // define info_string and print functions (needs the __printer__ function)
    __CLASSHELPER_DEFAULT_PRINTING_FUNCTIONS__
};

} // namespace fileinterfaces
} // namespace echosounders
} // namespace themachinethatgoesping