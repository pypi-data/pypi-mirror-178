/*
 * Copyright (c) CTR-Electronics
 * Contact support@ctr-electronics for any questions
 * including support, features, and licensing.
 */
#pragma once

#include <string>

namespace ctre
{
    namespace phoenixpro
    {
        namespace spns
        {
            /**
             * \brief Class that holds all the SPN values used in Phoenix Pro devices.
             */
            class SpnValue
            {
            public:
                int value;

                static constexpr int DeviceTemperature = 406;
                static constexpr int ProcessorTemperature = 622;
                static constexpr int TALONFX_MeasurementStatorCurrent_FR_Small = 646;
                static constexpr int TALONFX_MeasurementStatorCurrent_MB_Small = 647;
                static constexpr int TALONFX_MeasurementSupplyCurrent_Small = 648;
                static constexpr int TALONFX_SupplyVoltage = 649;
                static constexpr int AbsPosition = 728;
                static constexpr int CANCoder_SupplyVoltage = 729;
                static constexpr int CANcoder_MagHealth = 730;
                static constexpr int CANCoder_PulseWidth = 731;
                static constexpr int Version_Major = 732;
                static constexpr int Version_Minor = 733;
                static constexpr int Version_Bugfix = 734;
                static constexpr int Version_Build = 735;
                static constexpr int VoltageRampRate = 807;
                static constexpr int Slot0_kP = 808;
                static constexpr int Slot0_kI = 809;
                static constexpr int Slot0_kD = 810;
                static constexpr int Slot0_kV = 811;
                static constexpr int Slot0_PeakOutput = 814;
                static constexpr int Slot1_kP = 815;
                static constexpr int Slot1_kI = 816;
                static constexpr int Slot1_kD = 817;
                static constexpr int Slot1_kV = 818;
                static constexpr int Slot1_PeakOutput = 821;
                static constexpr int CANcoder_SensorDirection = 823;
                static constexpr int TalonFX_DutyCycle = 870;
                static constexpr int Velocity = 873;
                static constexpr int Position = 874;
                static constexpr int TalonFX_PIDInput_Position_Reference = 875;
                static constexpr int TalonFX_PIDInput_Position_ReferenceSlope = 876;
                static constexpr int TalonFX_PIDInput_Position_FeedForward = 877;
                static constexpr int TalonFX_PIDInput_Position_Slot = 878;
                static constexpr int TalonFX_PIDInput_Velocity_Reference = 879;
                static constexpr int TalonFX_PIDInput_Velocity_ReferenceSlope = 880;
                static constexpr int TalonFX_PIDInput_Velocity_FeedForward = 881;
                static constexpr int TalonFX_PIDInput_Velocity_Slot = 882;
                static constexpr int TalonFX_PIDState_PercentSupply_IntegratedAccum = 883;
                static constexpr int TalonFX_PIDOutpu_PercentSupply_PropOut = 884;
                static constexpr int TalonFX_PIDOutpu_PercentSupply_DerivOut = 885;
                static constexpr int TalonFX_PIDOutpu_PercentSupply_Output = 886;
                static constexpr int TalonFX_PIDState_MotorVoltage_IntegratedAccum = 887;
                static constexpr int TalonFX_PIDOutpu_MotorVoltage_PropOut = 888;
                static constexpr int TalonFX_PIDOutpu_MotorVoltage_DerivOut = 889;
                static constexpr int TalonFX_PIDOutpu_MotorVoltage_Output = 890;
                static constexpr int TalonFX_PIDState_TorqueCurrent_IntegratedAccum = 891;
                static constexpr int TalonFX_PIDOutpu_TorqueCurrent_PropOut = 892;
                static constexpr int TalonFX_PIDOutpu_TorqueCurrent_DerivOut = 893;
                static constexpr int TalonFX_PIDOutpu_TorqueCurrent_Output = 894;
                static constexpr int Config_Inverted = 909;
                static constexpr int TalonFX_ControlMode = 922;
                static constexpr int Pigeon2Temperature = 976;
                static constexpr int Pigeon2NoMotionCalEnabled = 977;
                static constexpr int Pigeon2NoMotionCount = 978;
                static constexpr int Pigeon2UpTime = 979;
                static constexpr int Pigeon2TempCompDisabled = 980;
                static constexpr int Pigeon2_SupplyVoltage = 983;
                static constexpr int Pigeon2Yaw = 985;
                static constexpr int Pigeon2Pitch = 986;
                static constexpr int Pigeon2Roll = 987;
                static constexpr int Pigeon2QuatW = 988;
                static constexpr int Pigeon2QuatX = 989;
                static constexpr int Pigeon2QuatY = 990;
                static constexpr int Pigeon2QuatZ = 991;
                static constexpr int Pigeon2AccumGyroX = 992;
                static constexpr int Pigeon2AccumGyroY = 993;
                static constexpr int Pigeon2AccumGyroZ = 994;
                static constexpr int Pigeon2GravityVectorX = 995;
                static constexpr int Pigeon2GravityVectorY = 996;
                static constexpr int Pigeon2GravityVectorZ = 997;
                static constexpr int Pigeon2AngularVelocityX = 998;
                static constexpr int Pigeon2AngularVelocityY = 999;
                static constexpr int Pigeon2AngularVelocityZ = 1000;
                static constexpr int Pigeon2MagneticFieldX = 1001;
                static constexpr int Pigeon2MagneticFieldY = 1002;
                static constexpr int Pigeon2MagneticFieldZ = 1003;
                static constexpr int Pigeon2AccelerationX = 1004;
                static constexpr int Pigeon2AccelerationY = 1005;
                static constexpr int Pigeon2AccelerationZ = 1006;
                static constexpr int Pigeon2RawMagneticFieldX = 1011;
                static constexpr int Pigeon2RawMagneticFieldY = 1012;
                static constexpr int Pigeon2RawMagneticFieldZ = 1013;
                static constexpr int CANCoder_MagnetOffset = 1014;
                static constexpr int CANcoder_AbsoluteSensorRange = 1015;
                static constexpr int CANCoder_RawPos = 1036;
                static constexpr int CANCoder_RawVel = 1037;
                static constexpr int ForwardLimit = 1049;
                static constexpr int ReverseLimit = 1050;

