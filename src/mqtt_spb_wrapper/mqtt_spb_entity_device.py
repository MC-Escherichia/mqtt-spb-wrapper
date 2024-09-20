from .mqtt_spb_entity import MqttSpbEntity


class MqttSpbEntityDevice(MqttSpbEntity):

    def __init__(self, spb_domain_name, spb_eon_name, spb_eon_device_name,
                 retain_birth=False,
                 debug_info=False
                 ):

        # Initialized the object ( parent class ) with Device_id as None - Configuring it as edge node
        super().__init__(spb_domain_name=spb_domain_name, spb_eon_name=spb_eon_name, spb_eon_device_name=spb_eon_device_name,
                         retain_birth=retain_birth,
                         debug_info=debug_info, debug_id="MQTT_SPB_DEVICE"
                         )
