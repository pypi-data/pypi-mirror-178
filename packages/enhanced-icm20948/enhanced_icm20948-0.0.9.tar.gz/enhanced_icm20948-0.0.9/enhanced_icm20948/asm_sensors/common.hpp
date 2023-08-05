#ifndef _COMMON_HPP_
#define _COMMON_HPP_


#include "mraa/common.hpp"
#include "mraa/i2c.hpp"
#include <iostream>
#include <unistd.h>
#include <assert.h>
#include <algorithm>
#include <cstdlib>
#include <cstdio>
#include <cstdint>
#include <string>
#include <vector>
#include <map>
#include <thread>
#include <mutex>
#include <atomic>
#include <pybind11/pybind11.h>

namespace py = pybind11;

uint8_t sensorId = 0;

class SensorBatch;
class Sensor {
    protected:
        uint8_t _sensorId;
        uint8_t _i2cBus;
        uint8_t _i2cAddress;

        std::atomic<bool> _isReading;
        
        friend class SensorBatch;
        friend void sensor_reading_thread(std::atomic<bool>&, std::vector<Sensor*>&, std::atomic<double>&);
        virtual void _sync_read_data(mraa::I2c& i2cBus) {

        }
        virtual void _async_read_data(mraa::I2c& i2cBus) {

        }
        virtual void _await_read_data(mraa::I2c& i2cBus) {

        }
        virtual void _init(mraa::I2c& i2cBus) {
            
        }
        virtual void _configure(mraa::I2c& i2cBus) {

        }
        virtual void _close(mraa::I2c& i2cBus) {

        }
    public:
        std::string sensorName;
        Sensor(uint8_t i2cBus, uint8_t i2cAddress)
        : _i2cBus(i2cBus), _i2cAddress(i2cAddress)
        {
            sensorName = "Sensor" + std::to_string(sensorId);
            _sensorId = sensorId;
            sensorId++;
        }
        
        virtual uint8_t get_sensor_id(void) const {
            return  _sensorId;
        }
        virtual uint8_t get_i2c_address(void) const {
            return _i2cAddress;
        }
        virtual uint8_t get_i2c_bus(void) const {
            return _i2cBus;
        }
        virtual double get_max_frequency(void) {
            return 0.0;
        }

};

void sensor_reading_thread(std::atomic<bool>& terminate, std::vector<Sensor*>& sensorPtrArray, std::atomic<double>& internalMaxFreq) {
    int sensorArraySize = sensorPtrArray.size();
    double sensorMaxFreq = 0.0;
    internalMaxFreq = 1e6;
    mraa::I2c i2cBus(sensorPtrArray[0]->_i2cBus);
    for (int i = 0; i < sensorArraySize; i++) {
        sensorPtrArray[i]->_init(i2cBus);
        sensorPtrArray[i]->_configure(i2cBus);
    }

    for (int i = 0; i < sensorArraySize; i++) {
        if (sensorMaxFreq < sensorPtrArray[i]->get_max_frequency()) {
            sensorMaxFreq = sensorPtrArray[i]->get_max_frequency();
        }
    }

    while (!terminate.load()) {
        auto start = std::chrono::system_clock::now();
        for (int i = 0; i < sensorArraySize; i++) {
            sensorPtrArray[i]->_async_read_data(i2cBus);
        }

        for (int i = 0; i < sensorArraySize; i++) {
            sensorPtrArray[i]->_sync_read_data(i2cBus);
        }

        for (int i = 0; i < sensorArraySize; i++) {
            sensorPtrArray[i]->_await_read_data(i2cBus);
        }
        auto end = std::chrono::system_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
        internalMaxFreq = 1e6 / duration.count();
        // if (internalMaxFreq.load() > sensorMaxFreq) {
        //     double restTime = (1e6 / sensorMaxFreq - 1e6 / internalMaxFreq.load()) / 2.0;
        //     std::this_thread::sleep_for(std::chrono::microseconds((int64_t)(restTime)));
        // }
    }

    for (int i = 0; i < sensorArraySize; i++) {
        sensorPtrArray[i]->_close(i2cBus);
    }
}

class SensorBatch {
    protected:
        std::map<uint8_t, std::vector<Sensor*>> _sensorPtrMap;
        std::thread* _threadPool;
        std::atomic<bool>* _terminateArray;
        std::atomic<double>* _internalMaxFreq;
        bool _isReading;
    public:
        SensorBatch() 
        : _threadPool(nullptr), _terminateArray(nullptr), _internalMaxFreq(nullptr), _isReading(false)
        {}
        template <typename T>
        bool add_sensor(T& sensor) {
            if (_isReading) {
                fprintf(stderr, "%s -> Warning: Invalid Operation: Sensor is Running\n", sensor.sensorName.c_str());
                return false;
            }
            auto busIndexFound = _sensorPtrMap.find(sensor._i2cBus);
            if (busIndexFound == _sensorPtrMap.end()) {
                _sensorPtrMap.insert(std::pair<uint8_t, std::vector<Sensor*>>(sensor._i2cBus, std::vector<Sensor*>()));
            } else {
                int sensorArraySize = busIndexFound->second.size();
                for (int i = 0; i < sensorArraySize; i++) {
                    if (_sensorPtrMap[sensor._i2cBus][i]->_i2cAddress == sensor._i2cAddress) {
                        fprintf(stderr, "Warning: I2C Address Conflict on `i2c-%hhu` Detected! Sensor: `%s` will NOT be added!\n", sensor._i2cBus, sensor.sensorName.c_str());
                        return false;
                    }
                }
            }
            _sensorPtrMap[sensor._i2cBus].push_back(&sensor);
            return true;
        }
        bool start_reading() {
            _isReading = true;
            int mapElementSize = _sensorPtrMap.size();
            int busIndex = 0;
            _threadPool = new std::thread[mapElementSize];
            _terminateArray = new std::atomic<bool>[mapElementSize];
            _internalMaxFreq = new std::atomic<double>[mapElementSize];
            for (auto iter = _sensorPtrMap.begin(); iter != _sensorPtrMap.end(); iter++) {
                _terminateArray[busIndex] = false;
                _internalMaxFreq[busIndex] = 0.0;
                _threadPool[busIndex] = std::thread(
                    sensor_reading_thread,
                    std::ref(_terminateArray[busIndex]),
                    std::ref(iter->second),
                    std::ref(_internalMaxFreq[busIndex])
                );
                busIndex++;
            }
            return true;
        }
        bool stop_reading() {
            if (_terminateArray == nullptr || _threadPool == nullptr || _internalMaxFreq == nullptr) {
                fprintf(stderr, "Warning: Nothing to Stop!\n");
                return false;
            }
            int mapElementSize = _sensorPtrMap.size();
            for (int i = 0; i < mapElementSize; i++) {
                _terminateArray[i] = true;
            }
            for (int i = 0; i < mapElementSize; i++) {
                _threadPool[i].join();
            }

            delete [] _terminateArray;
            delete [] _threadPool;
            delete [] _internalMaxFreq;

            _terminateArray = nullptr;
            _threadPool = nullptr;
            _internalMaxFreq = nullptr;

            _isReading = false;

            return true;
        }

        double get_max_frequency(void) {
            double maxFreq = 1e10;
            int mapElementSize = _sensorPtrMap.size();
            for (int i = 0; i < mapElementSize; i++) {
                double freq = _internalMaxFreq[i].load();
                if (freq < maxFreq) {
                    maxFreq = freq;
                }
            }
            return maxFreq;
        }
};

#endif