#pragma once
#include "io_particles.h"

#include "co_sim_params.h"
#include "co_device_structs.cuh"

#include <nlohmann/json.hpp>
#include <rrgsim_tl.h>

namespace rrgsim::common {
    void to_json(nlohmann::json& j, const SimParams& sim_params);
    void from_json(const nlohmann::json& j, SimParams& sim_params);

    void to_json(nlohmann::json& j, const GridInfo& grid_info);
    void from_json(const nlohmann::json& j, GridInfo& grid_info);
}

namespace rrgsim::io {
    struct ParsedParams {
        IniGalaxyData galaxy_data;
        common::SimParams sim_params;
        tl::optional<common::GridInfo> mb_grid_info;
    };

    void to_json(nlohmann::json& j, const IniGalaxyData& galaxy_data);
    void from_json(const nlohmann::json& j, IniGalaxyData& galaxy_data);

    tl::expected<ParsedParams, std::string>
    parse_params_json(const std::filesystem::path& path);
} // namespace rrgsim::io