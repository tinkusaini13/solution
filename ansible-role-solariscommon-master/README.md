solariscommon
=============

Common configuration for Solaris services (timezone, dns, nsswitch, etc).

Requirements
------------

None.

Role Variables
--------------

Available variables are listed below.

    solariscommon_be: false
    solariscommon_bename: "solaris"
    solariscommon_timezone: "America/Caracas"
    solariscommon_dns_servers: "192.168.56.1 192.168.56.101"
    solariscommon_dns_search: '"aldoca.local" "aldoca.local.ve"'
    solariscommon_ns_switch: '"files dns"'
    solariscommon_ntp_servers: [ '0.pool.ntp.org prefer', '1.pool.ntp.org', '2.pool.ntp.org' ]
    solariscommon_banner: |
      ##################################################################
      Authorized users only. All activity may be monitored and reported.
      ##################################################################

**Important**: check vars/main.yml before you set a variable, some astrings in svccfg may cause trouble without the necessary quotes.

To check timezones availables in Solaris --> /usr/share/lib/zoneinfo/

Defaults are listed below.

    solariscommon_maxauthtries: 6
    solariscommon_ignorerhosts: 'yes'
    solariscommon_permitrootlogin: 'no'
    solariscommon_permitemptypasswords: 'no'
    solariscommon_sleeptime: 4
    solariscommon_retries: 3
    solariscommon_lockafterretries: 'YES'
    solariscommon_maxweeks: 13
    solariscommon_minweeks: 1
    solariscommon_warnweeks: 4
    solariscommon_passlength: 14
    solariscommon_namecheck: 'YES'
    solariscommon_history: 10
    solariscommon_mindiff: 3
    solariscommon_minupper: 1
    solariscommon_minlower: 1
    solariscommon_minspecial: 1
    solariscommon_mindigit: 1
    solariscommon_maxrepeats: 0
    solariscommon_whitespace: 'YES'
    solariscommon_dictiondbdir: '/var/passwd'
    solariscommon_dictionlist: '/usr/share/lib/dict/words'
    solariscommon_umask: '027'

Dependencies
------------

None

Example Playbook
----------------

    - hosts: servers
      roles:
         - { role: aldenso.solariscommon, solariscommon_be: true, timezone: "America/New_York",  ns_switch: '"files dns mdns"', when: "ansible_os_family == 'Solaris'", become: true }

License
-------

BSD

Author Information
------------------

aldenso@gmail.com