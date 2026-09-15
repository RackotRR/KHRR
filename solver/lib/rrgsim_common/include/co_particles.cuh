#pragma once
#include "cuda_runtime.h"
#include <vector>
#include "co_device_structs.cuh"

namespace rrgsim::common {

    struct ParticlesData {
        std::vector<double3> pos;
        std::vector<double3> vel;
        std::vector<double> mass;
        std::vector<double> soft2;

        ParticlesInfo info;
    };

} // rrgsim::common