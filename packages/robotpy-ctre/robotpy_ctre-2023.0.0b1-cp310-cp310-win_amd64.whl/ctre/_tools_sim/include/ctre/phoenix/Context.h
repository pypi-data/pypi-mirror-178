/*
 * Copyright (c) CTR-Electronics
 * Contact support@ctr-electronics for any questions
 * including support, features, and licensing.
 */
#pragma once

typedef enum _Context
{
    ContextAPI, //!< Base priority
    ContextDiagServer, //!< Higher priority, this overrides API
} Context;
