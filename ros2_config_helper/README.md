# ros2_config_helper

This tool is intended to help users configure DDS correctly for their need.
It will generate a DDS XML profiles file based on the answer on some questions.

To run the tool, after sourcing the workspace were the package was built:

```
ros2 run ros2_config_helper -o <OUTPUT_DIR>
```

If you do not want to build a ROS 2 workspace, you can do:

```
python3 -m ros2_config_helper.main -o <OUTPUT_DIR>
```

By default, it will generate files for both FastDDS and CycloneDDS.
That can be controlled using the `--backends/-b` option.

For each backend, the files `setup_env.bash` and `profiles.xml` are created in the directory `<OUTPUT_DIR>/<BACKEND_NAME>`.
The `setup_env.bash` file can be sourced, so all nodes run use those settings.

If you're generating a file for another computer, use the `--remote-computer/-r` option.
That will do not check if the network interfaces are correct.

For more options, see `--help`.
