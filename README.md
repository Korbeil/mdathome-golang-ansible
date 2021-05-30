# mdathome-golang-ansible

## What it does

Ansible roles to install [flare's MD@H client](https://github.com/lflare/mdathome-golang) and related tooling.

Theses roles will install:
- MD@H with a systemd daemon;
- Prometheus to collect all your server metrics;
- Grafana to read all theses metrics with preconfigured dashboards;
- A nginx stream to distribute MD@H and Grafana with SSL.

## How to use

`git clone` this repository (or a fork) into your ansible root with "roles" as folder name, then you will be able to use
the roles with scripts like:
```ansible
---
- hosts: mdh
  become: yes
  roles:
    - at-home
    - grafana
    - proxy
```

## Requirements

You need to install following Ansible galaxy roles:
- cloudalchemy.node_exporter
- cloudalchemy.prometheus
- cloudalchemy.grafana

To make it easier, we provide a [`requirements.yaml`](./requirements.yaml) file that you can use as following:
```shell
ansible-galaxy install -r requirements.yaml
```

## Roles

Across all roles, there is one variable that is managing if the current target is a primary or a simple node. By 
default, we assume that you are running only one node and `mdh_node_type` is set to `primary` but if you run more than
one node, and you want to aggregate all the metrics, please set secondary nodes as `node`.

### AtHome

This role will setup [flare's MD@H client](https://github.com/lflare/mdathome-golang) on your server with everything
needed to run it:
- Configuration file is in `/etc/mdh` folder
- Binary is unpacked in `/usr/local/bin` folder
- Log are dump in `/var/log/mdathome` folder

You can override default behavior by setting Ansible variables, please check [`defaults/main.yaml`](./at-home/defaults/main.yaml).<br/>
But some variables are mandatory:
- `mdh_token` This is your MD@H client token

### Metrics

This role will setup Prometheus & node exporter and add Grafana and some dashboards.

You can override default behavior by setting Ansible variables, please check [`defaults/main.yaml`](metrics/defaults/main.yaml).<br/>
But some variables are mandatory:
- `grafana_password` This is your Grafana dashboard password

### Proxy

This role will provide a nginx stream to listen on port 443 and redirect MD@H traffic to flare's client and other stuff 
to usual nginx server blocks (one for Grafana and another one as default not found page).

You can override default behavior by setting Ansible variables, please check [`defaults/main.yaml`](./proxy/defaults/main.yaml).<br/>
But some variables are mandatory:
- `certbot_admin_email` Your email for Certbot updates
- `proxy_grafana_host` The hostname for your Grafana dashboard
- `proxy_mdh_host` Your MD@H host token, this is the second part from your MD@H client URL, for example if your client 
  URL is `https://tf4oiu67eza23.ou1eoz46aez7a.mangadex.network:443`, this variable should contain `ou1eoz46aez7a`
