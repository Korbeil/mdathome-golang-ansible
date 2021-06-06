def filter_hosts(hostvars, property, value):
    return [v for v in hostvars if hostvars[v][property] == value]


class FilterModule(object):

    def filters(self):
        return {
            'filter_hosts': filter_hosts
        }
