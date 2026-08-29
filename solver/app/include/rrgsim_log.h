#pragma once
#include <spdlog/spdlog.h>
#include <filesystem>

namespace rrgsim::log {

    void setup_logging(const std::filesystem::path& working_dir);

} // namespace rrgsim::log