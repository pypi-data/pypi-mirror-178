#ifndef _ICM20948_HPP_
#define _ICM20948_HPP_
#include "../common.hpp"
namespace ICM20948 {

    const uint8_t ICM20948_DEFAULT_I2C_ADDRESS =            (uint8_t)(0x69);
    const uint8_t ICM20948_ALT_I2C_ADDRESS =                (uint8_t)(0x68);

    const uint8_t CORRECT_WHO_AM_I_VALUE =                  (uint8_t)(0xEA);
    const uint8_t WHO_AM_I_VALUE =                          (uint8_t)(0xEA);
    const uint8_t BANK_SEL_REG_ADDR =                       (uint8_t)(0x7F);



    // Bank 0 Register
    const uint8_t WHO_AM_I_REG_ADDR =                       (uint8_t)(0x00);
    const uint8_t USER_CTRL_REG_ADDR =                      (uint8_t)(0x03);
    const uint8_t LP_CONFIG_REG_ADDR =                      (uint8_t)(0x05);
    const uint8_t POWER_MANAGEMENT_REG_1_ADDR =             (uint8_t)(0x06);
    const uint8_t POWER_MANAGEMENT_REG_2_ADDR =             (uint8_t)(0x07);
    const uint8_t INT_PIN_CFG_REG_ADDR =                    (uint8_t)(0x0F);
    const uint8_t ACCEL_XOUT_H_REG_ADDR =                   (uint8_t)(0x2D); // first byte of acceleromete data address
    const uint8_t GYRO_XOUT_H_REG_ADDR =                    (uint8_t)(0x33); // first byte of gyroscope data address
    const uint8_t I2C_MST_STATUS_REG_ADDR =                 (uint8_t)(0x17);
    const uint8_t EXT_SLV_SENS_DATA_00_REG_ADDR =           (uint8_t)(0x3B);

    // Bank 1 Register


    // Bank 2 Register
    const uint8_t GYRO_SMPLRT_DIV_REG_ADDR =                (uint8_t)(0x00);
    const uint8_t GYRO_CONFIG_1_REG_ADDR =                  (uint8_t)(0x01);
    const uint8_t GYRO_CONFIG_2_REG_ADDR =                  (uint8_t)(0x02);
    const uint8_t ACCEL_SMPLRT_DIV_1_REG_ADDR =             (uint8_t)(0x10);
    const uint8_t ACCEL_SMPLRT_DIV_2_REG_ADDR =             (uint8_t)(0x11);
    const uint8_t ACCEL_CONFIG_1_REG_ADDR =                 (uint8_t)(0x14);
    const uint8_t ACCEL_CONFIG_2_REG_ADDR =                 (uint8_t)(0x15);

    // Bank 3 Register
    const uint8_t I2C_MST_ODR_CONFIG_REG_ADDR =             (uint8_t)(0x00);
    const uint8_t I2C_MST_CTRL_REG_ADDR =                   (uint8_t)(0x01);
    const uint8_t I2C_MST_DELAY_CTRL_REG_ADDR =             (uint8_t)(0x02);
    const uint8_t I2C_SLV0_ADDR_REG_ADDR =                  (uint8_t)(0x03);
    const uint8_t I2C_SLV0_REG_REG_ADDR =                   (uint8_t)(0x04);
    const uint8_t I2C_SLV0_CTRL_REG_ADDR =                  (uint8_t)(0x05);
    const uint8_t I2C_SLV0_DO_REG_ADDR =                    (uint8_t)(0x06);
    const uint8_t I2C_SLV4_ADDR_REG_ADDR =                  (uint8_t)(0x13);
    const uint8_t I2C_SLV4_REG_REG_ADDR =                   (uint8_t)(0x14);
    const uint8_t I2C_SLV4_CTRL_REG_ADDR =                  (uint8_t)(0x15);
    const uint8_t I2C_SLV4_DO_REG_ADDR =                    (uint8_t)(0x16);
    const uint8_t I2C_SLV4_DI_REG_ADDR =                    (uint8_t)(0x17);

