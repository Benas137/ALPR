#include <wiringPi.h>
#include <iostream>
#include <chrono>
#include <thread>
#include <cstdlib>

using namespace std::chrono_literals;

const int TRIG = 27;
const int ECHO = 17;

void measure_distance()
{
    // set the trigger pin high for 10 microseconds
    digitalWrite(TRIG, HIGH);
    std::this_thread::sleep_for(10us);
    digitalWrite(TRIG, LOW);

    // measure the time it takes for the echo pin to go from low to high
    auto start = std::chrono::high_resolution_clock::now();
    while (digitalRead(ECHO) == LOW) {
        start = std::chrono::high_resolution_clock::now();
    }

    auto stop = std::chrono::high_resolution_clock::now();
    while (digitalRead(ECHO) == HIGH) {
        stop = std::chrono::high_resolution_clock::now();
    }

    // calculate the distance based on the speed of sound
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(stop - start);
    float distance = duration.count() * 0.034 / 2;

    std::cout << "Measured Distance = " << distance << " cm" << std::endl;

    if (distance <= 100) {
        std::this_thread::sleep_for(3s);
        std::system("python3 /home/admin/Desktop/ALPR/ALPR_Project/db_main.py");
    }
}

int main()
{
    // setup GPIO
    wiringPiSetupGpio();
    pinMode(TRIG, OUTPUT);
    pinMode(ECHO, INPUT);

    // set the trigger pin low to start
    digitalWrite(TRIG, LOW);

    // wait for the sensor to settle
    std::this_thread::sleep_for(2s);

    // main loop
    while (true) {
        measure_distance();
        std::this_thread::sleep_for(100ms);
    }

    // cleanup the GPIO pins when you're done
    pinMode(TRIG, INPUT);
    pinMode(ECHO, INPUT);
}
