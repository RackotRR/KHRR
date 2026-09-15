#pragma once
#include <limits>

namespace rrgsim::common {

constexpr int BLOCK_SIZE = 256;

struct ParticlesInfo {
    int ntotal = 0;
};

struct GridInfo {
    // Равномерная сетка
    double dx = std::numeric_limits<double>::quiet_NaN();
};

__constant__ ParticlesInfo particles_info_;

__constant__ GridInfo grid_info_;

} // namespace rrgsim::common