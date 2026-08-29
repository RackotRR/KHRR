#pragma once
#include <limits>

namespace rrgsim::common {

    constexpr double NAN_VALUE = std::numeric_limits<double>::quiet_NaN();
    struct SimParams {
        double time_max = NAN_VALUE;
        double dt_save = NAN_VALUE;
        double dt_dynamics = NAN_VALUE;
    };


} // namespace rrgsim::common