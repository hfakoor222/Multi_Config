Script autodetects networking device (router, switch, firewall) and vendor (Cisco, Arista, Junos);

It updates the device configuration without knowing what type of device we are connecting to ahead of time.

It does this by using pre-built Jinja2 configuration files, and YAML files for the variables.  Example:  


### Arista BGP Jinja File<br>
```markdown
router bgp {{ bgp_as_number }}
{% if bgp_router_id %}
  bgp router-id {{ bgp_router_id }}
{% endif %}
{% for neighbor in bgp_neighbors %}
  neighbor {{ neighbor.ip }} remote-as {{ neighbor.as_number }}
  {% if neighbor.description %}
    description {{ neighbor.description }}
  {% endif %}
  {% if neighbor.update_source %}
    update-source {{ neighbor.update_source }}
  {% endif %}
  {% if neighbor.password %}
    password {{ neighbor.password }}
  {% endif %}
  {% if neighbor.route_map_in %}
    route-map {{ neighbor.route_map_in }} in
  {% endif %}
  {% if neighbor.route_map_out %}
    route-map {{ neighbor.route_map_out }} out
  {% endif %}
{% endfor %}
```


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


```

 The same YAML can be used for different vendors and the script automatically detects what it is connecting to and picks the associated Jinja template.  
 
  The Jinja template has been built using AI, to pick out the most relevant and used configurations.  
  
  This script is good for pushing out validated configurations, especially in mixed vendor environments with frequent changes. We do not need to know the device type or vendor ahead of time - the script handles that.  It  
  can then conditionally update devices (edge, distribution, core, routing conditions).  
    
    It is ready to be integrated into exisating workflows, or invoked as an Ansible module.   
    
    
    The script is threaded and runs multiple configrations at once.


    Code is located in main_handler.py

##



