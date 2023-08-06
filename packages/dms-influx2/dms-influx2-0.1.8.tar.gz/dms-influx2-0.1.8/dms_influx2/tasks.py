from influxdb_client import TasksApi


class Tasks(TasksApi):
    def __init__(self, client):
        self.org = client.org
        self.org_id = client.organizations_api().get_organization(org_name=self.org)
        super().__init__(client)

    def create_or_update_calibration_task(self,
                                          bucket,
                                          measurement,
                                          channel_src,
                                          channel_dest,
                                          const_a=None,
                                          const_b=None,
                                          const_c=None,
                                          const_d=None,
                                          task_id=None):
        if bucket is None:
            raise ValueError('Value for argument `bucket` must not be None')
        if measurement is None:
            raise ValueError('Value for argument `measurement` must not be None')
        if channel_src is None:
            raise ValueError('Value for argument `channel_src` must not be None')
        if channel_dest is None:
            raise ValueError('Value for argument `channel_dest` must not be None')
        if const_a is None:
            const_a = 0
        if const_b is None:
            const_b = 0
        if const_c is None:
            const_c = 1
        if const_d is None:
            const_d = 0

        const_a = float(const_a)
        const_b = float(const_b)
        const_c = float(const_c)
        const_d = float(const_d)

        name = f'calibration_{bucket}_{measurement}_{channel_src}_{channel_dest}'

        flux = f'from(bucket: "{bucket}")\n' \
               f'|> range(start: -task.every)\n' \
               f'|> filter(fn: (r) => r._measurement == "{measurement}")\n' \
               f'|> filter(fn: (r) => r["_field"] == "value")\n' \
               f'|> filter(fn: (r) => r["channel"] == "{channel_src}")\n' \
               f'|> map(fn: (r) => ({{r with _value: math.round(x: ' \
               f'({const_a} * math.pow(x: r._value, y: 3.0) + ' \
               f'{const_b} * math.pow(x: r._value, y: 2.0) + ' \
               f'{const_c} * math.pow(x: r._value, y: 1.0) + ' \
               f'{const_d}) * 1000.0) / 1000.0}})) \n' \
               f'|> map(fn: (r) => ({{r with channel: "{channel_dest}", device_id: "${{r.device}}.{channel_dest}"}}))' \
               f'|> to(bucket: "{bucket}")'
        if task_id is not None:
            task = self.find_task_by_id(task_id=task_id)
        else:
            task = self.create_task_every(name=name, flux=flux, organization=self.org_id, every='1m')

        task.flux = 'import "math"\n' \
                    f'option task = {{name: "{name}", every: 1m}} \n' + flux
        return self.update_task(task)
