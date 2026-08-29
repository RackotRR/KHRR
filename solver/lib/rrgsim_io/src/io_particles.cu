#include <fstream>
#include <nlohmann/json.hpp>
#include <csv.hpp>
#include <fmt/format.h>
#include <spdlog/spdlog.h>

#include "io_particles.cuh"

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


    tl::expected<bool, std::string>
    read_particles_data_component(
        const IniGalaxyComponentData& component_data,
        ParticlesData& particles_data
    )
    {
        spdlog::info("Read particles data with ini path={}", component_data.ini_file.string());

        csv::CSVFormat format;
        format.delimiter(' ');
        format.no_header();
        format.variable_columns(csv::VariableColumnPolicy::KEEP);

        csv::CSVReader reader(component_data.ini_file.string(), format);
        csv::CSVRow row;

        bool succeed = reader.read_row(row);
        if (false == succeed) {
            return tl::make_unexpected("Failed to read ini header");
        }

        size_t ini_N = row[0].get<size_t>();
        double ini_t = row[1].get<double>();
        spdlog::info("Header says: {} particles, time = {:.10f}", ini_N, ini_t);

        size_t prev_N = particles_data.pos.size();
        size_t N = prev_N + ini_N;
        particles_data.pos.reserve(N);
        particles_data.vel.reserve(N);
        particles_data.mass.reserve(N);
        particles_data.eps2.reserve(N);
        spdlog::debug("Current array sizes: {}", prev_N);
        spdlog::debug("New data size: {}", ini_N);
        spdlog::debug("New array sizes: {}", N);

        auto& pos = particles_data.pos;
        auto& vel = particles_data.vel;
        auto& mass = particles_data.mass;
        auto& eps2 = particles_data.eps2;

        while (reader.read_row(row)) {
            pos.push_back(
                make_double3(
                    row[0].get<double>(),
                    row[1].get<double>(),
                    row[2].get<double>()
                )
            );

            vel.push_back(
                make_double3(
                    row[3].get<double>(),
                    row[4].get<double>(),
                    row[5].get<double>()
                )
            );

            mass.push_back(component_data.mass);
            eps2.push_back(component_data.soft);

            if (pos.size() % 100'000 == 0) {
                spdlog::info("Read {}/{} row", pos.size(), N);
            }
        }

        if (pos.size() != N) {
            return tl::make_unexpected(
                fmt::format("Rows header/file mismatch ({}/{})", N, pos.size())
            );
        }

        return true;
    }

    tl::expected<ParticlesData, std::string>
    read_simple_particles_data(
        const fs::path& ini_json_path
    )
    {
        spdlog::info("Read particles data. Ini json path: {}", ini_json_path.string());

        try {
            std::ifstream stream{ ini_json_path };
            nlohmann::json ini_json; stream >> ini_json;

            const IniGalaxyData ini_galaxy_data = ini_json.get<IniGalaxyData>();

            ParticlesData particles_data;

            if (ini_galaxy_data.mb_ini_file_star) {
                IniGalaxyComponentData component_data;
                component_data.ini_file = ini_galaxy_data.mb_ini_file_star.value();
                component_data.mass = ini_galaxy_data.mass_star;
                component_data.soft = ini_galaxy_data.soft_star;

                auto expected_result = read_particles_data_component(component_data, particles_data);
                EXPECTED_CHECK(expected_result);
            }

            if (ini_galaxy_data.mb_ini_file_dark) {
                IniGalaxyComponentData component_data;
                component_data.ini_file = ini_galaxy_data.mb_ini_file_dark.value();
                component_data.mass = ini_galaxy_data.mass_dark;
                component_data.soft = ini_galaxy_data.soft_dark;

                auto expected_result = read_particles_data_component(component_data, particles_data);
                EXPECTED_CHECK(expected_result);
            }

            spdlog::info("{} particles loaded", particles_data.pos.size());
            return particles_data;
        }
        catch(const std::exception& ex) {
            return tl::make_unexpected(
                fmt::format("Can't read simple particles data: {}", ex.what())
            );
        }
    }

} // namespace rrgsim::io