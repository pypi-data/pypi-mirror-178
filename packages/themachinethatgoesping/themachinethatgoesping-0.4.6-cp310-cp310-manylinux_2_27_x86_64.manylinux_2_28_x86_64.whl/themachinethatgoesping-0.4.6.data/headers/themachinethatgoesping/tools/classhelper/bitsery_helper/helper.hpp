// SPDX-FileCopyrightText: 2022 Peter Urban, Ghent University
//
// SPDX-License-Identifier: MPL-2.0
#pragma once

// include bitsery
#include <bitsery/bitsery.h>

// helper defines
#define SERIALIZER_DEFAULT_MAX_CONTAINER_SIZE 1000000

// distinguish between input and output serializer
// typically writing an extension should be more save? But I don't entirly understand the bitsery
// extension stuff
namespace themachinethatgoesping {
namespace tools {
namespace bitsery_helper {

template<typename T>
inline constexpr bool is_input([[maybe_unused]] bitsery::Serializer<T>& S)
{
    return false;
}

template<typename T>
inline constexpr bool is_input([[maybe_unused]] bitsery::Deserializer<T>& S)
{
    return true;
}

}
}
}