                /**
                 * \brief Gets the string representation of this enum
                 *
                 * \return String representation of this enum
                 */
                std::string ToString() const
                {
                    switch (value)
                    {
                    case SpnValue::DeviceTemperature: return "DeviceTemperature";
                    case SpnValue::ProcessorTemperature: return "ProcessorTemperature";
                    case SpnValue::TALONFX_MeasurementStatorCurrent_FR_Small: return "TALONFX_MeasurementStatorCurrent_FR_Small";
                    case SpnValue::TALONFX_MeasurementStatorCurrent_MB_Small: return "TALONFX_MeasurementStatorCurrent_MB_Small";
                    case SpnValue::TALONFX_MeasurementSupplyCurrent_Small: return "TALONFX_MeasurementSupplyCurrent_Small";
                    case SpnValue::TALONFX_SupplyVoltage: return "TALONFX_SupplyVoltage";
                    case SpnValue::AbsPosition: return "AbsPosition";
                    case SpnValue::CANCoder_SupplyVoltage: return "CANCoder_SupplyVoltage";
                    case SpnValue::CANcoder_MagHealth: return "CANcoder_MagHealth";
                    case SpnValue::CANCoder_PulseWidth: return "CANCoder_PulseWidth";
                    case SpnValue::Version_Major: return "Version_Major";
                    case SpnValue::Version_Minor: return "Version_Minor";
                    case SpnValue::Version_Bugfix: return "Version_Bugfix";
                    case SpnValue::Version_Build: return "Version_Build";
                    case SpnValue::VoltageRampRate: return "VoltageRampRate";
                    case SpnValue::Slot0_kP: return "Slot0_kP";
                    case SpnValue::Slot0_kI: return "Slot0_kI";
                    case SpnValue::Slot0_kD: return "Slot0_kD";
                    case SpnValue::Slot0_kV: return "Slot0_kV";
                    case SpnValue::Slot0_PeakOutput: return "Slot0_PeakOutput";
                    case SpnValue::Slot1_kP: return "Slot1_kP";
                    case SpnValue::Slot1_kI: return "Slot1_kI";
                    case SpnValue::Slot1_kD: return "Slot1_kD";
                    case SpnValue::Slot1_kV: return "Slot1_kV";
                    case SpnValue::Slot1_PeakOutput: return "Slot1_PeakOutput";
                    case SpnValue::CANcoder_SensorDirection: return "CANcoder_SensorDirection";
                    case SpnValue::TalonFX_DutyCycle: return "TalonFX_DutyCycle";
                    case SpnValue::Velocity: return "Velocity";
                    case SpnValue::Position: return "Position";
                    case SpnValue::TalonFX_PIDInput_Position_Reference: return "TalonFX_PIDInput_Position_Reference";
                    case SpnValue::TalonFX_PIDInput_Position_ReferenceSlope: return "TalonFX_PIDInput_Position_ReferenceSlope";
                    case SpnValue::TalonFX_PIDInput_Position_FeedForward: return "TalonFX_PIDInput_Position_FeedForward";
                    case SpnValue::TalonFX_PIDInput_Position_Slot: return "TalonFX_PIDInput_Position_Slot";
                    case SpnValue::TalonFX_PIDInput_Velocity_Reference: return "TalonFX_PIDInput_Velocity_Reference";
                    case SpnValue::TalonFX_PIDInput_Velocity_ReferenceSlope: return "TalonFX_PIDInput_Velocity_ReferenceSlope";
                    case SpnValue::TalonFX_PIDInput_Velocity_FeedForward: return "TalonFX_PIDInput_Velocity_FeedForward";
                    case SpnValue::TalonFX_PIDInput_Velocity_Slot: return "TalonFX_PIDInput_Velocity_Slot";
                    case SpnValue::TalonFX_PIDState_PercentSupply_IntegratedAccum: return "TalonFX_PIDState_PercentSupply_IntegratedAccum";
                    case SpnValue::TalonFX_PIDOutpu_PercentSupply_PropOut: return "TalonFX_PIDOutpu_PercentSupply_PropOut";
                    case SpnValue::TalonFX_PIDOutpu_PercentSupply_DerivOut: return "TalonFX_PIDOutpu_PercentSupply_DerivOut";
                    case SpnValue::TalonFX_PIDOutpu_PercentSupply_Output: return "TalonFX_PIDOutpu_PercentSupply_Output";
                    case SpnValue::TalonFX_PIDState_MotorVoltage_IntegratedAccum: return "TalonFX_PIDState_MotorVoltage_IntegratedAccum";
                    case SpnValue::TalonFX_PIDOutpu_MotorVoltage_PropOut: return "TalonFX_PIDOutpu_MotorVoltage_PropOut";
                    case SpnValue::TalonFX_PIDOutpu_MotorVoltage_DerivOut: return "TalonFX_PIDOutpu_MotorVoltage_DerivOut";
                    case SpnValue::TalonFX_PIDOutpu_MotorVoltage_Output: return "TalonFX_PIDOutpu_MotorVoltage_Output";
                    case SpnValue::TalonFX_PIDState_TorqueCurrent_IntegratedAccum: return "TalonFX_PIDState_TorqueCurrent_IntegratedAccum";
                    case SpnValue::TalonFX_PIDOutpu_TorqueCurrent_PropOut: return "TalonFX_PIDOutpu_TorqueCurrent_PropOut";
                    case SpnValue::TalonFX_PIDOutpu_TorqueCurrent_DerivOut: return "TalonFX_PIDOutpu_TorqueCurrent_DerivOut";
                    case SpnValue::TalonFX_PIDOutpu_TorqueCurrent_Output: return "TalonFX_PIDOutpu_TorqueCurrent_Output";
                    case SpnValue::Config_Inverted: return "Config_Inverted";
                    case SpnValue::TalonFX_ControlMode: return "TalonFX_ControlMode";
                    case SpnValue::Pigeon2Temperature: return "Pigeon2Temperature";
                    case SpnValue::Pigeon2NoMotionCalEnabled: return "Pigeon2NoMotionCalEnabled";
                    case SpnValue::Pigeon2NoMotionCount: return "Pigeon2NoMotionCount";
                    case SpnValue::Pigeon2UpTime: return "Pigeon2UpTime";
                    case SpnValue::Pigeon2TempCompDisabled: return "Pigeon2TempCompDisabled";
                    case SpnValue::Pigeon2_SupplyVoltage: return "Pigeon2_SupplyVoltage";
                    case SpnValue::Pigeon2Yaw: return "Pigeon2Yaw";
                    case SpnValue::Pigeon2Pitch: return "Pigeon2Pitch";
                    case SpnValue::Pigeon2Roll: return "Pigeon2Roll";
                    case SpnValue::Pigeon2QuatW: return "Pigeon2QuatW";
                    case SpnValue::Pigeon2QuatX: return "Pigeon2QuatX";
                    case SpnValue::Pigeon2QuatY: return "Pigeon2QuatY";
                    case SpnValue::Pigeon2QuatZ: return "Pigeon2QuatZ";
                    case SpnValue::Pigeon2AccumGyroX: return "Pigeon2AccumGyroX";
                    case SpnValue::Pigeon2AccumGyroY: return "Pigeon2AccumGyroY";
                    case SpnValue::Pigeon2AccumGyroZ: return "Pigeon2AccumGyroZ";
                    case SpnValue::Pigeon2GravityVectorX: return "Pigeon2GravityVectorX";
                    case SpnValue::Pigeon2GravityVectorY: return "Pigeon2GravityVectorY";
                    case SpnValue::Pigeon2GravityVectorZ: return "Pigeon2GravityVectorZ";
                    case SpnValue::Pigeon2AngularVelocityX: return "Pigeon2AngularVelocityX";
                    case SpnValue::Pigeon2AngularVelocityY: return "Pigeon2AngularVelocityY";
                    case SpnValue::Pigeon2AngularVelocityZ: return "Pigeon2AngularVelocityZ";
                    case SpnValue::Pigeon2MagneticFieldX: return "Pigeon2MagneticFieldX";
                    case SpnValue::Pigeon2MagneticFieldY: return "Pigeon2MagneticFieldY";
                    case SpnValue::Pigeon2MagneticFieldZ: return "Pigeon2MagneticFieldZ";
                    case SpnValue::Pigeon2AccelerationX: return "Pigeon2AccelerationX";
                    case SpnValue::Pigeon2AccelerationY: return "Pigeon2AccelerationY";
                    case SpnValue::Pigeon2AccelerationZ: return "Pigeon2AccelerationZ";
                    case SpnValue::Pigeon2RawMagneticFieldX: return "Pigeon2RawMagneticFieldX";
                    case SpnValue::Pigeon2RawMagneticFieldY: return "Pigeon2RawMagneticFieldY";
                    case SpnValue::Pigeon2RawMagneticFieldZ: return "Pigeon2RawMagneticFieldZ";
                    case SpnValue::CANCoder_MagnetOffset: return "CANCoder_MagnetOffset";
                    case SpnValue::CANcoder_AbsoluteSensorRange: return "CANcoder_AbsoluteSensorRange";
                    case SpnValue::CANCoder_RawPos: return "CANCoder_RawPos";
                    case SpnValue::CANCoder_RawVel: return "CANCoder_RawVel";
                    case SpnValue::ForwardLimit: return "ForwardLimit";
                    case SpnValue::ReverseLimit: return "ReverseLimit";
                    default:
                        return "Invalid Value";
                    }
                }

                friend std::ostream &operator<<(std::ostream &os, const SpnValue &data)
                {
                    os << data.ToString();
                    return os;
                }
                bool operator==(const SpnValue &data) const
                {
                    return this->value == data.value;
                }
                bool operator==(int data) const
                {
                    return this->value == data;
                }
                bool operator<(const SpnValue &data) const
                {
                    return this->value < data.value;
                }
                bool operator<(int data) const
                {
                    return this->value < data;
                }
            };
        }
    }
}
