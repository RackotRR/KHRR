#include <co_params.cuh>
#include <co_particles.cuh>
#include <co_device_utils.cuh>

#include "io_particles.cuh"
#include "io_params.cuh"

#include <fstream>

#include "rrgsim_log.h"
#include "nbody.cuh"

void print_conservation(
    const rrgsim::nbody::ConservationInfo& info
)
{
    spdlog::info("-- momentum:");
    spdlog::info("\t x {}", info.momentum.x);
    spdlog::info("\t y {}", info.momentum.y);
    spdlog::info("\t z {}", info.momentum.z);

    spdlog::info("-- angular momentum:");
    spdlog::info("\t x {}", info.angular.x);
    spdlog::info("\t y {}", info.angular.y);
    spdlog::info("\t z {}", info.angular.z);

    spdlog::info("-- energy: {}", info.E());
    spdlog::info("\t keenetic {}", info.Ek);
    spdlog::info("\t potential {}", info.Ep);
}
void print_conservation(
    const rrgsim::nbody::ConservationInfo& info0,
    const rrgsim::nbody::ConservationInfo& info
)
{
    using rrgsim::common::distance;
    using rrgsim::common::norm;

    double momentum_diff = distance(
        info.momentum,
        info0.momentum
    );
    double angular_momentum_diff = distance(
        info.angular,
        info0.angular
    );

    spdlog::info(
        "-- momentum: diff {} ; rel {}",
        momentum_diff,
        norm(info.momentum) / norm(info.momentum) - 1.
    );
    spdlog::trace(
        "\t {} -> {}",
        info0.momentum.x,
        info.momentum.x
    );
    spdlog::trace(
        "\t {} -> {}",
        info0.momentum.y,
        info.momentum.y
    );
    spdlog::trace(
        "\t {} -> {}",
        info0.momentum.z,
        info.momentum.z
    );

    spdlog::info(
        "-- angular momentum: diff {} ; rel {}",
        angular_momentum_diff,
        norm(info.angular) / norm(info0.angular) - 1.
    );
    spdlog::trace(
        "\t {} -> {}",
        info0.angular.x,
        info.angular.x
    );
    spdlog::trace(
        "\t {} -> {}",
        info0.angular.y,
        info.angular.y
    );
    spdlog::trace(
        "\t {} -> {}",
        info0.angular.z,
        info.angular.z
    );

    spdlog::info(
        "-- energy keenetic: diff {}", info.Ek - info0.Ek
    );
    spdlog::trace(
        "\t {} -> {}",
        info0.Ek,
        info.Ek
    );
    spdlog::info(
        "-- energy potential: diff {}", info.Ep - info0.Ep
    );
    spdlog::trace(
        "\t {} -> {}",
        info0.Ep,
        info.Ep
    );

    double energy_total = info.E();
    double energy_total0 = info0.E();
    spdlog::info(
        "-- energy total: diff {} ; rel {}",
        energy_total - energy_total0,
        energy_total / energy_total0 - 1.
    );
    spdlog::trace(
        "\t {} -> {}",
        energy_total0,
        energy_total
    );
}

void integrate(
    rrgsim::common::ParticlesData particles_data,
    rrgsim::common::SimParams sim_params
) {
    auto expected_context_ = rrgsim::nbody::initialize(particles_data);
    if (false == expected_context_.has_value()) {
        spdlog::error("Initialization error: {}", expected_context_.error());
        return;
    }

    auto context_ = std::move(expected_context_).value();
    auto context = std::make_shared<rrgsim::nbody::HostContext>();
    context->mass = std::move(particles_data.mass);
    context->pos = std::move(particles_data.pos);
    context->vel = std::move(particles_data.vel);
    rrgsim::nbody::nbody_grav(
        context_,
        sim_params
    );
    rrgsim::nbody::nbody_acceleration(
        context_,
        sim_params
    );
    context->grav = context_->grav_.to_vector();
    const auto base_conservation_info = rrgsim::nbody::calc_conservation(context);
    print_conservation(base_conservation_info);

    double time = 0.;
    double next_save = time + sim_params.dt_save;
    while (time < sim_params.time_max) {
        rrgsim::nbody::predict_step(
            context_,
            sim_params
        );

        rrgsim::nbody::nbody_acceleration(
            context_,
            sim_params
        );

        rrgsim::nbody::correct_step(
            context_,
            sim_params
        );

        time += sim_params.dt_dynamics;
        context_->time = time;

        if (time >= next_save) {
            spdlog::info("Time to save: {}", time);

            rrgsim::nbody::nbody_grav(
                context_,
                sim_params
            );

            context_->mass_.to_vector(context->mass);
            context_->vel_.to_vector(context->vel);
            context_->pos_.to_vector(context->pos);
            context_->grav_.to_vector(context->grav);

            print_conservation(
                base_conservation_info,
                rrgsim::nbody::calc_conservation(context)
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