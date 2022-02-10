#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2015, Adam Števko <adam.stevko@gmail.com>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible. If not, see <http://www.gnu.org/licenses/>.
#

DOCUMENTATION = '''
---
module: dladm_vlan
short_description: Manage VLAN interfaces on Solaris/illumos systems.
description:
    - Create or delete VLAN interfaces on Solaris/illumos systems.
version_added: "2.3"
author: Adam Števko (@xen0l)
options:
    name:
        description:
            - VLAN interface name.
        required: true
    link:
        description:
            - VLAN underlying link name.
        required: true
    temporary:
        description:
            - Specifies that the VLAN interface is temporary. Temporary VLANs
              do not persist across reboots.
        required: false
        default: false
    vlan_id:
        description:
            - VLAN ID value for VLAN interface.
        required: false
        default: false
        aliases: [ "vid" ]
    state:
        description:
            - Create or delete Solaris/illumos VNIC.
        required: false
        default: "present"
        choices: [ "present", "absent" ]
'''

EXAMPLES = '''
# Create 'vlan42' VLAN over 'bnx0' link
dladm_vlan: name=vlan42 link=bnx0 vlan_id=42 state=present

# Remove 'vlan1337' VLAN interface
dladm_vlan: name=vlan1337 state=absent
'''


class VLAN(object):

    def __init__(self, module):
        self.module = module

        self.name = module.params['name']
        self.link = module.params['link']
        self.vlan_id = module.params['vlan_id']
        self.temporary = module.params['temporary']
        self.state = module.params['state']

    def vlan_exists(self):
        cmd = [self.module.get_bin_path('dladm', True)]

        cmd.append('show-vlan')
        cmd.append(self.name)

        (rc, _, _) = self.module.run_command(cmd)

        if rc == 0:
            return True
        else:
            return False

    def create_vlan(self):
        cmd = [self.module.get_bin_path('dladm', True)]

        cmd.append('create-vlan')

        if self.temporary:
            cmd.append('-t')

        cmd.append('-l')
        cmd.append(self.link)
        cmd.append('-v')
        cmd.append(self.vlan_id)
        cmd.append(self.name)

        return self.module.run_command(cmd)

    def delete_vlan(self):
        cmd = [self.module.get_bin_path('dladm', True)]

        cmd.append('delete-vlan')

        if self.temporary:
            cmd.append('-t')
        cmd.append(self.name)

        return self.module.run_command(cmd)

    def is_valid_vlan_id(self):

        return 0 <= int(self.vlan_id) <= 4095


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(required=True, type='str'),
            link=dict(default=None, type='str'),
            vlan_id=dict(default=0, aliases=['vid']),
            temporary=dict(default=False, type='bool'),
            state=dict(default='present', choices=['absent', 'present']),
        ),
        required_if=[
            ['state', 'present', ['vlan_id', 'link', 'name']],
        ],
        supports_check_mode=True
    )

    vlan = VLAN(module)

    rc = None
    out = ''
    err = ''
    result = {}
    result['name'] = vlan.name
    result['link'] = vlan.link
    result['state'] = vlan.state
    result['temporary'] = vlan.temporary

    if int(vlan.vlan_id) != 0:
        if not vlan.is_valid_vlan_id():
            module.fail_json(msg='Invalid VLAN id value',
                             name=vlan.name,
                             state=vlan.state,
                             link=vlan.link,
                             vlan_id=vlan.vlan_id)
        result['vlan_id'] = vlan.vlan_id

    if vlan.state == 'absent':
        if vlan.vlan_exists():
            if module.check_mode:
                module.exit_json(changed=True)
            (rc, out, err) = vlan.delete_vlan()
            if rc != 0:
                module.fail_json(name=vlan.name, msg=err, rc=rc)
    elif vlan.state == 'present':
        if not vlan.vlan_exists():
            if module.check_mode:
                module.exit_json(changed=True)
            (rc, out, err) = vlan.create_vlan()

        if rc is not None and rc != 0:
            module.fail_json(name=vlan.name, msg=err, rc=rc)

    if rc is None:
        result['changed'] = False
    else:
        result['changed'] = True

    if out:
        result['stdout'] = out
    if err:
        result['stderr'] = err

    module.exit_json(**result)

from ansible.module_utils.basic import *
main()
