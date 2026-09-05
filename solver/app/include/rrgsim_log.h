#pragma once
#include <spdlog/spdlog.h>
#include <filesystem>

namespace rrgsim::log {

    inline std::filesystem::path WORKING_DIR;
    void setup_logging(const std::filesystem::path& working_dir);


} // namespace rrgsim::log