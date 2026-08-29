#pragma once
#include <vector>
#include <limits>
#include <filesystem>
#include <rrgsim_tl.h>
#include <nlohmann/json.hpp>
#include <cuda_runtime.h>
#include <co_particles.cuh>

namespace rrgsim::io {

    namespace fs = std::filesystem;
    using rrgsim::common::ParticlesData;

    constexpr double NAN_VALUE = std::numeric_limits<double>::quiet_NaN();

    struct IniGalaxyComponentData {
        double mass = NAN_VALUE;
        double soft = NAN_VALUE;
        fs::path ini_file;
    };

    struct IniGalaxyData {
        double mass_star = NAN_VALUE;
        double mass_dark = NAN_VALUE;
        double soft_star = NAN_VALUE;
        double soft_dark = NAN_VALUE;
        tl::optional<fs::path> mb_ini_file_star;
        tl::optional<fs::path> mb_ini_file_dark;
    };

    void to_json(nlohmann::json& j, const IniGalaxyData& galaxy_data);
    void from_json(const nlohmann::json& j, IniGalaxyData& galaxy_data);

    tl::expected<bool, std::string> read_particles_data_component(
        const IniGalaxyComponentData& component_data,
        ParticlesData& particles_data
    );

    tl::expected<ParticlesData, std::string> read_simple_particles_data(
        const fs::path& ini_json_path
    );

} // namespace rrgsim_io