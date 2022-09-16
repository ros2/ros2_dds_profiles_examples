# ros2_dds_profiles_examples

This repo contains examples of how to configure DDS for different use cases using a profiles file.

## Use cases covered

This repo provides examples to configure DDS for four different use cases:

* `localhost_isolated.xml`: Discovery restricted to localhost.
  This is really useful for development, if you want to avoid collisions with other ROS 2 users in the same network.
* `localhost_isolated_addressable_from_another_host.xml` (*): Discovery restricted to localhost, but still being able to connect from another host if the IP address of the machine is specified.
  This is basically avoiding to use multicast discovery, but still allowing unicast discovery in a network interface that can be chosen by the user.
* `unicast_discovery_from_another_host.xml` (*): Profile to connect to the above case, and still not cause collisions with other machines in the network.
  This example can be extended and be used to connect a set of hosts using unicast discovery and avoiding multicast.
  It's important to remember that DDS discovery can be asymmetric.
  i.e. you don't need to list all peers in all machines, as all nodes have one common peer discovery will work.
  Though it's better to list a few peers of the group at least, to make sure discovery works even if one of the peers is down.
* `multicast_discover_filtered_interfaces.xml` (*): Multicast discovery, restricted to some network interfaces.

(*) These profiles files require the user to make some edits in order to work.
Generally, they only require modifying some IP addresses.

## DDS vendors supported

There are examples available for:

* FastDDS (rmw_fastrtps_cpp/rmw_fastrtps_dynamic_cpp)
* CycloneDDS (rmw_cyclonedds_cpp)

### FastDDS

```bash
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
export FASTRTPS_DEFAULT_PROFILES_FILE=/path/to/profiles/file.xml
```

### CycloneDDS

```bash
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
export CYCLONEDDS_URI=file:///path/to/profile/file.xml
```

### Compatibility

You can mix nodes using CycloneDDS/FastDDS, they all work as expected as far as tested.

## Testing the settings with docker

If you want to test host-to-host communication using docker make sure to:

* Use a bridge network when running the container.
  You can use the default bridge, in which case you do not need to add anything to your `docker run` command.
  Or to make sure you're using the default bridge, add `--network=bridge`.
  Alternative you can create your own bridge network, see https://docs.docker.com/network/bridge/.
* Update the profiles file with the correct IP addresses.
