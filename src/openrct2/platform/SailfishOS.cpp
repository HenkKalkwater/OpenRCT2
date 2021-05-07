/*****************************************************************************
 * Copyright (c) 2014-2020 OpenRCT2 developers
 *
 * For a complete list of all authors, please refer to contributors.md
 * Interested in contributing? Visit https://github.com/OpenRCT2/OpenRCT2
 *
 * OpenRCT2 is licensed under the GNU General Public License version 3.
 *****************************************************************************/

#ifdef __SAILFISHOS__
#include "platform.h"

float platform_get_default_scale()
{
    return 2.5;
}

int platform_get_default_fullsreen_mode()
{
    return 1;
}

DrawingEngine platform_get_default_drawing_engine()
{
    return DrawingEngine::SoftwareWithHardwareDisplay;
}

#endif //__SAILFISHOS__
