#!/usr/bin/env python3
"""Publish the K1 robot description (robot_state_publisher).

Args:
  robot_ns  frame prefix for links/joints (default k1_0)
  gui       also start joint_state_publisher_gui + RViz2 (default true).
            Bringup launches pass gui:=false: on a sim or real robot the GUI
            would publish /joint_states alongside the actual robot state.
"""
import os
import re

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

URDF = os.path.join('assets', 'robots', 'K1', 'K1_22dof.urdf')


def robot_description(share: str) -> str:
    """K1 URDF with relative mesh paths rewritten to absolute file:// URIs."""
    path = os.path.join(share, URDF)
    mesh_dir = os.path.join(os.path.dirname(path), 'meshes')
    with open(path) as f:
        return re.sub(r'filename="meshes/', f'filename="file://{mesh_dir}/', f.read())


def _rsp(context):
    share = get_package_share_directory('k1_description')
    ns = LaunchConfiguration('robot_ns').perform(context)
    return [Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description(share),
                     'frame_prefix': f'{ns}/' if ns else ''}],
    )]


def generate_launch_description():
    gui = IfCondition(LaunchConfiguration('gui'))
    rviz_config = os.path.join(get_package_share_directory('k1_description'),
                               'config', 'view_robot.rviz')
    rviz_args = ['-d', rviz_config] if os.path.exists(rviz_config) else []
    return LaunchDescription([
        DeclareLaunchArgument('robot_ns', default_value='k1_0',
                              description='Frame prefix for links and joints'),
        DeclareLaunchArgument('gui', default_value='true',
                              description='Start joint_state_publisher_gui and RViz2'),
        OpaqueFunction(function=_rsp),
        Node(package='joint_state_publisher_gui',
             executable='joint_state_publisher_gui', condition=gui),
        Node(package='rviz2', executable='rviz2', arguments=rviz_args,
             output='screen', condition=gui),
    ])
