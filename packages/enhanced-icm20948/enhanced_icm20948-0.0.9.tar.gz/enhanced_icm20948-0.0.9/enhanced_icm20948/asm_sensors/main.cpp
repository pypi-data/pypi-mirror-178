#include <pybind11/pybind11.h>
#include "common.hpp"
#include "sensors.hpp"
namespace py = pybind11;


PYBIND11_MODULE(asm_sensors, m) {
    m.doc() = "An ultra-fast and powerful ICM20948 sensor reading library"; // optional module docstring

    py::class_<Sensor>(m, "Sensor")
        .def(py::init<uint8_t, uint8_t>(), py::arg("i2cBus"), py::arg("i2cAddress"))
        .def("get_sensor_id", &Sensor::get_sensor_id)
        .def("get_i2c_address", &Sensor::get_i2c_address)
        .def("get_i2c_bus", &Sensor::get_i2c_bus)
        .def_readwrite("sensorName", &Sensor::sensorName);
        
    py::class_<ICM20948::ICM20948, Sensor>(m, "ICM20948")
        .def(py::init<uint8_t, uint8_t>(), py::arg("i2cBus"), py::arg("i2cAddress") = ICM20948::ICM20948_DEFAULT_I2C_ADDRESS)
        .def("get_accel_frequency", &ICM20948::ICM20948::get_accel_frequency)
        .def("get_gyro_frequency", &ICM20948::ICM20948::get_gyro_frequency)
        .def("get_mag_frequency", &ICM20948::ICM20948::get_mag_frequency)
        .def("set_accel_frequency_divisor", &ICM20948::ICM20948::set_accel_frequency_divisor, py::arg("divisor"))
        .def("set_gyro_frequency_divisor", &ICM20948::ICM20948::set_gyro_frequency_divisor, py::arg("divisor"))
        .def("set_mag_mode", &ICM20948::ICM20948::set_mag_mode, py::arg("mode"))
        .def("get_accel_range", &ICM20948::ICM20948::get_accel_range)
        .def("get_gyro_range", &ICM20948::ICM20948::get_gyro_range)
        .def("set_accel_range", &ICM20948::ICM20948::set_accel_range, py::arg("range"))
        .def("set_gyro_range", &ICM20948::ICM20948::set_gyro_range, py::arg("range"))
        .def("get_accel_data", &ICM20948::ICM20948::get_accel_data)
        .def("get_gyro_data", &ICM20948::ICM20948::get_gyro_data)
        .def("get_mag_data", &ICM20948::ICM20948::get_mag_data)
        .def("get_temp_data", &ICM20948::ICM20948::get_temp_data)
        .def("get_max_frequency", &ICM20948::ICM20948::get_max_frequency);

    py::class_<SensorBatch>(m, "SensorBatch")
        .def(py::init())
        .def("add_sensor", &SensorBatch::add_sensor<ICM20948::ICM20948>)
        .def("start_reading", &SensorBatch::start_reading)
        .def("stop_reading", &SensorBatch::stop_reading)
        .def("get_max_frequency", &SensorBatch::get_max_frequency);

    m.attr("ICM20948_DEFAULT_I2C_ADDRESS") = ICM20948::ICM20948_DEFAULT_I2C_ADDRESS;
}