class Rule:
    id = "506"
    description = "Verify Network elements are enabled in fabric overlay services"
    severity = "HIGH"

    @classmethod
    def match(cls, data_model):
        results = []
       
        networks = []

        network_keys = ['vxlan', 'overlay', 'networks']
        check = cls.data_model_key_check(data_model, network_keys)
        if 'networks' in check['keys_data']:
            networks = data_model["vxlan"]["overlay"]["networks"]
        else:
            network_keys = ['vxlan', 'overlay_services', 'networks']
            check = cls.data_model_key_check(data_model, network_keys)
            if 'networks' in check['keys_data']:
                networks = data_model["vxlan"]["overlay_services"]["networks"]

        # if data_model.get("vxlan", None):
        #     if data_model["vxlan"].get("overlay", None) or data_model["vxlan"].get("overlay_services", None):
        #         if data_model["vxlan"].get("overlay").get("networks", None):
        #             networks = data_model["vxlan"]["overlay"]["networks"]
        #         elif data_model["vxlan"].get("overlay_services").get("networks", None):
        #             networks = data_model["vxlan"]["overlay_services"]["networks"]

        for network in networks:
            results.append("Found network: " + network.get("name", "unnamed"))

        return results

    @classmethod
    def data_model_key_check(cls, tested_object, keys):
        dm_key_dict = {'keys_found': [], 'keys_not_found': [], 'keys_data': [], 'keys_no_data': []}
        for key in keys:
            if tested_object and key in tested_object:
                dm_key_dict['keys_found'].append(key)
                tested_object = tested_object[key]
                if tested_object:
                    dm_key_dict['keys_data'].append(key)
                else:
                    dm_key_dict['keys_no_data'].append(key)
            else:
                dm_key_dict['keys_not_found'].append(key)
        return dm_key_dict

    @classmethod
    def safeget(cls, dict, keys):
        # Utility function to safely get nested dictionary values
        for key in keys:
            if dict is None:
                return None
            if key in dict:
                dict = dict[key]
            else:
                return None

        return dict
