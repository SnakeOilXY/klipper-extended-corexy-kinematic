# Introduction to extended-coreXY
 In the SnakeOilXY beta3 release, we added support/upgrade options for <code>SnakeOilXY IDEX</code> (using hybrid_coreXY kinematic) and <code>SnakeOilXY 4PR</code> (using extended_coreXY kinematic).  
 Extended Corexy(name might be changed when merged into klipper main branch) is a mix of traditional coreXY and hybrid coreXY.
Before explained what is extended coreXY and it's benefit, let's check the traditional coreXY and 4 motors coreXY (aslo called AWD coreXY or 4WD coreXY) concept and their benefits.

### Traditional Corexy

![coreXY](./corexy.png)
- With stationary motors, we have less moving mass compared to bed-slinger machine and result in have faster max speed and higher max acceleration without losing print quality.
- It's hard to keep the same performance when scale up the machine because increase of the gantry mass and longer belt path.

### 4 motors coreXY
![awd-coreXY](./awd-corexy.png)
- By adding 2 more motor, we have more torque and shorter motor-to-toolhead belt path. 
- This setup is effective, simple, and easy to adapt to current core system.  
- But we cannot set independent speed/acceleration for X and Y axis(yet) the whole system performance need to be lower to match Y axis performance(the same as traditional coreXY).

### Extended coreXY
![extended-coreXY](./extended_corexy.png)
- The ideal of extended coreXY is instead of adding power to both X and Y axis, we add 2 motors to support the heavy Y axis only. And with less load on AB motors, we also will have some boost on X axis too.  
- Compare to 4 motors coreXY, extended coreXY will require more parts and modify to the current system to add 2 extra motors. Tuning belt tension also need more effort than tuning for other coreXY setup.
- With independent endstop of left and right of Y axis, we can square the gantry with homing.
- Another benefit of extended coreXY is the system can be easily switched to IDEX hybrid coreXY just by adding 1 more toolhead as the image bellow.

![idex-coreXY](./idex-corexy.png)


