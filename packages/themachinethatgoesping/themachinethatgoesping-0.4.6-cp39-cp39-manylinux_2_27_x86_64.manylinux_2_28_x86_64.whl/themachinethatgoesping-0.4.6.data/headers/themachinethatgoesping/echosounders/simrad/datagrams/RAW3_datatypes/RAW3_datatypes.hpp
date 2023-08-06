// SPDX-FileCopyrightText: 2022 Tim Weiß, GEOMAR Helmholtz Centre for Ocean Research Kiel
// SPDX-FileCopyrightText: 2022 Peter Urban, GEOMAR Helmholtz Centre for Ocean Research Kiel
// SPDX-FileCopyrightText: 2022 Peter Urban, Ghent University
//
// SPDX-License-Identifier: MPL-2.0

#pragma once

// std includes
#include <variant>

// themachinethatgoesping import
#include <themachinethatgoesping/tools/helper.hpp>

#include "RAW3_dataangle.hpp"
#include "RAW3_datapower.hpp"
#include "RAW3_datapowerandangle.hpp"
#include "RAW3_dataskipped.hpp"
#include "i_RAW3_data.hpp"
#include "t_RAW3_datatype.hpp"
// #include "RAW3_datacomplexfloat16.hpp"
#include "RAW3_datacomplexfloat32.hpp"

namespace themachinethatgoesping {
namespace echosounders {
namespace simrad {
namespace datagrams {
namespace RAW3_datatypes {

using RAW3_DataVariant = std::variant<RAW3_DataSkipped,
                                      RAW3_DataComplexFloat32,
                                      RAW3_DataPowerAndAngle,
                                      RAW3_DataPower,
                                      RAW3_DataAngle>;

}
}
}
}
}