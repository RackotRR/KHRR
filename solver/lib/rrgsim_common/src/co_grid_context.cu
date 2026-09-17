#include "co_grid_context.h"

namespace rrgsim::common {

void GridContext::fill_device_data(
    const sGridContext_ context_
)
{
    context_->grav_curr_.to_vector(this->grav);
    context_->mass_.to_vector(this->mass);
}

sGridContext_
initialize_grid_context_(
    GridInfo grid_info
)
{
    return nullptr;
}

sGridContext
initialize_grid_context(
    GridInfo grid_info
)
{
    return nullptr;
}

} // namespace rrgsim::common