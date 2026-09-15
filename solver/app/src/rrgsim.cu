#include <co_params.cuh>
#include <co_particles.cuh>
#include <co_particles_context.h>
#include <co_device_utils.cuh>

#include "io_particles.h"
#include "io_params.h"
#include "io_handler.h"

#include <fstream>

#include "rrgsim_log.h"
#include "rrgsim_conservation.h"
#include "nbody.h"

void integrate(
    rrgsim::common::ParticlesData particles_data,
    rrgsim::common::SimParams sim_params
) {
    auto expected_context_ = rrgsim::common::initialize_particles_context_(particles_data);
    if (false == expected_context_.has_value()) {
        spdlog::error("Initialization error: {}", expected_context_.error());
        return;
    }

    auto particles_context_ = std::move(expected_context_).value();
    auto particles_context = initialize_particles_context(std::move(particles_data));
    rrgsim::nbody::nbody_grav(
        particles_context_,
        sim_params
    );
    rrgsim::nbody::nbody_acceleration(
        particles_context_,
        sim_params
    );
    particles_context->grav = particles_context_->grav_.to_vector();
    const auto base_conservation_info = rrgsim::nbody::calc_conservation(particles_context);
    rrgsim::conservation::print_conservation(base_conservation_info);

    double time = 0.;
    double next_save = time + sim_params.dt_save;
    while (time < sim_params.time_max) {
        rrgsim::nbody::predict_step(
            particles_context_,
            sim_params
        );

        rrgsim::nbody::nbody_acceleration(
            particles_context_,
            sim_params
        );

        rrgsim::nbody::correct_step(
            particles_context_,
            sim_params
        );

        time += sim_params.dt_dynamics;
        particles_context_->time = time;

        if (time >= next_save) {
            spdlog::info("Time to save: {}", time);

            rrgsim::nbody::nbody_grav(
                particles_context_,
                sim_params
            );

            particles_context->fill_device_data(
                particles_context_
            );

            rrgsim::conservation::print_conservation(
                base_conservation_info,
                rrgsim::nbody::calc_conservation(particles_context)
            );

            next_save += sim_params.dt_save;
        }
    }
}

int main(int argc, const char** argv) {
    if (argc < 2) {
        return 1;
    }
    else if (argc < 3) {
        const char* work_dir = argv[1];
        std::filesystem::path work_dir_path = work_dir;

        rrgsim::log::setup_logging(work_dir_path);
        rrgsim::io::IOHandler::setup(work_dir_path);

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

        try {
            ::integrate(
                std::move(expected_particles_data).value(),
                std::move(expected_sim_params).value()
            );
        }
        catch (const std::exception& ex) {
            spdlog::error("Exception: {}", ex.what());
        }
    }

    return 0;
}