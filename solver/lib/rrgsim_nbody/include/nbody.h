#pragma once
#include <co_particles.cuh>
#include <co_params.cuh>
#include <co_device_structs.cuh>

#include <memory>
#include <vector>

#include <rrgsim_tl.h>

#include <RR/CUDA/CuCommon.cuh>

namespace rrgsim::nbody {
    using RR::CUDA::CuDarray;
    using common::CommonParams;
    using common::BLOCK_SIZE;
    using common::SimParams;

    // контекст расчёта на GPU
    struct Context {
        double time = 0.; // current time

        CuDarray<double3> pos_; // particles position (GPU)
        CuDarray<double3> vel_; // particles velocity (GPU)
        CuDarray<double3> vel_predicted_; // particles velocity predicted (GPU)
        CuDarray<double3> acc_; // particles acceleration (GPU)
        CuDarray<double> mass_; // particles masses (GPU)
        CuDarray<double> soft2_; // particles softening squared (GPU)
        CuDarray<double> grav_; // particles gravitational potential (GPU)

        CommonParams common_params;
    };
    using sContext = std::shared_ptr<Context>;

    // контекст для пост-процессинга на CPU (данные, которые копируются с шагом dt_save)
    struct HostContext {
        double time = 0.;
        std::vector<double3> pos;
        std::vector<double3> vel;
        std::vector<double> mass;
        std::vector<double> grav;
    };
    using sHostContext = std::shared_ptr<HostContext>;

    tl::expected<sContext, std::string>
    initialize(
        const common::ParticlesData& particles_data
    );

    struct ConservationInfo {
        double time = 0;
        double Ek = 0;
        double Ep = 0;
        double3 momentum = make_double3(0., 0., 0.);
        double3 angular = make_double3(0., 0., 0.);

        double E() const {
            return Ek + Ep;
        }
    };

    ConservationInfo calc_conservation(
        sHostContext host_context
    );

    void predict_step(
        sContext context,
        const SimParams& sim_params
    );

    void nbody_acceleration(
        sContext context,
        const SimParams& sim_params
    );

    void nbody_grav(
        sContext context,
        const SimParams& sim_params
    );

    void correct_step(
        sContext context,
        const SimParams& sim_params
    );

    inline int calc_blocks_count(int ntotal) {
        return (ntotal + BLOCK_SIZE - 1) / BLOCK_SIZE;
    }

} // namespace rrgsim::nbody