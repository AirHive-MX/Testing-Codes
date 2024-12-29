#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;

void setup() {
  Serial.begin(9600);
  Wire.begin();

  if (!mpu.begin()) {
    Serial.println("Failed to initialize MPU6050. Check your wiring!");
    while (1);
  }

  mpu.calcGyroOffsets(true); // Calibrate the MPU6050
  Serial.println("MPU6050 ready.");
  Serial.println("AccelX,AccelY,AccelZ,GyroX,GyroY,GyroZ");
}

void loop() {
  mpu.update();

  // Get acceleration and gyro values
  float accelX = mpu.getAccX();
  float accelY = mpu.getAccY();
  float accelZ = mpu.getAccZ();
  float gyroX = mpu.getGyroX();
  float gyroY = mpu.getGyroY();
  float gyroZ = mpu.getGyroZ();

  // Send data to Serial
  Serial.print(accelX); Serial.print(",");
  Serial.print(accelY); Serial.print(",");
  Serial.print(accelZ); Serial.print(",");
  Serial.print(gyroX); Serial.print(",");
  Serial.print(gyroY); Serial.print(",");
  Serial.println(gyroZ);

  delay(10); // Adjust to control data rate
}
