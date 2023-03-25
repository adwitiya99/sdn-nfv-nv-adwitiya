from sdntool.models import Counter


class NameGenerator:
    @staticmethod
    def get_next_network_name():
        counter = Counter.objects.get_or_create(key="network", defaults={
            "value": 0
        })[0]
        counter.value = counter.value + 1
        counter.save()
        return "NT" + str(counter.value)

    @staticmethod
    def get_next_controller_name():
        counter = Counter.objects.get_or_create(key="controller", defaults={
            "value": 0
        })[0]
        counter.value = counter.value + 1
        counter.save()

        return "CTRL" + str(counter.value)

    @staticmethod
    def get_next_switch_name():
        counter = Counter.objects.get_or_create(key="switch", defaults={
            "value": 0
        })[0]
        counter.value = counter.value + 1
        counter.save()

        return "SW" + str(counter.value)

    @staticmethod
    def get_next_router_name():
        counter = Counter.objects.get_or_create(key="router", defaults={
            "value": 0
        })[0]
        counter.value = counter.value + 1
        counter.save()

        return "RT" + str(counter.value)

    @staticmethod
    def get_next_host_name():
        counter = Counter.objects.get_or_create(key="host", defaults={
            "value": 0
        })[0]
        counter.value = counter.value + 1
        counter.save()

        return "H" + str(counter.value) \



    @staticmethod
    def get_next_vni_name():
        counter = Counter.objects.get_or_create(key="vni", defaults={
            "value": 0
        })[0]
        counter.value = counter.value + 1
        counter.save()

        return "VNI" + str(counter.value)

    @staticmethod
    def get_next_virtualmachine_name():
        counter = Counter.objects.get_or_create(key="virtualmachine", defaults={
            "value": 0
        })[0]
        counter.value = counter.value + 1
        counter.save()

        return "VM" + str(counter.value)

    def get_next_virtualnetwork_name():
        counter = Counter.objects.get_or_create(key="virtualnetwork", defaults={
            "value": 0
        })[0]
        counter.value = counter.value + 1
        counter.save()

        return "VN" + str(counter.value)

    @staticmethod
    def get_next_virtualnetworkfunction_name():
        counter = Counter.objects.get_or_create(key="virtualnetworkfunction", defaults={
            "value": 0
        })[0]
        counter.value = counter.value + 1
        counter.save()

        return "VNF" + str(counter.value)

    @staticmethod
    def get_next_nvi_name():
        counter = Counter.objects.get_or_create(key="nvi", defaults={
            "value": 0
        })[0]
        counter.value = counter.value + 1
        counter.save()

        return "NVI" + str(counter.value)

    @staticmethod
    def get_next_router_nv_name():
        counter = Counter.objects.get_or_create(key="router", defaults={
            "value": 0
        })[0]
        counter.value = counter.value + 1
        counter.save()

        return "RTR" + str(counter.value)


