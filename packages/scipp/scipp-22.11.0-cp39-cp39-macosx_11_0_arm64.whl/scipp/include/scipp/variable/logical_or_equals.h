// SPDX-License-Identifier: BSD-3-Clause
// Copyright (c) 2022 Scipp contributors (https://github.com/scipp)
/// @file
/// @author Simon Heybrock
#pragma once

#include "scipp-variable_export.h"
#include "scipp/variable/variable.h"

namespace scipp::variable {

SCIPP_VARIABLE_EXPORT Variable &operator|=(Variable &lhs, const Variable &rhs);
SCIPP_VARIABLE_EXPORT Variable operator|=(Variable &&lhs, const Variable &rhs);

} // namespace scipp::variable
