// SPDX-License-Identifier: BSD-3-Clause
// Copyright (c) 2022 Scipp contributors (https://github.com/scipp)
/// @file
/// @author Simon Heybrock
#pragma once

#include "scipp/dataset/dataset.h"

namespace scipp::dataset {

[[nodiscard]] SCIPP_DATASET_EXPORT DataArray
erfc(const DataArray &a);

[[nodiscard]] SCIPP_DATASET_EXPORT Dataset
erfc(const Dataset &ds);

} // namespace scipp::dataset
