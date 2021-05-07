/*****************************************************************************
 * Copyright (c) 2014-2021 OpenRCT2 developers
 *
 * For a complete list of all authors, please refer to contributors.md
 * Interested in contributing? Visit https://github.com/OpenRCT2/OpenRCT2
 *
 * OpenRCT2 is licensed under the GNU General Public License version 3.
 *****************************************************************************/

#include "../common.h"
#include "../core/Guard.hpp"
#include "Drawing.h"

#if defined(__ARM_NEON__) || defined(__ARM_NEON)

#    include <arm_neon.h>

void mask_neon(
    int32_t width, int32_t height, const uint8_t* RESTRICT maskSrc, const uint8_t* RESTRICT colourSrc, uint8_t* RESTRICT dst,
    int32_t maskWrap, int32_t colourWrap, int32_t dstWrap)
{
    if (width == 32)
    {
        const uint8x16_t zero128 = {};
        for (int32_t yy = 0; yy < height; yy++)
        {
            int32_t colourStep = yy * (colourWrap + 32);
            int32_t maskStep = yy * (maskWrap + 32);
            int32_t dstStep = yy * (dstWrap + 32);

            // first half
            const uint8x16_t colour1 = vld1q_u8(reinterpret_cast<const uint8_t*>(colourSrc + colourStep));
            const uint8x16_t mask1 = vld1q_u8(reinterpret_cast<const uint8_t*>(maskSrc + maskStep));
            const uint8x16_t dest1 = vld1q_u8(reinterpret_cast<const uint8_t*>(dst + dstStep));
            const uint8x16_t mc1 = vandq_u8(colour1, mask1);
            const uint8x16_t saturate1 = vceqq_u8(mc1, zero128);
            // blended = (for each bit) if saturate1 then dest1 else mc1
            const uint8x16_t blended1 = vbslq_u8(saturate1, dest1, mc1);

            // second half
            const uint8x16_t colour2 = vld1q_u8(reinterpret_cast<const uint8_t*>(colourSrc + 16 + colourStep));
            const uint8x16_t mask2 = vld1q_u8(reinterpret_cast<const uint8_t*>(maskSrc + 16 + maskStep));
            const uint8x16_t dest2 = vld1q_u8(reinterpret_cast<const uint8_t*>(dst + 16 + dstStep));
            const uint8x16_t mc2 = vandq_u8(colour2, mask2);
            const uint8x16_t saturate2 = vceqq_u8(mc2, zero128);
            // blended = (for each bit) if saturate1 then dest1 else mc1
            const uint8x16_t blended2 = vbslq_u8(saturate2, dest2, mc2);

            vst1q_u8(reinterpret_cast<uint8_t*>(dst + dstStep), blended1);
            vst1q_u8(reinterpret_cast<uint8_t*>(dst + 16 + dstStep), blended2);
        }
    }
    else
    {
        mask_scalar(width, height, maskSrc, colourSrc, dst, maskWrap, colourWrap, dstWrap);
    }
}

#else

#    if defined(OPENRCT2_ARM) || defined(OPENRCT2_AARCH64)
#        error You have to compile this file with NEON enabled, when targeting ARM!
#    endif

void mask_neon(
    int32_t width, int32_t height, const uint8_t* RESTRICT maskSrc, const uint8_t* RESTRICT colourSrc, uint8_t* RESTRICT dst,
    int32_t maskWrap, int32_t colourWrap, int32_t dstWrap)
{
    openrct2_assert(false, "ARM NEON function called on a CPU that doesn't support NEON");
}

#endif // defined(__ARM_NEON__) || defined(__ARM_NEON)
