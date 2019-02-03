#define Kp 4                           // experiment to determine this, start by something small that just makes your bot follow the line at a slow speed
#define Kd 16                          // experiment to determine this, slowly increase the speeds and adjust this value. ( Note: Kp < Kd) 

#define left_line_sensor A0
#define center_line_sensor A1
#define right_line_sensor A2

#define right_motor_max_pwm 255
#define left_motor_max_pwm 255
#define right_motor_base_pwm 210
#define left_motor_base_pwm 210

#define forward_right_motor 7
#define backward_right_motor 12
#define enable_right_motor 2

#define forward_left_motor 11
#define backward_left_motor 12
#define enable_left_motor 3

#define buzzer X
#define red_led R
#define green_led G
#define blue_led B


int left_sensor_threshold;
int center_sensor_threshold;
int right_sensor_threshold;
int robot_movement_direction = 0;
int lastError = 0;

void setup()
{
  pinMode(forward_right_motor, OUTPUT);
  pinMode(backward_right_motor, OUTPUT);
  pinMode(enable_right_motor, OUTPUT);
  pinMode(forward_left_motor, OUTPUT);
  pinMode(backward_left_motor, OUTPUT);
  pinMode(enable_left_motor, OUTPUT);

  line_sensor_calibrate();
  initialize_pick_place();
}

void loop()
{
  
}

int movement()
{
  int error = get_bot_position();
  int right_motor_pwm = 0;
  int left_motor_pwm = 0;
  if (abs(error) < 2)
  {
     int motorSpeed = Kp * error + Kd * (error - lastError);
     lastError = error;
     if (robot_movement_direction == 1)                           // 1 - Forward
     {
        right_motor_pwm = right_motor_base_pwm + motorSpeed;
        left_motor_pwm = left_motor_base_pwm - motorSpeed;
        set_movement_direction();
     }
     else if (robot_movement_direction == -1)                     // -1 - Backward
     {
        right_motor_pwm = right_motor_base_pwm - motorSpeed;
        left_motor_pwm = left_motor_base_pwm + motorSpeed;
        set_movement_direction();
     }
     
     if (right_motor_pwm > right_motor_max_pwm )
        right_motor_pwm = right_motor_max_pwm;                    // prevent the motor from going beyond max speed
     if (left_motor_pwm > left_motor_max_pwm )
        left_motor_pwm = left_motor_max_pwm;
     if (right_motor_pwm < 0)
        right_motor_pwm = 0;                                      // keep the motor speed positive
     if (left_motor_pwm < 0)
        left_motor_pwm = 0;

     analogWrite(enable_left_motor, left_motor_pwm);
     analogWrite(enable_right_motor, right_motor_pwm);
  }
  else
  {
    robot_movement_direction = 0;
    set_movement_direction();
    return 0;
  }
}

void line_sensor_calibrate()
{
  int left_white_value = 0, left_black_value = 0;
  int center_white_value = 0, center_black_value = 0;
  int right_white_value = 0, right_black_value = 0;

  left_white_value = analogRead(left_line_sensor);
  center_white_value = analogRead(center_line_sensor);
  right_white_value = analogRead(right_line_sensor);

  robot_movement_direction = 1;
  set_movement_direction();
  
  digitalWrite(enable_right_motor, HIGH);
  digitalWrite(enable_left_motor, HIGH);
  
  delay(80);                                         // 80 ms (for approx 1.5 cms)
  
  robot_movement_direction = 0;
  set_movement_direction();
  
  left_black_value = analogRead(left_line_sensor);
  center_black_value = analogRead(center_line_sensor);
  right_black_value = analogRead(right_line_sensor);

  left_sensor_threshold = ((left_black_value + left_white_value) / 2) - (left_white_value / 3);
  center_sensor_threshold = ((center_black_value + center_white_value) / 2) - (center_white_value / 3);
  right_sensor_threshold = ((right_black_value + right_white_value) / 2) - (right_white_value / 3);
}

void set_movement_direction()
{
   if (robot_movement_direction == 1)               // 1 - Forward
   {
      digitalWrite(forward_right_motor, HIGH);
      digitalWrite(backward_right_motor, LOW);
      digitalWrite(forward_left_motor, HIGH);
      digitalWrite(backward_left_motor, LOW);
   }
   else if (robot_movement_direction == -1)         // -1 - Backward
   {
      digitalWrite(forward_right_motor, LOW);
      digitalWrite(backward_right_motor, HIGH);
      digitalWrite(forward_left_motor, LOW);
      digitalWrite(backward_left_motor, HIGH);
   }
   else if (robot_movement_direction == 0)          // 0 - Stop
   {
      digitalWrite(enable_right_motor, LOW);
      digitalWrite(enable_left_motor, LOW);
   }
}


int get_bot_position()
{
  int left_sensor_value = analogRead(left_line_sensor);
  int center_sensor_value = analogRead(center_line_sensor);
  int right_sensor_value = analogRead(right_line_sensor);

  /*  Black Line: "Greater than/equal to" sensor_threshold
   *  White Line: "Lesser than/equal to" sensor_threshold
   */
  
  if (left_sensor_value <= left_sensor_threshold &&
      center_sensor_value <= center_sensor_threshold &&
      right_sensor_value >= right_sensor_threshold)
  {
    // RIGHT CONDITION;
    return 1;
  }
  
  else if (left_sensor_value <= left_sensor_threshold &&
           center_sensor_value >= center_sensor_threshold &&
           right_sensor_value <= right_sensor_threshold)
  {
    // STRAIGHT LINE CONDITION;
    return 0;
  }
  
  else if (left_sensor_value >= left_sensor_threshold &&
           center_sensor_value <= center_sensor_threshold &&
           right_sensor_value <= right_sensor_threshold)
  {
    // LEFT CONDITION;
    return -1;
  }
  
  else if (left_sensor_value <= left_sensor_threshold &&
           center_sensor_value >= center_sensor_threshold &&
           right_sensor_value >= right_sensor_threshold)
  {
    // RIGHT BRANCHED-NODE CONDITION;
    return 2;
  }
  
  else if (left_sensor_value >= left_sensor_threshold &&
           center_sensor_value >= center_sensor_threshold &&
           right_sensor_value <= right_sensor_threshold)
  {
    // LEFT BRANCHED-NODE CONDITION;
    return -2;
  }
  
  else if ((left_sensor_value >= left_sensor_threshold &&
            center_sensor_value >= center_sensor_threshold &&
            right_sensor_value >= right_sensor_threshold)
  {
    // T-NODE CONDITION;
    return 3;
  }

  else if ((left_sensor_value <= left_sensor_threshold &&
            center_sensor_value <= center_sensor_threshold &&
            right_sensor_value <= right_sensor_threshold)
  {
    // WHITE SPACE CONDITION;
    return -3;
  }
}
