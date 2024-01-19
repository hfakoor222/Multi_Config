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

 The same YAML can be used for different vendors and the script automatically detects what it is connecting to, by using SSH port 22, and Netmiko API,  and picks the associated Jinja template.  
 
  The Jinja template has been built using AI, to pick out the most relevant and used configurations.  
  
  This script is good for pushing out validated configurations, especially in mixed vendor environments with frequent changes. We do not need to know the device type or vendor ahead of time - the script handles that.  
  
  It reads in a device list from xlsx(excel) file.
  It  can then conditionally update devices (edge, distribution, core, routing conditions).    
  
  It is ready to be integrated into existing workflows, or invoked as an Ansible module.  
    
The script is threaded and runs multiple configrations at once.


Code is located in main_handler.py




I will be posting a video soon. I will be posting a unit test script soon (validates the AI generated configurations).  The script is ready to be run. 


here is a list of all the drivers/devices it auto detects: 

Supported SSH device_type values
a10
accedian
adtran_os
adva_fsp150f2
adva_fsp150f3
alcatel_aos
alcatel_sros
allied_telesis_awplus
apresia_aeos
arista_eos
arris_cer
aruba_os
aruba_osswitch
aruba_procurve
audiocode_66
audiocode_72
audiocode_shell
avaya_ers
avaya_vsp
broadcom_icos
brocade_fastiron
brocade_fos
brocade_netiron
brocade_nos
brocade_vdx
brocade_vyos
calix_b6
casa_cmts
cdot_cros
centec_os
checkpoint_gaia
ciena_saos
cisco_asa
cisco_ftd
cisco_ios
cisco_nxos
cisco_s200
cisco_s300
cisco_tp
cisco_viptela
cisco_wlc
cisco_xe
cisco_xr
cloudgenix_ion
coriant
dell_dnos9
dell_force10
dell_isilon
dell_os10
dell_os6
dell_os9
dell_powerconnect
dell_sonic
dlink_ds
digi_transport
eltex
eltex_esr
endace
enterasys
ericsson_ipos
ericsson_mltn63
ericsson_mltn66
extreme
extreme_ers
extreme_exos
extreme_netiron
extreme_nos
extreme_slx
extreme_tierra
extreme_vdx
extreme_vsp
extreme_wing
f5_linux
f5_ltm
f5_tmsh
flexvnf
fortinet
generic
generic_termserver
hillstone_stoneos
hp_comware
hp_procurve
huawei
huawei_olt
huawei_smartax
huawei_vrp
huawei_vrpv8
ipinfusion_ocnos
juniper
juniper_junos
juniper_screenos
keymile
keymile_nos
linux
mellanox
mellanox_mlnxos
mikrotik_routeros
mikrotik_switchos
mrv_lx
mrv_optiswitch
netapp_cdot
netgear_prosafe
netscaler
nokia_srl
nokia_sros
oneaccess_oneos
ovs_linux
paloalto_panos
pluribus
quanta_mesh
rad_etx
raisecom_roap
ruckus_fastiron
ruijie_os
sixwind_os
sophos_sfos
supermicro_smis
teldat_cit
tplink_jetstream
ubiquiti_edge
ubiquiti_edgerouter
ubiquiti_edgeswitch
ubiquiti_unifiswitch
vyatta_vyos
vyos
watchguard_fireware
yamaha
zte_zxros
zyxel_os
Supported Telnet device_type values
adtran_os_telnet
apresia_aeos_telnet
arista_eos_telnet
aruba_procurve_telnet
audiocode_72_telnet
audiocode_66_telnet
audiocode_shell_telnet
brocade_fastiron_telnet
brocade_netiron_telnet
calix_b6_telnet
centec_os_telnet
ciena_saos_telnet
cisco_ios_telnet
cisco_xr_telnet
cisco_s200_telnet
cisco_s300_telnet
dell_dnos6_telnet
dell_powerconnect_telnet
dlink_ds_telnet
extreme_telnet
extreme_exos_telnet
extreme_netiron_telnet
generic_telnet
generic_termserver_telnet
hp_procurve_telnet
hp_comware_telnet
huawei_telnet
huawei_olt_telnet
ipinfusion_ocnos_telnet
juniper_junos_telnet
nokia_sros_telnet
oneaccess_oneos_telnet
paloalto_panos_telnet
rad_etx_telnet
raisecom_telnet
ruckus_fastiron_telnet
ruijie_os_telnet
supermicro_smis_telnet
teldat_cit_telnet
tplink_jetstream_telnet
yamaha_telnet
zte_zxros_telnet
Supported Secure Copy device_type values
arista_eos
ciena_saos
cisco_asa
cisco_ios
cisco_nxos
cisco_xe
cisco_xr
dell_os10
extreme_exos
juniper_junos
linux
nokia_sros
ubiquiti_edgerouter


