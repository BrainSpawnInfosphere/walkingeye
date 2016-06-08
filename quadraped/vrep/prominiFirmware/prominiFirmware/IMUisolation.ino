#include <math.h>

#define GYR_CMPFM_FACTOR 250

//****** end of advanced users settings *************
#define INV_GYR_CMPF_FACTOR   (1.0f / (GYR_CMPF_FACTOR  + 1.0f))
#define INV_GYR_CMPFM_FACTOR  (1.0f / (GYR_CMPFM_FACTOR + 1.0f))
#define MAG_DECLINIATION 0.0f


static int16_t  gyroADC[3],gyroZero[3],magZero[3],accZero[3],accADC[3],accAngle[3],accSmooth[3],magADC[3],gyroAngle[3],gyroData[3],gyroSmooth[3],gyroADCprevious[3],angleTrim[3];
static int16_t acc_1G = 200,annex650_overrun_count =0;
static int16_t pos[3], angle[3], vel[3];
unsigned long int start,lastpid;
int SMALL_ANGLES_25=0;
unsigned long int lastUpdate = 0,cicletime=0;
static int32_t calib_sum[3] ={0,0,0};
int calib_counter=0,axis=0,calibrated=0;
float dt;
static uint16_t acc_25deg = acc_1G * 0.423;
static int16_t  heading;
static uint32_t currentTime = 0;
static uint16_t previousTime = 0;


typedef struct fp_vector {		
  float X,Y,Z;		
} t_fp_vector_def;

typedef union {		
  float A[3];		
  t_fp_vector_def V;		
} t_fp_vector;

typedef struct int32_t_vector {
  int32_t X,Y,Z;
} t_int32_t_vector_def;

typedef union {
  int32_t A[3];
  t_int32_t_vector_def V;
} t_int32_t_vector;

static t_int32_t_vector EstM32;
static t_fp_vector EstM;


#define GYRO_SCALE ((2279 * PI)/((32767.0f / 4.0f ) * 180.0f * 1000000.0f)) //(ITG3200 and MPU6050)
#define GYR_CMPF_FACTOR 600
#define INV_GYR_CMPF_FACTOR   (1.0f / (GYR_CMPF_FACTOR  + 1.0f))
#define INV_GYR_CMPFM_FACTOR  (1.0f / (GYR_CMPFM_FACTOR + 1.0f))
#define ACC_LPF_FACTOR 4

static uint32_t neutralizeTime = 0,i2c_errors_count = 0;

enum rc {
  ROLL,
  PITCH,
  YAW,
  THROTTLE,
  AUX1,
  AUX2,
  AUX3,
  AUX4
};

void imu_setup(){
  delay(1000);
  i2c_init();
  for(int axis=0;axis<3;axis++){
    gyroZero[axis] =0;
    accSmooth[axis] = 0;
    pos[axis] = 0;
 //   attitude[axis] = 0;
    vel[axis]= 0;
  }
  start = 0;
  Gyro_init();
  ACC_init();
  //Mag_init();
  Serial.begin(115200);
}

//void printStuff(){
//
//Serial.print("gyro:");
//Serial.print(gyroADC[0]);
//Serial.print(", ");
//Serial.print(gyroData[1]);
//Serial.print(", ");
//Serial.println(gyroData[2]);
//
//Serial.print("gyroAngle:");
//Serial.print(gyroAngle[0]);
//Serial.print(", ");
//Serial.print(gyroAngle[1]);
//Serial.print(", ");
//Serial.println(gyroAngle[2]);
//
//Serial.print("acc:");
//Serial.print(accSmooth[0]);
//Serial.print(", ");
//Serial.print(accSmooth[1]);
//Serial.print(", ");
//Serial.println(accSmooth[2]);
//
//Serial.print("i2cErrors");
//Serial.println(i2c_errors_count);
//}
//
//void printPos(){
//  Serial.print("vel:");
//  Serial.print(vel[0]);
//  Serial.print(", ");
//  Serial.print(vel[1]);
//  Serial.print(", ");
//  Serial.println(vel[2]);
//  Serial.print("accAngle:");
//  Serial.print(accAngle[0]);
//  Serial.print(", ");
//  Serial.print(accAngle[1]);
//  Serial.print(", ");
//  Serial.println(accAngle[2]);
//  Serial.print("angle:");
//  Serial.print(angle[0]);
//  Serial.print(", ");
//  Serial.print(angle[1]);
//  Serial.print(", ");
//  Serial.println(angle[2]);
//  Serial.print("time:");
//  Serial.println(dt);
//  Serial.print("heading:");
//  Serial.println(heading);
//  Serial.println("end");
//}
//

