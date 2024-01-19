Script autodetects networking device (router, switch, firewall) and vendor (Cisco, Arista, Junos);

It updates the device configuration without knowing what type of device we are connecting to ahead of time.

It does this by using pre-built Jinja2 configuration files, and YAML files for the variables.  Example:  

Arista device example:  

{% if router_bgp %}<br>
### Arista BGP Configuration<br>
```markdown
router bgp {{ bgp_as_number }}<br>
{% if bgp_router_id %}<br>
  bgp router-id {{ bgp_router_id }}<br>
{% endif %}<br>
{% for neighbor in bgp_neighbors %}<br>
  neighbor {{ neighbor.ip }} remote-as {{ neighbor.as_number }}<br>
  {% if neighbor.description %}<br>
    description {{ neighbor.description }}<br>
  {% endif %}<br>
  {% if neighbor.update_source %}<br>
    update-source {{ neighbor.update_source }}<br>
  {% endif %}<br>
  {% if neighbor.password %}<br>
    password {{ neighbor.password }}<br>
  {% endif %}<br>
  {% if neighbor.route_map_in %}<br>
    route-map {{ neighbor.route_map_in }} in<br>
  {% endif %}<br>
  {% if neighbor.route_map_out %}<br>
    route-map {{ neighbor.route_map_out }} out<br>
  {% endif %}<br>
{% endfor %}<br>
```<br>
Thi



Arista YAML for BGP:

```yaml
router_bgp:
  bgp_as_number: 65001
  bgp_router_id: 1.1.1.1
  bgp_neighbors:
    - ip: 192.168.2.1
      as_number: 65002
      description: Neighbor 1
      update_source: Loopback0
      password: secret
      route_map_in: inbound_map
      # ...
      # ...
      # ...

     



  The same YAML can be used for different vendors and the script automatically detects what it is connecting to and picks the associated Jinja template.  
  The Jinja template has been built using AI, to pick out the most relevant and used configurations.
  This script is good for pushing out validated configurations, especially in mixed vendor environments with frequent changes. We do not need to know the device type or vendor ahead of time - the script handles that.  It  
  can then conditionally update devices (edge, distribution, core, routing conditions). It is ready to be integrated into exisating workflows, or invoked as an Ansible module.


    Code is located in main_handler.py