    // Magnetometer Register
    const uint8_t MAG_CNTL2_REG_ADDR =                      (uint8_t)(0x31);
    const uint8_t MAG_WHO_AM_I_REG_ADDR =                   (uint8_t)(0x01);


    const uint8_t BANK_0 =                                  (uint8_t)(0x00);
    const uint8_t BANK_1 =                                  (uint8_t)(0x10);
    const uint8_t BANK_2 =                                  (uint8_t)(0x20);
    const uint8_t BANK_3 =                                  (uint8_t)(0x30);
    const double ACCEL_SCALE_FACTOR_ARRAY[4] = {1/16384.0, 1/8192.0, 1/4096.0, 1/2048.0};
    const double GYRO_SCALE_FACTOR_ARRAY[4] = {1/131.0, 1/65.5, 1/32.8, 1/16.4};
    const double MAG_SCALE_FACTOR = 4912.0 / 32752.0;

    // Exposed to Python

    const uint8_t INVALID_RANGE =                           (uint8_t)(0xFF);

    const uint8_t ACCEL_RANGE_2G =                          (uint8_t)(0x00);
    const uint8_t ACCEL_RANGE_4G =                          (uint8_t)(0x02);
    const uint8_t ACCEL_RANGE_8G =                          (uint8_t)(0x04);
    const uint8_t ACCEL_RANGE_16G =                         (uint8_t)(0x06);
    const uint8_t ACCEL_RANGE_MASK =                        (uint8_t)(0xF9);
    
    const uint8_t GYRO_RANGE_250DPS =                       (uint8_t)(0x00);
    const uint8_t GYRO_RANGE_500DPS =                       (uint8_t)(0x02);
    const uint8_t GYRO_RANGE_1000DPS =                      (uint8_t)(0x04);
    const uint8_t GYRO_RANGE_2000DPS =                      (uint8_t)(0x06);
    const uint8_t GYRO_RANGE_MASK =                         (uint8_t)(0xF9);


    const uint8_t MAG_POWER_DOWN_MODE =                     (uint8_t)(0x00);
    const uint8_t MAG_SINGLE_MEASURE_MODE =                 (uint8_t)(0x01);
    const uint8_t MAG_FREQ_10HZ_MODE =                      (uint8_t)(0x02);
    const uint8_t MAG_FREQ_20HZ_MODE =                      (uint8_t)(0x04);
    const uint8_t MAG_FREQ_50HZ_MODE =                      (uint8_t)(0x06);
    const uint8_t MAG_FREQ_100HZ_MODE =                     (uint8_t)(0x08);
    const uint8_t MAG_SELF_TEST_MODE =                      (uint8_t)(0x10);
    
    

    struct DataPack {
        std::atomic<bool> accelValid;
        std::atomic<bool> gyroValid;
        std::atomic<bool> magValid;
        std::atomic<int16_t> temperature;
        int16_t accelX, accelY, accelZ;
        int16_t gyroX, gyroY, gyroZ;
        int16_t magX, magY, magZ;
        std::mutex accelMutex;
        std::mutex gyroMutex;
        std::mutex magMutex;
    };

    class ICM20948: public Sensor {
        private:
            uint8_t _currentBank;
            uint8_t _currentWhoAmI;
            uint8_t _currentPowerStatus1;

            uint8_t _currentAccelFreqDivisor;
            uint8_t _currentAccelRange;

            uint8_t _currentGyroFreqDivisor;
            uint8_t _currentGyroRange;

            uint8_t _currentMagMode;
            