float erro=0,ref=0,integral=0,old_erro=0,derivada,input;


void imu_loop(){
  Gyro_getADC();
  ACC_getADC();
  //Mag_getADC();
  //imu();
  computeIMU();
  // Measure loop rate just afer reading the sensors
//  currentTime = micros();
//  //cycleTime = currentTime - previousTime;
//  previousTime = currentTime;
//
//  if (millis()>start+50)
//  {
//    //printStuff();
//    //printPos();
//    //printStuff();
//
//    start= millis() ;
//   }
   //set_servo();
   delay(10);
}







int16_t _atan2(int32_t y, int32_t x){
  float z = (float)y / x;
  int16_t a;
  if ( abs(y) < abs(x) ){
     a = 573 * z / (1.0f + 0.28f * z * z);
   if (x<0) {
     if (y<0) a -= 1800;
     else a += 1800;
   }
  } else {
   a = 900 - 573 * z / (z * z + 0.28f);
   if (y<0) a -= 1800;
  }
  return a;
}

float InvSqrt (float x){ 
  union{  
    int32_t i;  
    float   f; 
  } conv; 
  conv.f = x; 
  conv.i = 0x5f3759df - (conv.i >> 1); 
  return 0.5f * conv.f * (3.0f - x * conv.f * conv.f);
}

// Rotate Estimated vector(s) with small angle approximation, according to the gyro data
void rotateV(struct fp_vector *v,float* delta) {
  fp_vector v_tmp = *v;
  v->Z -= delta[ROLL]  * v_tmp.X + delta[PITCH] * v_tmp.Y;
  v->X += delta[ROLL]  * v_tmp.Z - delta[YAW]   * v_tmp.Y;
  v->Y += delta[PITCH] * v_tmp.Z + delta[YAW]   * v_tmp.X;
}


static int32_t accLPF32[3]    = {0, 0, 1};
static float invG; // 1/|G|

static t_fp_vector EstG;
static t_int32_t_vector EstG32;

void computeIMU () {
  uint8_t axis;
  static int16_t gyroADCprevious[3] = {0,0,0};
  int16_t gyroADCp[3];
  int16_t gyroADCinter[3];
  static uint32_t timeInterleave = 0;

  //we separate the 2 situations because reading gyro values with a gyro only setup can be acchieved at a higher rate
  //gyro+nunchuk: we must wait for a quite high delay betwwen 2 reads to get both WM+ and Nunchuk data. It works with 3ms
  //gyro only: the delay to read 2 consecutive values can be reduced to only 0.65ms


      ACC_getADC();
      getEstimatedAttitude();
      Gyro_getADC();
    for (axis = 0; axis < 3; axis++)
      gyroADCp[axis] =  gyroADC[axis];
    timeInterleave=micros();
    if ((micros()-timeInterleave)>650) {
       annex650_overrun_count++;
    } else {
       while((micros()-timeInterleave)<650) ; //empirical, interleaving delay between 2 consecutive reads
    }
      Gyro_getADC();
    for (axis = 0; axis < 3; axis++) {
      gyroADCinter[axis] =  gyroADC[axis]+gyroADCp[axis];
      // empirical, we take a weighted value of the current and the previous values
      gyroData[axis] = (gyroADCinter[axis]+gyroADCprevious[axis])/3;
      gyroADCprevious[axis] = gyroADCinter[axis]>>1;
      accADC[axis]=0;
    }



}



