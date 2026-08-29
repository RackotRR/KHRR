#pragma once
#include <string>
#include <filesystem>

#include <nlohmann/json.hpp>
#include <tl/expected.hpp>

#include <co_params.cuh>

namespace rrgsim::common {
    void to_json(nlohmann::json& j, const SimParams& sim_params);
    void from_json(const nlohmann::json& j, SimParams& sim_params);
}

namespace rrgsim::io {

    tl::expected<rrgsim::common::SimParams, std::string>
    read_sim_params(
        const std::filesystem::path& sim_json_path
    );

} // namespace rrgsim::io