            inline void _switch_bank(mraa::I2c& i2cBus, uint8_t bank) {
                i2cBus.writeReg(BANK_SEL_REG_ADDR, bank);
                std::this_thread::sleep_for(std::chrono::milliseconds(50));
            }
            // Bank 0 Operation
            inline uint8_t _who_am_i(mraa::I2c& i2cBus) {
                if (_currentBank != BANK_0) {
                    _switch_bank(i2cBus, BANK_0);
                    _currentBank = BANK_0;
                }
                _currentWhoAmI = i2cBus.readReg(WHO_AM_I_REG_ADDR);
                return _currentWhoAmI;
            }
            inline void _reset(mraa::I2c& i2cBus) {
                _switch_bank(i2cBus, BANK_0);
                _currentBank = BANK_0;
                _currentPowerStatus1 = i2cBus.readReg(POWER_MANAGEMENT_REG_1_ADDR);
                _currentPowerStatus1 |= (uint8_t)(0x80);
                i2cBus.writeReg(POWER_MANAGEMENT_REG_1_ADDR, _currentPowerStatus1);
            }
            
            inline void _wake(mraa::I2c& i2cBus) {
                if (_currentBank != BANK_0) {
                    _switch_bank(i2cBus, BANK_0);
                    _currentBank = BANK_0;
                }
                _currentPowerStatus1 = i2cBus.readReg(POWER_MANAGEMENT_REG_1_ADDR);
                _currentPowerStatus1 &= (uint8_t)(0xBF);
                i2cBus.writeReg(POWER_MANAGEMENT_REG_1_ADDR, _currentPowerStatus1);
            }
            // Bank 2 Operation
            inline void _set_accel_range(mraa::I2c& i2cBus) {
                if (_currentBank != BANK_2) {
                    _switch_bank(i2cBus, BANK_2);
                    _currentBank = BANK_2;
                }
                auto currentAccelConfig1 = i2cBus.readReg(ACCEL_CONFIG_1_REG_ADDR);
                currentAccelConfig1 = (currentAccelConfig1 & ACCEL_RANGE_MASK) | _currentAccelRange;
                i2cBus.writeReg(ACCEL_CONFIG_1_REG_ADDR, currentAccelConfig1);
            }
            inline void _set_accel_freq(mraa::I2c& i2cBus) {
                if (_currentBank != BANK_2) {
                    _switch_bank(i2cBus, BANK_2);
                    _currentBank = BANK_2;
                }
                i2cBus.writeReg(ACCEL_SMPLRT_DIV_2_REG_ADDR, _currentAccelFreqDivisor);
            }

            inline void _set_gyro_range(mraa::I2c& i2cBus) {
                if (_currentBank != BANK_2) {
                    _switch_bank(i2cBus, BANK_2);
                    _currentBank = BANK_2;
                }
                auto currentGyroConfig1 = i2cBus.readReg(GYRO_CONFIG_1_REG_ADDR);
                currentGyroConfig1 = (currentGyroConfig1 & GYRO_RANGE_MASK) | _currentGyroRange;
                i2cBus.writeReg(GYRO_CONFIG_1_REG_ADDR, currentGyroConfig1);
            }
            inline void _set_gyro_freq(mraa::I2c& i2cBus) {
                if (_currentBank != BANK_2) {
                    _switch_bank(i2cBus, BANK_2);
                    _currentBank = BANK_2;
                }
                i2cBus.writeReg(GYRO_SMPLRT_DIV_REG_ADDR, _currentGyroFreqDivisor);
            }

            // Magnetometer Operation
            inline void _disable_bypass(mraa::I2c& i2cBus) {
                if (_currentBank != BANK_0) {
                    _switch_bank(i2cBus, BANK_0);
                    _currentBank = BANK_0;
                }
                auto currentIntPinConfig = i2cBus.readReg(INT_PIN_CFG_REG_ADDR);
                currentIntPinConfig &= (uint8_t)(0xFD);
                i2cBus.writeReg(INT_PIN_CFG_REG_ADDR, currentIntPinConfig);
            }
            inline void _config_master(mraa::I2c& i2cBus) {
                if (_currentBank != BANK_3) {
                    _switch_bank(i2cBus, BANK_3);
                    _currentBank = BANK_3;
                }
                i2cBus.writeReg(I2C_MST_CTRL_REG_ADDR, (uint8_t)(0x17));
            }