void getEstimatedAttitude(){
  uint8_t axis;
  int32_t accMag = 0;
  float scale, deltaGyroAngle[3];
  static uint16_t previousT;
  uint16_t currentT = micros();

  scale = (currentT - previousT) * GYRO_SCALE;
  previousT = currentT;

  // Initialization
  for (axis = 0; axis < 3; axis++) {
    deltaGyroAngle[axis] = gyroADC[axis]  * scale;

    accLPF32[axis]    -= accLPF32[axis]>>ACC_LPF_FACTOR;
    accLPF32[axis]    += accADC[axis];
    accSmooth[axis]    = accLPF32[axis]>>ACC_LPF_FACTOR;

    accMag += (int32_t)accSmooth[axis]*accSmooth[axis] ;
  }
  accMag = accMag*100/((int32_t)acc_1G*acc_1G);

  rotateV(&EstG.V,deltaGyroAngle);
  rotateV(&EstM.V,deltaGyroAngle);

  if ( abs(accSmooth[ROLL])<acc_25deg && abs(accSmooth[PITCH])<acc_25deg && accSmooth[YAW]>0) {
    SMALL_ANGLES_25 = 1;
  } else {
    SMALL_ANGLES_25 = 0;
  }

  // Apply complimentary filter (Gyro drift correction)
  // If accel magnitude >1.15G or <0.85G and ACC vector outside of the limit range => we neutralize the effect of accelerometers in the angle estimation.
  // To do that, we just skip filter, as EstV already rotated by Gyro
  if (  72 < accMag && accMag < 133 )
    for (axis = 0; axis < 3; axis++) {
      EstG.A[axis] = (EstG.A[axis] * GYR_CMPF_FACTOR + accSmooth[axis]) * INV_GYR_CMPF_FACTOR;
    }
    for (axis = 0; axis < 3; axis++) {
      EstM.A[axis] = (EstM.A[axis] * GYR_CMPFM_FACTOR  + magADC[axis]) * INV_GYR_CMPFM_FACTOR;
      EstM32.A[axis] = EstM.A[axis];
    }

  for (axis = 0; axis < 3; axis++)
    EstG32.A[axis] = EstG.A[axis]; //int32_t cross calculation is a little bit faster than float	

  // Attitude of the estimated vector
  int32_t sqGZ = sq(EstG32.V.Z);
  int32_t sqGX = sq(EstG32.V.X);
  int32_t sqGY = sq(EstG32.V.Y);
  int32_t sqGX_sqGZ = sqGX + sqGZ;
  float invmagXZ  = InvSqrt(sqGX_sqGZ);
  invG = InvSqrt(sqGX_sqGZ + sqGY);
  angle[ROLL]  = _atan2(EstG32.V.X , EstG32.V.Z);
  angle[PITCH] = _atan2(EstG32.V.Y , invmagXZ*sqGX_sqGZ);
  
    heading = _atan2(
    EstM32.V.Z * EstG32.V.X - EstM32.V.X * EstG32.V.Z,
    EstM32.V.Y * invG * sqGX_sqGZ  - (EstM32.V.X * EstG32.V.X + EstM32.V.Z * EstG32.V.Z) * invG * EstG32.V.Y ); 
    heading += MAG_DECLINIATION * 10; //add declination
    heading = heading /10;

}





void respond_with_imu()
{
    Serial.print("imu:");
    Serial.print(angle[0]);
    Serial.print(", ");
    Serial.print(angle[1]);
    Serial.print(", ");
    Serial.print(angle[2]);
    Serial.print("!<");
}





