#pragma once

namespace rrgsim::common {

constexpr int BLOCK_SIZE = 256;

struct CommonParams {
    int ntotal = 0;
};

__constant__ CommonParams params_;

} // namespace rrgsim::common