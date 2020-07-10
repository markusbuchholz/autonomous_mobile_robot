# autonomous_mobile_robot
```bash
docker build . -t amr
```
jupyter lab --ip=0.0.0.0 --port=8888 --allow-root

docker run -p 8888:8888 -v `pwd`/dev_ws/src:/usr/src/app/dev_ws/src -it --rm --gpus all amr 

## First shell
Run docker
. /opt/ros/dashing/setup.bash
. /opt/ros/melodic/setup.bash
export ROS_MASTER_URI=http://192.168.0.189:11311
export DOMAIN_ID=0
ros2 run ros1_bridge dynamic_bridge --bridge-all-1to2-topics

##Second shell
. catkin_ws/devel/setup.bash
roslaunch skid_steer_bot run_world.launch

##Third shell
docker ps
docker exec
. /dev_ws/install/setup.bash
export DOMAIN_ID=0
/opt/conda/lib/python3.7
/opt/conda/lib/python3.7/site-packages
export PYTHONPATH=$PYTHONPATH:/opt/conda/lib/python3.7:/opt/conda/lib/python3.7/site-packages
export PYTHONPATH=$PYTHONPATH:/opt/conda/lib/python3.7/site-packages/torch/
