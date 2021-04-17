/*
 * Hash reversal
 *
 * Copyright (c) 2020 Authors:
 *   - Trevor Phillips <trevphil3@gmail.com>
 *
 * All rights reserved.
 *
 * Unauthorized copying of this file, via any medium is strictly prohibited
 * Proprietary and confidential
 */

#pragma once

#include "core/sym_bit_vec.hpp"
#include "core/sym_hash.hpp"
#include "hashing/sym_sha256.hpp"
#include "hashing/sym_ripemd160.hpp"
#include "hashing/sym_md5.hpp"

namespace preimage {

class SameIOHash : public SymHash {
 public:
  SymBitVec hash(const SymBitVec &hash_input, int difficulty) override;
};

class NotHash : public SymHash {
 public:
  SymBitVec hash(const SymBitVec &hash_input, int difficulty) override;
};

class LossyPseudoHash : public SymHash {
 public:
  SymBitVec hash(const SymBitVec &hash_input, int difficulty) override;
};

class NonLossyPseudoHash : public SymHash {
 public:
  SymBitVec hash(const SymBitVec &hash_input, int difficulty) override;
};

}  // end namespace preimage