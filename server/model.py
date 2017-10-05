import re


class Configurer:

    def parse_config(self):
        # parsing
        with open("config", "r") as f:
            configs = {}
            for line in f:
                line = re.sub("\s", "", line)

                if line == "" or line.startswith("#"):
                    continue
                words = line.split("=")
                try:
                    words[1] = int(words[1])
                except ValueError:
                    try:
                        words[1] = bool(words[1])
                    except ValueError:
                        print("[ERROR] Value of property '%s' in config file is neither int nor boolean." %words[0])
                except IndexError:
                    print("[ERROR] Value of property '%s' in config file is missing." %words[0])

                configs[words[0]] = words[1]
            # setting
            self.bus_num = configs.get("busnum", 1)
            self.offset_x = configs.get("offset_x", 0)
            self.offset_y = configs.get("offset_y", 0)
            self.offset = configs.get("offset", 0)
            self.forward_0 = configs.get("forward0", True)
            self.forward_1 = configs.get("forward1", False)

    def __init__(self):
        self.parse_config()
