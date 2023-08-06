import unittest
from omegaconf import OmegaConf


class TestCLI(unittest.TestCase):
    def test_type(self):
        # test on yaml str
        yaml_str = """
                a: ${list.a}
                b: shdgd
                list:
                    a: 256
                c: 5"""
        conf = OmegaConf.create(yaml_str)
        cfg = OmegaConf.to_container(conf, resolve=True)
        print(type(cfg["list"]["a"]))
        self.assertEqual(cfg["list"]["a"], 256)

        # test yaml file
        config_pth = "/home/azureuser/AutonomousSystemsResearch/utils_package/torchlightning_utils/test/config.yaml"
        config = OmegaConf.load(config_pth)
        cfg = OmegaConf.to_container(config, resolve=True)
        value = cfg["data"]["dataset_config"]["transform_config"]["kwargs"][
            "input_size"
        ]
        print(type(value))
        self.assertEqual(value, 224)

    def test_eval(self):
        OmegaConf.register_new_resolver("eval", eval)
        cfg = OmegaConf.create(
            """
            foo: 35
            baz: ${eval:'${foo} * 0.1'}
            """
        )
        print(cfg.baz)  # Prints '1'


if __name__ == "__main__":
    unittest.main()
