#include "nbody_kernel.cuh"
#include "nbody.h"
#include <spdlog/spdlog.h>

namespace rrgsim::nbody {

tl::expected<sContext, std::string>
initialize(
    const common::ParticlesData& particles_data
)
{
    spdlog::info("Initialize NBody context");

    try {
        sContext context = std::make_shared<Context>();
        context->pos_ = particles_data.pos;
        context->vel_ = particles_data.vel;
        context->mass_ = particles_data.mass;
        context->soft2_ = particles_data.soft2;

        const size_t N = particles_data.params.ntotal;

        context->acc_ = CuDarray<double3>(N);
        context->vel_predicted_ = CuDarray<double3>(N);
        context->grav_ = CuDarray<double>(N);

        context->common_params = particles_data.params;
        RR::CUDA::CuCopyToSymbol(context->common_params, rrgsim::common::params_, RR::CUDA::ToDevice);

        return context;
    }
    catch(const std::exception& ex) {
        return tl::make_unexpected(ex.what());
    }
}

void predict_step(
    sContext context,
    const SimParams& sim_params
)
{
    spdlog::debug("NBody::predict_step (t={})", context->time);

    int blocks_count = calc_blocks_count(context->common_params.ntotal);
    RR::CUDA::CuCall(predict_step_, blocks_count, BLOCK_SIZE) (
        context->acc_,
        context->vel_,
        context->pos_,
        context->vel_predicted_,
        sim_params.dt_dynamics
    );
}

void nbody_acceleration(
    sContext context,
    const SimParams& sim_params
)
{
    spdlog::debug("NBody::acceleration (t={})", context->time);

    int blocks_count = calc_blocks_count(context->common_params.ntotal);
    RR::CUDA::CuCall(acceleration_kernel_blocked_, blocks_count, BLOCK_SIZE) (
        context->acc_,
        context->pos_,
        context->mass_,
        context->soft2_
    );
}

void nbody_grav(
    sContext context,
    const SimParams& sim_params
)
{
    spdlog::debug("NBody::grav (t={})", context->time);

    int blocks_count = calc_blocks_count(context->common_params.ntotal);
    RR::CUDA::CuCall(grav_kernel_blocked_, blocks_count, BLOCK_SIZE) (
        context->grav_,
        context->pos_,
        context->mass_,
        context->soft2_
    );
}

void correct_step(
    sContext context,
    const SimParams& sim_params
)
{
    spdlog::debug("NBody::correct_step (t={})", context->time);

    int blocks_count = calc_blocks_count(context->common_params.ntotal);
    RR::CUDA::CuCall(correct_step_, blocks_count, BLOCK_SIZE) (
        context->acc_,
        context->vel_,
        context->vel_predicted_,
        sim_params.dt_dynamics
    );
}

ConservationInfo calc_conservation(
    sHostContext host_context
)
{
    spdlog::info("NBody::conservation");
    const auto& pos = host_context->pos;
    const auto& vel = host_context->vel;
    const auto& mass = host_context->mass;
    const auto& grav = host_context->grav;
    if (vel.size() != mass.size()) {
        throw std::runtime_error("Conservation calculation error: velocity and mass arrays size mismatch");
    }
    const size_t N = vel.size();

    ConservationInfo info;
    info.momentum = double3(0., 0., 0.);
    info.angular = double3(0., 0., 0.);
    info.Ek = 0;
    info.Ep = 0;

    for (size_t i = 0; i < N; ++i) {
        const double x = pos[i].x;
        const double y = pos[i].y;
        const double z = pos[i].z;
        const double m = mass[i];
        const double vx = vel[i].x;
        const double vy = vel[i].y;
        const double vz = vel[i].z;

        info.momentum.x += m * vx;
        info.momentum.y += m * vy;
        info.momentum.z += m * vz;

        info.angular.x += m * (vz * y - vy * z);
        info.angular.y += m * (vx * z - vz * x);
        info.angular.z += m * (vy * x - vx * y);

        info.Ek += m * (vx * vx + vy * vy + vz * vz);
        info.Ep += m * grav[i];
    }

    info.Ek *= 0.5;
    info.Ep *= 0.5;
    info.time = host_context->time;
    return info;
}

} // namespace rrgsim::nbody