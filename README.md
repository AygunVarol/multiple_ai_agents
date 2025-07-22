# Multi-Agent LLM Framework for Smart Environments

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Paper](https://img.shields.io/badge/paper-IEEE%20Network-green.svg)](link-to-paper)

## Overview

This repository contains the implementation of a hierarchical multi-agent framework that enables edge-enabled collaboration between large-scale cloud-based models and small-scale edge-deployed models in smart indoor environments. The system demonstrates dynamic task allocation across Raspberry Pi devices, edge servers, and cloud infrastructure for environmental monitoring and control.

## Architecture

The framework consists of:
- **Location-Specific LLM Agents**: Deployed on Raspberry Pi devices with BME680 sensors
- **Supervisory Agent**: Orchestrates distributed agents using dynamic task allocation
- **Edge-Cloud Collaboration**: Optimizes computational efficiency and responsiveness

## Features

- 🏠 **Smart Environment Monitoring**: Real-time temperature, humidity, pressure, and air quality tracking
- 🤖 **Multi-Agent Coordination**: Hierarchical agent system with autonomous task allocation
- ⚡ **Edge-Cloud Optimization**: Dynamic resource allocation based on computational requirements
- 🔄 **Fault Tolerance**: Autonomous failover mechanisms and leader election
- 🎯 **Location-Aware Specialization**: Environment-specific model fine-tuning
- 📡 **REST API Communication**: Seamless interaction between heterogeneous computing resources

## Repository Structure

```
├── agents/
│   ├── supervisor/
│   │   ├── supervisor_agent.py
│   │   ├── task_allocator.py
│   │   └── resource_monitor.py
│   ├── location_agents/
│   │   ├── base_agent.py
│   │   ├── office_agent.py
│   │   ├── kitchen_agent.py
│   │   └── hallway_agent.py
│   └── models/
│       ├── llama_wrapper.py
│       └── model_utils.py
├── sensors/
│   ├── bme680_reader.py
│   ├── sensor_calibration.py
│   └── data_processor.py
├── communication/
│   ├── api_server.py
│   ├── message_handler.py
│   └── protocol.py
├── deployment/
│   ├── raspberry_pi/
│   │   ├── install.sh
│   │   ├── systemd/
│   │   └── config/
│   ├── edge_server/
│   │   ├── docker/
│   │   └── kubernetes/
│   └── cloud/
│       └── aws/
├── experiments/
│   ├── scenarios/
│   │   ├── normal_operation.py
│   │   ├── supervisor_failure.py
│   │   └── load_shedding.py
│   ├── evaluation/
│   │   ├── performance_metrics.py
│   │   └── analysis_tools.py
│   └── data/
│       ├── tampere_deployment/
│       └── synthetic/
├── config/
│   ├── agent_config.yaml
│   ├── sensor_config.yaml
│   └── deployment_config.yaml
├── docs/
│   ├── installation.md
│   ├── deployment_guide.md
│   ├── api_documentation.md
│   └── troubleshooting.md
├── tests/
│   ├── unit/
│   ├── integration/
│   └── system/
├── requirements.txt
├── setup.py
├── LICENSE
└── README.md
```

## Quick Start

### Prerequisites
- Python 3.8+
- Raspberry Pi 4/5 with Raspbian OS
- Bosch BME680 sensors
- Edge server (laptop/desktop) with GPU (optional)
- Internet connection for cloud integration

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/multi-agent-llm-smart-env.git
cd multi-agent-llm-smart-env
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure the system:
```bash
cp config/agent_config.yaml.example config/agent_config.yaml
# Edit configuration files according to your setup
```

### Deployment

#### Raspberry Pi Agents
```bash
# On each Raspberry Pi
./deployment/raspberry_pi/install.sh
sudo systemctl enable smart-agent
sudo systemctl start smart-agent
```

#### Supervisor Agent
```bash
# On edge server
python agents/supervisor/supervisor_agent.py --config config/agent_config.yaml
```

## Experimental Scenarios

### Scenario 1: Normal Operation
```bash
python experiments/scenarios/normal_operation.py
```

### Scenario 2: Supervisor Failure
```bash
python experiments/scenarios/supervisor_failure.py
```

### Scenario 3: Load Shedding
```bash
python experiments/scenarios/load_shedding.py
```

## Configuration

### Agent Configuration
```yaml
supervisor:
  host: "192.168.1.100"
  port: 8080
  model: "llama-3.2-1b"
  resource_threshold: 0.7

agents:
  office:
    location: "office"
    sensor_port: "/dev/ttyUSB0"
    model: "llama-3.2-1b"
  kitchen:
    location: "kitchen"
    sensor_port: "/dev/ttyUSB1"
    model: "llama-3.2-1b"
  hallway:
    location: "hallway"
    sensor_port: "/dev/ttyUSB2"
    model: "llama-3.2-1b"
```

## API Documentation

### Supervisor Agent Endpoints
- `GET /agents` - List all registered agents
- `POST /task` - Submit task for execution
- `GET /status` - System status and metrics
- `POST /allocate` - Manual task allocation

### Location Agent Endpoints
- `GET /sensor_data` - Current sensor readings
- `POST /execute` - Execute assigned task
- `GET /health` - Agent health status

## Performance Metrics

The framework tracks:
- **Latency**: Response times for different task types
- **Throughput**: Tasks processed per second
- **Resource Utilization**: CPU/Memory/GPU usage across devices
- **Accuracy**: Task completion success rates
- **Energy Consumption**: Power usage on Raspberry Pi devices

## Research Paper

This implementation accompanies our IEEE Network paper:
> "Multiple AI/LLM Agent Deployments in Smart Environments: Edge-Enabled Collaboration Between Large-Scale and Small-Scale Models"

### Citation
```bibtex
@article{varol2025multi,
  title={Multiple AI/LLM Agent Deployments in Smart Environments: Edge-Enabled Collaboration Between Large-Scale and Small-Scale Models},
  author={Varol, Ayg{\"u}n and Motlagh, Naser Hossein and Leino, Mirka and Virkki, Johanna},
  journal={IEEE Network},
  year={2025},
  publisher={IEEE}
}
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Tampere University for providing experimental facilities
- IEEE Network for publication opportunity
- Open source community for tools and libraries

## Contact

- Aygün Varol - [aygun.varol@tuni.fi](mailto:aygun.varol@tuni.fi)
- Project Link: [[https://github.com/yourusername/multi-agent-llm-smart-env](https://github.com/AygunVarol/multiple_ai_agents)]([https://github.com/AygunVarol/multi-agent-llm-smart-env](https://github.com/AygunVarol/multiple_ai_agents))

## Troubleshooting

See [docs/troubleshooting.md](docs/troubleshooting.md) for common issues and solutions.

## Roadmap

- [ ] Support for additional sensor types
- [ ] Mobile app interface
- [ ] Enhanced security features
- [ ] Kubernetes deployment automation
- [ ] Real-time dashboard
