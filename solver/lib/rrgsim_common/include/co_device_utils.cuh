#pragma once
#include <cuda_runtime.h>

namespace rrgsim::common {

template<typename T>
__host__ __device__
double dot(const T& vec1, const T& vec2);

template<>
__host__ __device__
double dot(const double2& vec1, const double2& vec2) {
	return
		vec1.x * vec2.x +
		vec1.y * vec2.y;
}

template<>
__host__ __device__
double dot(const double3& vec1, const double3& vec2) {
	return
		vec1.x * vec2.x +
		vec1.y * vec2.y +
		vec1.z * vec2.z;
}

template<typename T>
__host__ __device__
double norm(const T& vec) {
	return sqrt(dot(vec, vec));
}

template<typename T>
__host__ __device__ T clamp(T val, T min_val, T max_val) {
    if (val < min_val) return min_val;
    if (val > max_val) return max_val;
    return val;
}

inline __host__ __device__
double sqr(double x) {
	return x * x;
}

inline __host__ __device__
double cube(double x) {
	return x * x * x;
}

} // namespace rrgsim::common