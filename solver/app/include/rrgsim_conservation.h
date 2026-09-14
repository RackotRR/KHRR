#pragma once
#include <nbody.h>
#include <filesystem>

namespace rrgsim::conservation {

void print_conservation(
    const rrgsim::nbody::ConservationInfo& info
);

void print_conservation(
    const rrgsim::nbody::ConservationInfo& info0,
    const rrgsim::nbody::ConservationInfo& info
);

} // namespace rrgsim::conservation