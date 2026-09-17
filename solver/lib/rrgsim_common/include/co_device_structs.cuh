#pragma once
#include <limits>

namespace rrgsim::common {

constexpr int BLOCK_SIZE = 256;

struct ParticlesInfo {
    int ntotal;
};

/// @brief Равномерная сетка
struct GridInfo {
    /// @brief Количество ячеек в одном измерении
    int nx;

    /// @brief Шаг по координате
    double dx;

    /// @brief Область моделирования в одном измерении
    double domain_l;

    /// @brief Область граничных условий: domain_l = bc_l + sim_l + bc_l
    double bc_l;

    /// @brief Основная область моделирования
    double sim_l;
};

__constant__ ParticlesInfo particles_info_;

__constant__ GridInfo grid_info_;

} // namespace rrgsim::common