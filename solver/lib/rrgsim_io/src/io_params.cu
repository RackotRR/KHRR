#include <fstream>
#include <spdlog/spdlog.h>
#include "io_params.cuh"


namespace rrgsim::common {
    void to_json(nlohmann::json& j, const SimParams& sim_params) {
        j["time_max"] = sim_params.time_max;
        j["dt_save"] = sim_params.dt_save;
        j["dt_dynamics"] = sim_params.dt_dynamics;
    }
    void from_json(const nlohmann::json& j, SimParams& sim_params) {
        j.at("time_max").get_to(sim_params.time_max);
        j.at("dt_save").get_to(sim_params.dt_save);
        j.at("dt_dynamics").get_to(sim_params.dt_dynamics);
    }
} // namespace rrgsim::common

namespace rrgsim::io {

    tl::expected<rrgsim::common::SimParams, std::string>
    read_sim_params(
        const std::filesystem::path& sim_json_path
    )
    {
        spdlog::info("Read sim params from {}", sim_json_path.string());

        try {
            std::ifstream stream{ sim_json_path };
            nlohmann::json j; stream >> j;

            auto sim_params = j.get<rrgsim::common::SimParams>();
            spdlog::info("Target simulation time: {:.10f}", sim_params.time_max);

            return sim_params;
        }
        catch(const std::exception& ex) {
            return tl::make_unexpected(
                fmt::format("Can't read sim params: {}", ex.what())
            );
        }
    }

} // namespace rrgsim::io