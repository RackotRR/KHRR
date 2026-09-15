#include "co_particles_context.h"

#include <spdlog/spdlog.h>

namespace rrgsim::common {

tl::expected<sContext, std::string>
initialize_particles_context(
    const common::ParticlesData& particles_data
)
{
    spdlog::info("Initialize particles context");

    try {
        sContext context = std::make_shared<Context>();
        context->pos_ = particles_data.pos;
        context->vel_ = particles_data.vel;
        context->mass_ = particles_data.mass;
        context->soft2_ = particles_data.soft2;

        const size_t N = particles_data.params.ntotal;

        context->acc_ = CuDarray<double3>(N);
        context->vel_predicted_ = CuDarray<double3>(N);
        context->grav_ = CuDarray<double>(N);

        context->common_params = particles_data.params;
        RR::CUDA::CuCopyToSymbol(context->common_params, rrgsim::common::params_, RR::CUDA::ToDevice);

        return context;
    }
    catch(const std::exception& ex) {
        return tl::make_unexpected(ex.what());
    }
}

} // namespace rrgsim::common