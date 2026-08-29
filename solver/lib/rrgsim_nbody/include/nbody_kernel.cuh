#pragma once
#include <cuda_runtime.h>

#include <co_device_utils.cuh>
#include <co_device_structs.cuh>

#include <cuda/std/algorithm>

namespace rrgsim::nbody {
	using rrgsim::common::BLOCK_SIZE;
	using rrgsim::common::params_;
	using rrgsim::common::cube;
	using rrgsim::common::dot;

//-----Force_Nbody kernel--------
__global__ void acceleration_kernel(
	double3* acc,
	const double3* pos_i,
	const double3* pos_j,
	const double* mass_j, // G * m_j
	const double* eps2_j
)
{
	__shared__ double3 pos_other[BLOCK_SIZE];
	__shared__ double mass_other[BLOCK_SIZE];
	__shared__ double eps2_other[BLOCK_SIZE];
	cuda::std::memset(pos_other, 0, sizeof(double3) * BLOCK_SIZE);
	cuda::std::memset(mass_other, 0, sizeof(double) * BLOCK_SIZE);
	cuda::std::memset(eps2_other, 0, sizeof(double) * BLOCK_SIZE);

	double3 f_sum = make_double3(0.0, 0.0, 0.0);
	int i_curr_global = threadIdx.x + blockIdx.x * blockDim.x;

	double3 p_curr;
	double eps2_curr;
	if (i_curr_global < params_.ntotal) {
		p_curr = pos_i[i_curr_global];
		eps2_curr = eps2_j[i_curr_global];
	}
	else {
		p_curr = make_double3(0., 0., 0.);
		eps2_curr = 0.;
	}

	for (int block = 0; block < gridDim.x; block++) {
		int i_other_global = threadIdx.x + block * blockDim.x;
		if (i_other_global < params_.ntotal) {
			pos_other[threadIdx.x] = pos_j[i_other_global];
			mass_other[threadIdx.x] = mass_j[i_other_global];
			eps2_other[threadIdx.x] = eps2_j[i_other_global];
		}

		__syncthreads();

		for (int i_other_local = 0; i_other_local < blockDim.x; ++i_other_local) {
			double3 dp = make_double3(
				pos_other[i_other_local].x - p_curr.x,
				pos_other[i_other_local].y - p_curr.y,
				pos_other[i_other_local].z - p_curr.z
			);
			double denominator = sqrt(
				dot(dp, dp) +
				0.5 * (eps2_curr + eps2_other[i_other_local])
			);
			double k = mass_other[i_other_local] / cube(denominator);
			f_sum.x += dp.x * k;
			f_sum.y += dp.y * k;
			f_sum.z += dp.z * k;
		}

		__syncthreads();

	}

	if (i_curr_global < params_.ntotal) {
		acc[i_curr_global] = make_double3(
			acc[i_curr_global].x + f_sum.x,
			acc[i_curr_global].y + f_sum.y,
			acc[i_curr_global].z + f_sum.z
		);
	}
}

/// @brief Шаг по координате
/// @param acc Ускорение (a_{i})
/// @param vel Скорость (v_{i})
/// @param [in, out] pos Координата (p_{i} -> p_{i+1})
/// @param vel_predict Предположение по скорости (v_{i+1}^{*})
/// @param dt Шаг по времени
__global__ void predict_step(
	const double3* acc,
	const double3* vel,
	double3* pos,
	double3* vel_predict,
	double dt
)
{
	const int i = threadIdx.x + blockIdx.x * blockDim.x;
	if (i >= params_.ntotal) {
		return;
	}

	const double3 v = vel[i];
	const double3 r = pos[i];
	const double3 a = acc[i];

	// v_{i+1}^{*} = v_{i} + dt * a_{i}
	vel_predict[i] = make_double3(
		v.x + dt * a.x,
		v.y + dt * a.y,
		v.z + dt * a.z
	);

	// p_{i+1} = p_{i} + dt * 0.5(v_{i} + v_{i+1}^{*})
	pos[i] = make_double3(
		r.x + dt * 0.5 * (v.x + vel_predict[i].x),
		r.y + dt * 0.5 * (v.y + vel_predict[i].y),
		r.z + dt * 0.5 * (v.z + vel_predict[i].z)
	);
}

/// @brief Уточнение скорости
/// @param acc_new Ускорение в новой точке (a_{i+1})
/// @param vel Скорость (v_{i} -> v_{i+1})
/// @param vel_predict Предположение по скорости (v_{i+1}^{*})
/// @param dt Шаг по времени
__global__ void correct_step(
	const double3* acc_new,
	double3* vel,
	const double3* vel_predict,
	double dt
)
{
	const int i = threadIdx.x + blockIdx.x * blockDim.x;
	if (i >= params_.ntotal) {
		return;
	}

	const double3 v = vel[i];
	const double3 vv = vel_predict[i];
	const double3 aa = acc_new[i];

	// v_{i+1} = 0.5 * (v_i + v_{i+1}^{*}) + 0.5 * dt * a_{i+1}
	vel[i] = make_double3(
		0.5 * (v.x + vv.x + dt * aa.x),
		0.5 * (v.y + vv.y + dt * aa.y),
		0.5 * (v.z + vv.z + dt * aa.z)
	);
}


} // namespace rrgsim::nbody