#pragma once

#include <arbor/export.hpp>

namespace arb {
ARB_ARBOR_API extern const char* source_id;
ARB_ARBOR_API extern const char* arch;
ARB_ARBOR_API extern const char* build_config;
ARB_ARBOR_API extern const char* version;
ARB_ARBOR_API extern const char* full_build_id;
constexpr int version_major = 0;
constexpr int version_minor = 8;
constexpr int version_patch = 0;
ARB_ARBOR_API extern const char* version_dev;
}

#define ARB_SOURCE_ID "2022-11-15T16:19:19+01:00 8e82ec1947a3a6d84452969d1d628b2292654319"
#define ARB_ARCH "none"
#define ARB_BUILD_CONFIG "RELEASE"
#define ARB_FULL_BUILD_ID "source_id=2022-11-15T16:19:19+01:00 8e82ec1947a3a6d84452969d1d628b2292654319;version=0.8.0;arch=none;config=RELEASE;NEUROML_ENABLED;BUNDLED_ENABLED;"
#define ARB_VERSION "0.8.0"
#define ARB_VERSION_MAJOR 0
#define ARB_VERSION_MINOR 8
#define ARB_VERSION_PATCH 0
#ifndef ARB_NEUROML_ENABLED
#define ARB_NEUROML_ENABLED
#endif
#ifndef ARB_BUNDLED_ENABLED
#define ARB_BUNDLED_ENABLED
#endif
