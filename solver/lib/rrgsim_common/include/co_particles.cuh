#pragma once
#include "cuda_runtime.h"
#include <vector>

namespace rrgsim::common {

    struct ParticlesData {
        std::vector<double3> pos;
        std::vector<double3> vel;
        std::vector<double> mass;
        std::vector<double> eps2;
    };

} // rrgsim::common