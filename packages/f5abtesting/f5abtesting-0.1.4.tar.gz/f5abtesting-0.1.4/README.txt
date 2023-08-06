A python package for region based abtesting.

Installation Guide
1. Install Python (if not has python installed)
    Download python 2.7: https://www.python.org/downloads/release/python-2712/
    Install Python 2.7
2. Install pip
    To install pip, follow the link https://pip.pypa.io/en/latest/installing/
    Download get-pip.py, https://bootstrap.pypa.io/get-pip.py
    python get-pip.py
3. Install f5-sdk
    pip install f5-sdk
4. Install f5abtesting
    pip install f5abtesting
5. Patch f5-sdk
    Copy f5sdk_pool_patch.py to pool.py in f5-sdk package

------------------------------------------------------------------

2 configure files need for the initialization.

ip2region.conf, input IP address to region mapping, here is an example:
region1 10.0.0.0/24
region1 10.10.2.0/24
region2 10.20.2.0/24
region2 10.30.0.0/24
region3 10.40.2.0/24
region3 10.50.2.0/24

irules_tmp.conf, an irules for F5 BIG-IP to distribute traffic to B pool:
# Replace ab_demo with the actual name of the virtual server

when CLIENT_ACCEPTED {
	set debug 1
	set vs_name_dg_ip2region ab_demo_dg_ip2region
	set vs_name_dg_region2b ab_demo_dg_region2b
	set vs_name_pool_b ab_demo_pool_b

	set region_name [class lookup [IP::client_addr] $vs_name_dg_ip2region ]
	if {$debug} {
		log local0. "Client [IP::client_addr] accepted from $region_name, will be assigned to $vs_name_pool_b"
	}
	if { [class match $region_name equals $vs_name_dg_region2b]} {
		pool $vs_name_pool_b
		if {$debug} {
			log local0. "region $region_name is assigned to $vs_name_pool_b"
		}
	}
}