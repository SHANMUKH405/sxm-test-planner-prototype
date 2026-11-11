from ..models import DriverConfig, Target


def get_targets() -> list[Target]:
    return [
        Target(
            id="local-simulator",
            name="Local Learning Simulator",
            status="available",
            target_type="simulator",
            driver=DriverConfig.DEMO,
            capabilities=["local_simulator", "common_flow_demo"],
            description="Safe local target for the prototype Common Flow demo.",
        ),
        Target(
            id="headunit-placeholder",
            name="Head Unit Target",
            status="unconfigured",
            target_type="placeholder",
            driver=DriverConfig.HEADUNIT,
            capabilities=["headunit"],
            description="Placeholder only. No real-head-unit integration is implemented.",
        ),
        Target(
            id="sxm-emu-placeholder",
            name="SAT Emulator + Proxy",
            status="unconfigured",
            target_type="placeholder",
            driver=DriverConfig.SXM_EMU,
            capabilities=["headunit", "sat_emulator", "proxy"],
            description="Placeholder only. No driver control is implemented.",
        ),
        Target(
            id="proxy-placeholder",
            name="Real SAT + Proxy",
            status="unconfigured",
            target_type="placeholder",
            driver=DriverConfig.PROXY,
            capabilities=["headunit", "real_sat", "proxy"],
            description="Placeholder only. No driver control is implemented.",
        ),
    ]
