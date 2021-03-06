# NTP check
{{< img src="integrations/ntp/ntpgraph.png" alt="NTP Graph" responsive="true" popup="true">}}
## Overview

The Network Time Protocol (NTP) integration is enabled by default and reports the time offset from an ntp server every 15 minutes. When the local agent's time is more than 15 seconds off from the Datadog service and the other hosts that you are monitoring, you may experience:

* Incorrect alert triggers
* Metric delays
* Gaps in graphs of metrics

Default NTP servers reached:

* `1.datadog.pool.ntp.org`
* `2.datadog.pool.ntp.org`
* `3.datadog.pool.ntp.org`

## Setup
### Installation

The NTP check is packaged with the Agent, so simply [install the Agent](https://app.datadoghq.com/account/settings#agent) on your servers.

### Configuration

The Agent enables the NTP check by default, but if you want to configure the check yourself, create a file `ntp.yaml` in the Agent's `conf.d` directory. See the [sample ntp.yaml](https://github.com/DataDog/integrations-core/blob/master/ntp/conf.yaml.default) for all available configuration options:

```
init_config:

instances:
  - offset_threshold: 60 # seconds difference between local clock and NTP server when ntp.in_sync service check becomes CRITICAL; default is 60
#   host: pool.ntp.org # set to use an NTP server of your choosing
#   port: 1234         # set along with host
#   version: 3         # to use a specific NTP version
#   timeout: 5         # seconds to wait for a response from the NTP server; default is 1
```

Configuration Options:

* `host` (Optional) - Host name of alternate ntp server, for example `pool.ntp.org`
* `port` (Optional) - What port to use
* `version` (Optional) - ntp version
* `timeout` (Optional) - Response timeout

[Restart the Agent](https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent) to effect any configuration changes.

### Validation

[Run the Agent's `status` subcommand](https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information) and look for `ntp` under the Checks section.

## Data Collected
### Metrics
See [metadata.csv](https://github.com/DataDog/integrations-core/blob/master/ntp/metadata.csv) for a list of metrics provided by this check.

### Events
The NTP check does not include any event at this time.

### Service Checks

`ntp.in_sync`:

Returns CRITICAL if the NTP offset is greater than the threshold specified in `ntp.yaml`, otherwise OK.

## Troubleshooting
Need help? Contact [Datadog Support](http://docs.datadoghq.com/help/).

## Further Reading
Learn more about infrastructure monitoring and all our integrations on [our blog](https://www.datadoghq.com/blog/)
