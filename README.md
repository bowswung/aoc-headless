# Headless AoC

Run Age of Empires II (WK) on a server. The included ansible script is capable of bootstrapping an Ubuntu install to run AoC. It can be used on an AWS ec2 instance, a local VM, a docker container, or even the local computer.

## Prerequisite

The game asset must be supplied by you. gzip an `Age of Empires II` folder with an "offline" WK install. Delete any Voobly files to save space, if there are any.

## Setup

- Clone this repository
- `pip3 install ansible`
- Create clean Ubuntu 18.04 server instance(s)
- Configure [ansible](https://docs.ansible.com/ansible/latest/index.html) as necessary
- `ansible-playbook install.yml -e path='</path/to/remote/install>' -e game='</path/to/aoc.tar.gz>'`

## Play a rec

- Connect to server instance
- `cd </path/to/remote/install>`
- `. venv/bin/activate`
- `python -m haoc -i </path/to/remote/install> <path/to/rec>`

## TODO

- [ ] GraphQL API wrapper
- [ ] MGZ parsing
- [ ] Streaming rec input
- [ ] Game snapshots

## Disclaimer

This is experimental software. Use at your own risk.