            inline void _reset_master(mraa::I2c& i2cBus) {
                if (_currentBank != BANK_0) {
                    _switch_bank(i2cBus, BANK_0);
                    _currentBank = BANK_0;
                }
                auto currentUserControlConfig = i2cBus.readReg(USER_CTRL_REG_ADDR);
                currentUserControlConfig |= (uint8_t)(0x02);
                i2cBus.writeReg(USER_CTRL_REG_ADDR, currentUserControlConfig);
                std::this_thread::sleep_for(std::chrono::milliseconds(50));
            }

            inline void _enable_master(mraa::I2c& i2cBus) {
                if (_currentBank != BANK_0) {
                    _switch_bank(i2cBus, BANK_0);
                    _currentBank = BANK_0;
                }
                auto currentUserControlConfig = i2cBus.readReg(USER_CTRL_REG_ADDR);
                currentUserControlConfig |= (uint8_t)(0x20);
                i2cBus.writeReg(USER_CTRL_REG_ADDR, currentUserControlConfig);
            }

            inline void _enable_mag(mraa::I2c& i2cBus) {
                _disable_bypass(i2cBus);
                std::this_thread::sleep_for(std::chrono::milliseconds(50));
                _config_master(i2cBus);
                std::this_thread::sleep_for(std::chrono::milliseconds(50));
                _enable_master(i2cBus);
                std::this_thread::sleep_for(std::chrono::milliseconds(50));
            }

            inline void _async_read_mag_register(mraa::I2c& i2cBus, uint8_t magRegisterAddr) {
                if (_currentBank != BANK_3) {
                    _switch_bank(i2cBus, BANK_3);
                    _currentBank = BANK_3;
                }
                i2cBus.writeReg(I2C_SLV4_ADDR_REG_ADDR, (uint8_t)(0x8C));
                std::this_thread::sleep_for(std::chrono::milliseconds(10));
                i2cBus.writeReg(I2C_SLV4_REG_REG_ADDR, magRegisterAddr);
                std::this_thread::sleep_for(std::chrono::milliseconds(10));
                i2cBus.writeReg(I2C_SLV4_CTRL_REG_ADDR, (uint8_t)(0x80));
                std::this_thread::sleep_for(std::chrono::milliseconds(10));
            }

            inline uint8_t _await_read_mag_register(mraa::I2c& i2cBus) {
                if (_currentBank != BANK_0) {
                    _switch_bank(i2cBus, BANK_0);
                    _currentBank = BANK_0;
                }
                auto currentI2cMasterStatus = i2cBus.readReg(I2C_MST_STATUS_REG_ADDR);
                int waitCount = 0;
                while (true) {
                    if (waitCount == 100) {
                        fprintf(stderr, "%s -> Warning: Magnetometer Read May Stuck[%d]!\n", sensorName.c_str(), waitCount);
                        return 255;
                    }
                    if ((currentI2cMasterStatus & (uint8_t)(0x40))) {
                        _switch_bank(i2cBus, BANK_3);
                        return i2cBus.readReg(I2C_SLV4_DI_REG_ADDR);
                    } else {
                        waitCount++;
                        std::this_thread::sleep_for(std::chrono::milliseconds(10));
                        currentI2cMasterStatus = i2cBus.readReg(I2C_MST_STATUS_REG_ADDR);
                        continue;
                    }
                }
            }

