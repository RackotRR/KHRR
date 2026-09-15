#pragma once
#include <RR/CUDA/CuCommon.cuh>

#include <memory>
#include <vector>

#include <rrgsim_tl.h>

#include <co_device_structs.cuh>
#include <co_particles.cuh>

namespace rrgsim::common {
    using RR::CUDA::CuDarray;

    // контекст расчёта на GPU
    struct GridContext_ {
        double time = 0.; // current time

        CuDarray<double> mass_; // cell masses (GPU)
        CuDarray<double> grav_prev_; // cell gravitational potential (GPU)
        CuDarray<double> grav_curr_; // cell gravitational potential (GPU)
        CuDarray<double> grav_next_; // cell gravitational potential (GPU)
        CuDarray<double3> acc_; // acceleration (GPU)

        GridInfo grid_info;
    };
    using sGridContext_ = std::shared_ptr<GridContext_>;

    // контекст для пост-процессинга на CPU (данные, которые копируются с шагом dt_save)
    struct GridContext {
        double time = 0.;
        std::vector<double> mass;
        std::vector<double> grav;
    };
    using sGridContext = std::shared_ptr<GridContext>;


    tl::expected<sGridContext_, std::string>
    initialize_grid_context(
        const common::ParticlesData& particles_data
    );

} // namespace rrgsim::common