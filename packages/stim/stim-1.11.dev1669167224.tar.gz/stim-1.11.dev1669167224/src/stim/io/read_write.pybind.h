// Copyright 2021 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#ifndef _STIM_IO_READ_WRITE_PYBIND_H
#define _STIM_IO_READ_WRITE_PYBIND_H

#include <cstddef>
#include <pybind11/pybind11.h>

#include "stim/mem/simd_bit_table.h"

namespace stim_pybind {

void pybind_read_write(pybind11::module &m);

}  // namespace stim_pybind

#endif