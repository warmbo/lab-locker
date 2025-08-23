# 🏠 My Homelab

## 🖥️ Server Inventory

| Hostname | Role | CPU | RAM | Primary OS | Status |
|----------|------|-----|-----|------------|--------|
| server-01 | `[Primary Function, e.g., Media Server]` | `[CPU Model]` | `[RAM Amount]` | `[OS Name]` | `Active` |
| server-02 | `[Secondary Function]` | `[CPU Model]` | `[RAM Amount]` | `[OS Name]` | `Standby` |
| nas-01 | `[Storage/Backup]` | `[CPU Model]` | `[RAM Amount]` | `[OS Name]` | `Active` |

## 🌐 Network Configuration

```mermaid
graph TD
    A[Internet] --> B{`[Router/Firewall Model]`}
    B --> C[`[Core Switch Model]`]
    C --> D[Management VLAN]
    C --> E[Services VLAN]
    C --> F[IoT VLAN]
```

## 📦 Self-Hosted Services

### Media & Entertainment
- [ ] Plex Media Server
  - **URL**: `[local.plex.example.com]`
  - **Purpose**: `[Personal media streaming]`
- [ ] Sonarr
  - **URL**: `[sonarr.example.com]`
  - **Purpose**: `[TV Show Management]`

### Productivity
- [ ] Nextcloud
  - **URL**: `[cloud.example.com]`
  - **Purpose**: `[Personal Cloud Storage]`
- [ ] Gitea
  - **URL**: `[git.example.com]`
  - **Purpose**: `[Self-Hosted Git Repository]`

### Home Automation
- [ ] Home Assistant
  - **URL**: `[ha.example.com]`
  - **Purpose**: `[Smart Home Control]`

### Monitoring
- [ ] Grafana
  - **URL**: `[monitor.example.com]`
  - **Purpose**: `[System Metrics Dashboard]`
- [ ] Uptime Kuma
  - **URL**: `[status.example.com]`
  - **Purpose**: `[Service Uptime Monitoring]`

## 🔒 Access & Security

| Service | Authentication Method | Access Type |
|---------|----------------------|-------------|
| VPN | `[VPN Type, e.g., WireGuard]` | Remote Access |
| Web Services | `[SSO Method]` | `[Access Control Type]` |
| SSH | `[Authentication Method]` | `[Restricted/Open]` |

## 📊 Infrastructure Details

- **Total Compute Cores**: `[Number of Cores]`
- **Total RAM**: `[Total RAM Amount]`
- **Storage**:
  - Local SSD: `[SSD Storage Amount]`
  - NAS Storage: `[NAS Storage Amount]`
  - Backup Storage: `[Backup Storage Amount]`

## 🚀 Project Roadmap

- [ ] `[Specific Infrastructure Improvement]`
- [ ] `[Service Migration Plan]`
- [ ] `[Security Enhancement]`

## 🔧 Recent Changes

> **Last Major Update**: `[Date of Last Significant Change]`
> 
> **Notes**: `[Brief description of recent modifications]`

## 📝 Contact & Support

- **Primary Administrator**: `[Your Name]`
- **Contact Email**: `[Your Email]`
- **Emergency Contact**: `[Optional Emergency Contact]`

*Last Updated*: {{ current_date }}