            inline void _async_write_mag_register(mraa::I2c& i2cBus, uint8_t magRegisterAddr, uint8_t data) {
                if (_currentBank != BANK_3) {
                    _switch_bank(i2cBus, BANK_3);
                    _currentBank = BANK_3;
                }
                i2cBus.writeReg(I2C_SLV4_ADDR_REG_ADDR, (uint8_t)(0x0C));
                std::this_thread::sleep_for(std::chrono::milliseconds(10));
                i2cBus.writeReg(I2C_SLV4_REG_REG_ADDR, magRegisterAddr);
                std::this_thread::sleep_for(std::chrono::milliseconds(10));
                i2cBus.writeReg(I2C_SLV4_DO_REG_ADDR, data);
                std::this_thread::sleep_for(std::chrono::milliseconds(10));
                i2cBus.writeReg(I2C_SLV4_CTRL_REG_ADDR, (uint8_t)(0x80));
                std::this_thread::sleep_for(std::chrono::milliseconds(10));
            }

            inline void _await_write_mag_register(mraa::I2c& i2cBus) {
                if (_currentBank != BANK_0) {
                    _switch_bank(i2cBus, BANK_0);
                    _currentBank = BANK_0;
                }
                auto currentI2cMasterStatus = i2cBus.readReg(I2C_MST_STATUS_REG_ADDR);
                int waitCount = 0;
                while (true) {
                    if (waitCount == 100) {
                        fprintf(stderr, "%s -> Warning: Magnetometer Write May Stuck[%d]!\n", sensorName.c_str(), waitCount);
                        return;
                    }
                    if ((currentI2cMasterStatus & (uint8_t)(0x40))) {
                        return;
                    } else {
                        waitCount++;
                        std::this_thread::sleep_for(std::chrono::milliseconds(10));
                        currentI2cMasterStatus = i2cBus.readReg(I2C_MST_STATUS_REG_ADDR);
                        continue;
                    }
                }
            }

            inline void _set_mag_mode(mraa::I2c& i2cBus) {
                _async_write_mag_register(i2cBus, MAG_CNTL2_REG_ADDR, MAG_POWER_DOWN_MODE);
                std::this_thread::sleep_for(std::chrono::milliseconds(10));
                _await_write_mag_register(i2cBus);
                std::this_thread::sleep_for(std::chrono::milliseconds(50));
                _async_write_mag_register(i2cBus, MAG_CNTL2_REG_ADDR, _currentMagMode);
                std::this_thread::sleep_for(std::chrono::milliseconds(10));
                _await_write_mag_register(i2cBus);
                std::this_thread::sleep_for(std::chrono::milliseconds(50));
            }

            inline void _check_mag_configured(mraa::I2c& i2cBus) {
                _async_read_mag_register(i2cBus, MAG_CNTL2_REG_ADDR);
                auto result = _await_read_mag_register(i2cBus);
                while (result != _currentMagMode) {
                    fprintf(stderr, "%s -> Warning: Magnetometer Abnormal!\n", sensorName.c_str());
                    fprintf(stderr, "%s -> Warning: I2C Master Reset!\n", sensorName.c_str());
                    _reset_master(i2cBus);
                    _async_read_mag_register(i2cBus, MAG_CNTL2_REG_ADDR);
                    result = _await_read_mag_register(i2cBus);
                }
                // while (result == 255) {
                //     fprintf(stderr, "%s -> Warning: I2C Master Reset!\n", sensorName.c_str());
                //     _reset_master(i2cBus);
                //     _async_read_mag_register(i2cBus, MAG_WHO_AM_I_REG_ADDR);
                //     result = _await_read_mag_register(i2cBus);
                // }
            }

            inline void _start_reading_mag(mraa::I2c& i2cBus) {
                if (_currentBank != BANK_3) {
                    _switch_bank(i2cBus, BANK_3);
                    _currentBank = BANK_3;
                }
                i2cBus.writeReg(I2C_SLV0_ADDR_REG_ADDR, (uint8_t)(0x8C));
                std::this_thread::sleep_for(std::chrono::milliseconds(10));
                i2cBus.writeReg(I2C_SLV0_REG_REG_ADDR, (uint8_t)(0x11));
                std::this_thread::sleep_for(std::chrono::milliseconds(10));
                i2cBus.writeReg(I2C_SLV0_CTRL_REG_ADDR, (uint8_t)(0x89));
                std::this_thread::sleep_for(std::chrono::milliseconds(10));
            }

