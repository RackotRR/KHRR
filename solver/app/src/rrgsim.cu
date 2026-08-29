#include <co_params.cuh>
#include <co_particles.cuh>

#include "io_particles.cuh"
#include "io_params.cuh"

#include "rrgsim_log.h"


int main(int argc, const char** argv) {
    if (argc < 2) {
        return 999;
    }
    else if (argc < 3) {
        const char* work_dir = argv[1];
        std::filesystem::path work_dir_path = work_dir;

        rrgsim::log::setup_logging(work_dir_path);

        std::filesystem::path ini_path = work_dir_path / "ini.json";
        auto expected_particles_data = rrgsim::io::read_simple_particles_data(ini_path);
        if (false == expected_particles_data.has_value()) {
            spdlog::error("Error: {}", expected_particles_data.error());
            return 0;
        }

        std::filesystem::path sim_params_path = work_dir_path / "sim.json";
        auto expected_sim_params = rrgsim::io::read_sim_params(sim_params_path);
        if (false == expected_sim_params.has_value()) {
            spdlog::error("Error: {}", expected_sim_params.error());
            return 0;
        }
    }

    return 0;
}