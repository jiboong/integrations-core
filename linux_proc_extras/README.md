# Linux_proc_extras Integration

## Overview
Get metrics from linux_proc_extras service in real time to:

* Visualize and monitor linux_proc_extras states
* Be notified about linux_proc_extras failovers and events.

## Setup
### Installation

The Linux_proc_extras check is packaged with the Agent, so simply [install the Agent](https://app.datadoghq.com/account/settings#agent) on your servers.

### Configuration

Create a `linux_proc_extras.yaml` file in the Datadog Agent's `conf.d` directory. See the [sample linux_proc_extras.yaml](https://github.com/DataDog/integrations-core/blob/master/linux_proc_extras/conf.yaml.example) for all available configuration options.

### Validation

[Run the Agent's `status` subcommand](https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information) and look for `linux_proc_extras` under the Checks section.

## Data Collected
### Metrics
The Linux proc extras check does not include any metric at this time.

### Events
The Linux proc extras check does not include any event at this time.

### Service Checks
The Linux proc extras check does not include any service check at this time.

## Troubleshooting

Need help? Contact [Datadog Support](http://docs.datadoghq.com/help/).

## Further Reading
Learn more about infrastructure monitoring and all our integrations on [our blog](https://www.datadoghq.com/blog/)