            inline void _config_mag(mraa::I2c& i2cBus) {
                _enable_mag(i2cBus);
                _set_mag_mode(i2cBus);
                _check_mag_configured(i2cBus);
                _start_reading_mag(i2cBus);
            }
        protected:
            friend class SensorBatch;
            friend void sensor_reading_thread(std::atomic<bool>&, std::vector<Sensor*>&, std::atomic<double>&);
            virtual void _sync_read_data(mraa::I2c& i2cBus) {
                uint8_t dataBuffer[20];
                if (_currentBank != BANK_0) {
                    _switch_bank(i2cBus, BANK_0);
                    _currentBank = BANK_0;
                }

                auto result = i2cBus.readBytesReg(ACCEL_XOUT_H_REG_ADDR, dataBuffer, 20);
                if (result != 20) {
                    printf("Read Error: %d!\n", result);
                }

                uint8_t temperatureGyroAccelRawData[14];
                for (int i = 0; i < 14; i++) {
                    temperatureGyroAccelRawData[i] = dataBuffer[13-i];
                }
                int16_t* temperatureRawData = (int16_t*)(temperatureGyroAccelRawData);
                int16_t* gyroRawData = (int16_t*)(temperatureGyroAccelRawData+2);
                int16_t* accelRawData = (int16_t*)(temperatureGyroAccelRawData+8);
                int16_t* magRawData = (int16_t*)(dataBuffer+14);

                
                if (_data.accelZ != accelRawData[0] || _data.accelY != accelRawData[1] || _data.accelX != accelRawData[2]) {
                    _data.accelMutex.lock();
                    _data.accelZ = accelRawData[0];
                    _data.accelY = accelRawData[1];
                    _data.accelX = accelRawData[2];
                    _data.accelMutex.unlock();
                    _data.accelValid = true;
                }
                
                
                if (_data.gyroZ != gyroRawData[0] || _data.gyroY != gyroRawData[1] || _data.gyroX != gyroRawData[2]) {
                    _data.gyroMutex.lock();
                    _data.gyroZ = gyroRawData[0];
                    _data.gyroY = gyroRawData[1];
                    _data.gyroX = gyroRawData[2];
                    _data.gyroMutex.unlock();
                    _data.gyroValid = true;
                }
                
                
                if (_data.magX != magRawData[0] || _data.magY != magRawData[1] || _data.magZ != magRawData[2]) {
                    _data.magMutex.lock();
                    _data.magX = magRawData[0];
                    _data.magY = magRawData[1];
                    _data.magZ = magRawData[2];
                    _data.magMutex.unlock();
                    _data.magValid = true;
                }
                
                _data.temperature = temperatureRawData[0];
            }
            virtual void _async_read_data(mraa::I2c& i2cBus) {
                i2cBus.address(_i2cAddress);
            }
            virtual void _await_read_data(mraa::I2c& i2cBus) {

            }
            virtual void _init(mraa::I2c& i2cBus) {
                _isReading = true;
                i2cBus.address(_i2cAddress);
                _reset(i2cBus);
                std::this_thread::sleep_for(std::chrono::milliseconds(50));
                _wake(i2cBus);
                std::this_thread::sleep_for(std::chrono::milliseconds(50));
                _who_am_i(i2cBus);
                std::this_thread::sleep_for(std::chrono::milliseconds(50));
            }
            virtual void _configure(mraa::I2c& i2cBus) {
                _config_mag(i2cBus);
                std::this_thread::sleep_for(std::chrono::milliseconds(50));
                _set_accel_range(i2cBus);
                std::this_thread::sleep_for(std::chrono::milliseconds(50));
                _set_gyro_range(i2cBus);
                std::this_thread::sleep_for(std::chrono::milliseconds(50));
                _set_accel_freq(i2cBus);
                std::this_thread::sleep_for(std::chrono::milliseconds(50));
                _set_gyro_freq(i2cBus);
                std::this_thread::sleep_for(std::chrono::milliseconds(50));
            }
            virtual void _close(mraa::I2c& i2cBus) {
                _reset(i2cBus);
            }
            DataPack _data;
            
