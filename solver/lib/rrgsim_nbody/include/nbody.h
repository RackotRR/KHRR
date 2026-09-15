#pragma once
#include <co_params.cuh>
#include <co_device_structs.cuh>
#include <co_particles_context.h>

namespace rrgsim::nbody {
    using RR::CUDA::CuDarray;
    using common::CommonParams;
    using common::BLOCK_SIZE;
    using common::SimParams;
    using common::sContext;
    using common::sHostContext;

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