# 💻 Server Hardware Specifications

## 🖥️ Primary Server (server-01)

### Hardware Specifications
- **Hostname**: `server-01`
- **Purpose**: `[Primary Workload, e.g., Virtualization Host]`

| Component | Details |
|-----------|---------|
| Manufacturer | `[Manufacturer]` |
| Chassis | `[Rack/Tower/Mini]` |
| CPU | `[Model, e.g., AMD Ryzen 5 5600X]` |
| CPU Cores | `[Number of Cores]` |
| Base Clock | `[Base Frequency]` |
| RAM | `[Total Amount, e.g., 64GB]` |
| RAM Type | `[DDR4/DDR5, Speed]` |

### Storage Configuration
- **Boot Drive**:
  - Type: `[SSD/NVMe]`
  - Capacity: `[Size]`
  - Mount: `/`

- **Data Drives**:
  1. `/storage/media`
     - Type: `[HDD/SSD]`
     - Capacity: `[Size]`
     - RAID Configuration: `[RAID Level/None]`

  2. `/backup`
     - Type: `[HDD/SSD]`
     - Capacity: `[Size]`
     - Backup Strategy: `[Snapshot/Incremental]`

## 🔧 System Configuration

### Operating System
- **Distribution**: `[OS Name, e.g., Proxmox VE]`
- **Version**: `[Version Number]`
- **Install Date**: `[Date]`

### Virtualization
- **Hypervisor**: `[Type, e.g., KVM/Docker/Kubernetes]`
- **Container Runtime**: `[Docker/Containerd]`
- **Orchestration**: `[Kubernetes Distro/None]`

## 📊 Performance Metrics

### CPU Utilization
- **Average Load**: `[Percentage]`
- **Peak Load**: `[Percentage]`

### Memory Usage
- **Total RAM**: `[Total Amount]`
- **Used RAM**: `[Current Usage]`
- **Free RAM**: `[Available Memory]`

### Disk I/O
- **Read Speed**: `[MB/s]`
- **Write Speed**: `[MB/s]`
- **IOPS**: `[Input/Output Operations per Second]`

## 🚀 Planned Upgrades

- [ ] Increase RAM
- [ ] Add more storage
- [ ] Upgrade CPU
- [ ] Improve cooling solution

## 📝 Maintenance Log

> **Last Hardware Check**: `[Date]`
> 
> **Notes**: `[Any recent maintenance or observations]`

*Last Updated*: {{ current_date }}