        public:

            ICM20948(uint8_t i2cBusIndex, uint8_t i2cAddress = ICM20948_DEFAULT_I2C_ADDRESS)
            : Sensor(i2cBusIndex, i2cAddress), _data{} {
                // Accelerometer Defatul@225Hz 8g
                _currentAccelFreqDivisor = 4;
                _currentAccelRange = ACCEL_RANGE_8G;
                // Gyroscope Default@220Hz 500dps
                _currentGyroFreqDivisor = 4;
                _currentGyroRange = GYRO_RANGE_500DPS;
                // Magnetometer Default@100Hz
                _currentMagMode = MAG_FREQ_100HZ_MODE;
            }
            double get_accel_frequency(void) {
                return 1125.0 / (_currentAccelFreqDivisor + 1);
            }
            double get_gyro_frequency(void) {
                return 1100.0 / (_currentGyroFreqDivisor + 1);
            }
            double get_mag_frequency(void) {
                switch (_currentMagMode) {
                    case MAG_FREQ_100HZ_MODE:
                        return 100.0;
                    break;
                    case MAG_FREQ_50HZ_MODE:
                        return 50.0;
                    break;
                    case MAG_FREQ_20HZ_MODE:
                        return 20.0;
                    break;
                    case MAG_FREQ_10HZ_MODE:
                        return 10.0;
                    break;
                    default:
                        return 0.0;
                    break;
                }
            }
            double set_accel_frequency_divisor(uint8_t divisor) {
                if (!_isReading.load()) {
                    _currentAccelFreqDivisor = divisor;
                } else {
                    fprintf(stderr, "%s -> Warning: Invalid Operation: Sensor is Running\n", sensorName.c_str());
                }
                return get_accel_frequency();
            }
            double set_gyro_frequency_divisor(uint8_t divisor) {
                if (!_isReading.load()) {
                    _currentGyroFreqDivisor = divisor;
                } else {
                    fprintf(stderr, "%s -> Warning: Invalid Operation: Sensor is Running\n", sensorName.c_str());
                }
                return get_gyro_frequency();
            }
            double set_mag_mode(uint8_t mode) {
                if (!_isReading.load()) {
                    switch (mode) {
                        case MAG_POWER_DOWN_MODE:
                        case MAG_FREQ_10HZ_MODE:
                        case MAG_FREQ_20HZ_MODE:
                        case MAG_FREQ_50HZ_MODE:
                        case MAG_FREQ_100HZ_MODE:
                            _currentMagMode = mode;
                        break;
                        default:
                            fprintf(stderr, "%s -> Warning: Invalid Magnetometer Divisor: Available Value: 0~3\n", sensorName.c_str());
                        break;
                    }
                } else {
                    fprintf(stderr, "%s -> Warning: Invalid Operation: Sensor is Running\n", sensorName.c_str());
                }
                return get_mag_frequency();
            }

            uint8_t get_accel_range(void) {
                return _currentAccelRange;
            }
            uint8_t set_accel_range(uint8_t range) {
                if (!_isReading.load()) {
                    switch (range) {
                        case ACCEL_RANGE_2G:
                        case ACCEL_RANGE_4G:
                        case ACCEL_RANGE_8G:
                        case ACCEL_RANGE_16G:
                            _currentAccelRange = range;
                        break;
                        default:
                            fprintf(stderr, "%s -> Warning: Invalid Accelerometer Range", sensorName.c_str());
                        break;
                    }
                } else {
                    fprintf(stderr, "%s -> Warning: Invalid Operation: Sensor is Running\n", sensorName.c_str());
                }
                return get_accel_range();
            }

