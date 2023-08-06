/*
 * Copyright (c) CTR-Electronics
 * Contact support@ctr-electronics for any questions
 * including support, features, and licensing.
 */
#pragma once

namespace ctre {
namespace phoenix {
namespace platform {

	/** List of all supporte device types */
	#define kDeviceTypeListInitializer	TalonSRXType, VictorSPXType, PigeonIMUType, RibbonPigeonIMUType, TalonFXType, CANCoderType


	enum DeviceType {kDeviceTypeListInitializer};

	namespace can {

		typedef enum {
			// CAN 2.0 Network
			CAN2 = 1,
			// CAN FD Network
			CANFD = 2,
			// CAN 2.0 or CAN FD Network
			CAN = 3,
		} NetworkType;

	}

}
}
}
