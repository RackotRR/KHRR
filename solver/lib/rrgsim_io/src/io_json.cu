#include <fstream>

#include <spdlog/spdlog.h>

#include "io_json.h"

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

    void to_json(nlohmann::json& j, const GridInfo& grid_info) {
        j.at("nx") = grid_info.nx;
        j.at("dx") = grid_info.dx;
        j.at("bc_frac") = 1. - grid_info.sim_l / grid_info.domain_l;
    }
    void from_json(const nlohmann::json& j, GridInfo& grid_info) {
        j.at("nx").get_to(grid_info.nx);
        j.at("dx").get_to(grid_info.dx);

        grid_info.domain_l = grid_info.dx * grid_info.nx;

        double bc_frac = j.at("bc_frac").get<double>();
        grid_info.sim_l = (1. - bc_frac) * grid_info.domain_l;
        grid_info.bc_l = 0.5 * bc_frac * grid_info.domain_l;
    }
} // namespace rrgsim::common

namespace rrgsim::io {
    void to_json(nlohmann::json& j, const IniGalaxyData& galaxy_data) {
        j["mass_star"] = galaxy_data.mass_star;
        j["mass_dark"] = galaxy_data.mass_dark;
        j["soft_star"] = galaxy_data.soft_star;
        j["soft_dark"] = galaxy_data.soft_dark;

        auto path_to_json = [](const fs::path& path) -> nlohmann::json {
            return path.string();
        };
        j["ini_file_star"] = galaxy_data.mb_ini_file_star.map_or(path_to_json, nlohmann::json{ nullptr });
        j["ini_file_dark"] = galaxy_data.mb_ini_file_dark.map_or(path_to_json, nlohmann::json{ nullptr });
    }
    void from_json(const nlohmann::json& j, IniGalaxyData& galaxy_data) {
        j.at("mass_star").get_to(galaxy_data.mass_star);
        j.at("mass_dark").get_to(galaxy_data.mass_dark);
        j.at("soft_star").get_to(galaxy_data.soft_star);
        j.at("soft_dark").get_to(galaxy_data.soft_dark);

        auto json_to_path = [&j](std::string_view key) -> tl::optional<fs::path> {
            if (auto iter = j.find(key); iter != j.end() && !iter->is_null()) {
                return iter->get<std::string>();
            }
            else {
                return tl::nullopt;
            }
        };
        galaxy_data.mb_ini_file_star = json_to_path("ini_file_star");
        galaxy_data.mb_ini_file_dark = json_to_path("ini_file_dark");
    }

    template<typename T>
    bool parse_opt_json_object(
        std::string_view key,
        tl::optional<T>& out_obj,
        const nlohmann::json& json
    )
    {
        if (json.contains(key)) {
            spdlog::debug("Parse {} section", key);
            out_obj = json.at(key).get<T>();
        }
        else {
            spdlog::debug("No {} section", key);
            out_obj = tl::nullopt;
        }

        return true;
    }

    template<typename T>
    bool parse_mandatory_json_object(
        std::string_view key,
        T& out_obj,
        const nlohmann::json& json
    )
    {
        if (json.contains(key)) {
            spdlog::debug("Parse {} section", key);
            out_obj = json.at(key).get<T>();
            return true;
        }
        else {
            spdlog::error("No {} section", key);
            return false;
        }
    }


    tl::expected<ParsedParams, std::string>
    parse_params_json(const std::filesystem::path& path) {
        try {
            std::ifstream stream{ path };
            nlohmann::json json; stream >> json;

            ParsedParams parsed;

            bool succeed =
                parse_opt_json_object(
                    "grid_info",
                    parsed.mb_grid_info,
                    json
                )
                &&
                parse_mandatory_json_object(
                    "sim_params",
                    parsed.sim_params,
                    json
                )
                &&
                parse_mandatory_json_object(
                    "ini_params",
                    parsed.galaxy_data,
                    json
                );

            if (succeed) {
                spdlog::info("Params json parsed successfully");
                return parsed;
            }
            else {
                return tl::make_unexpected(
                    fmt::format("Params json parsing failed")
                );
            }
        }
        catch (const std::exception& ex) {
            return tl::make_unexpected(
                fmt::format("Unexpected error on params json parsing: {}", ex.what())
            );
        }
    }
} // namespace rrgsim::io