            uint8_t get_gyro_range(void) {
                return _currentGyroRange;
            }

            uint8_t set_gyro_range(uint8_t range) {
                if (!_isReading.load()) {
                    switch (range) {
                        case GYRO_RANGE_250DPS:
                        case GYRO_RANGE_500DPS:
                        case GYRO_RANGE_1000DPS:
                        case GYRO_RANGE_2000DPS:
                            _currentGyroRange = range;
                        break;
                        default:
                            fprintf(stderr, "%s -> Warning: Invalid Gyroscope Range", sensorName.c_str());
                        break;
                    }
                } else {
                    fprintf(stderr, "%s -> Warning: Invalid Operation: Sensor is Running\n", sensorName.c_str());
                }
                return get_gyro_range();
            }

            py::list get_accel_data(void) {
                py::list pyResult;
                int16_t accelX, accelY, accelZ;

                if (_data.accelValid.load()) {
                    _data.accelMutex.lock();
                    accelX = _data.accelX;
                    accelY = _data.accelY;
                    accelZ = _data.accelZ;
                    _data.accelMutex.unlock();
                    _data.accelValid = false;

                    pyResult.append(accelX * ACCEL_SCALE_FACTOR_ARRAY[(_currentAccelRange >> 1)]);
                    pyResult.append(accelY * ACCEL_SCALE_FACTOR_ARRAY[(_currentAccelRange >> 1)]);
                    pyResult.append(accelZ * ACCEL_SCALE_FACTOR_ARRAY[(_currentAccelRange >> 1)]);
                }
                
                return pyResult;
            }

            py::list get_gyro_data(void) {
                py::list pyResult;
                int16_t gyroX, gyroY, gyroZ;

                if (_data.gyroValid.load()) {
                    _data.gyroMutex.lock();
                    gyroX = _data.gyroX;
                    gyroY = _data.gyroY;
                    gyroZ = _data.gyroZ;
                    _data.gyroMutex.unlock();
                    _data.gyroValid = false;

                    pyResult.append(gyroX * GYRO_SCALE_FACTOR_ARRAY[(_currentGyroRange >> 1)]);
                    pyResult.append(gyroY * GYRO_SCALE_FACTOR_ARRAY[(_currentGyroRange >> 1)]);
                    pyResult.append(gyroZ * GYRO_SCALE_FACTOR_ARRAY[(_currentGyroRange >> 1)]);
                }
                
                return pyResult;
            }

            py::list get_mag_data(void) {
                py::list pyResult;
                int16_t magX, magY, magZ;

                if (_data.magValid.load()) {
                    _data.magMutex.lock();
                    magX = _data.magX;
                    magY = _data.magY;
                    magZ = _data.magZ;
                    _data.magMutex.unlock();
                    _data.magValid = false;

                    pyResult.append(magX * MAG_SCALE_FACTOR);
                    pyResult.append(magY * MAG_SCALE_FACTOR);
                    pyResult.append(magZ * MAG_SCALE_FACTOR);
                }
                
                return pyResult;
            }

            py::list get_temp_data(void) {
                py::list pyResult;
                pyResult.append(_data.temperature.load());
                return pyResult;
            }

            double get_max_frequency(void) {
                double maxFreq = 0.0;
                if (get_accel_frequency() > maxFreq)    maxFreq = get_accel_frequency();
                if (get_gyro_frequency() > maxFreq)     maxFreq = get_gyro_frequency();
                if (get_mag_frequency() > maxFreq)      maxFreq = get_mag_frequency();
                return maxFreq;
            }
            
    };
}
#endif