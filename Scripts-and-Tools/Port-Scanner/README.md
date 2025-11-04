# Advanced Port Scanner

A Python-based TCP port scanner that detects whether a port is **OPEN**, **CLOSED**, or **FILTERED** (firewalled).  
Includes banner grabbing for identifying running services.

## Features
- Detects:
  - **OPEN** ports → Service is listening
  - **CLOSED** ports → No service, but reachable
  - **FILTERED** ports → Blocked by firewall / no response
- Banner grabbing for some services
- Multithreaded for faster scanning

## Usage
1. Clone this repository:
   ```bash
   git clone https://github.com/Thato-Taj/cybersecurity-portfolio.git

