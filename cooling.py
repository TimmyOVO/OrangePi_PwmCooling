import subprocess
import sys
import os
import time

n = 0
period = 20000000
duty_cycle = 5000000

fan_speed_array = [(0, 0), (35, 20), (45, 30), (75, 85), (85, 100)]


def get_pwmchip_path():
    return f"/sys/class/pwm/pwmchip{str(n)}"


def is_pwmchip_enabled():
    enable_flag_path = f"{get_pwmchip_path()}/pwm0/enable"
    return bool(open(enable_flag_path, "r").readline(1))


def get_system_core_temperature():
    return 0.001 * float(open("/sys/class/thermal/thermal_zone1/temp", "r").read())


def enable_pwm_layout():
    subprocess.run(f"echo 0 > {get_pwmchip_path()}/export", shell=True)


def set_pwm_enabled(enabled):
    subprocess.run(f"echo {enabled} > {get_pwmchip_path()}/pwm0/enable", shell=True)


def change_duty_cycle(new_percentage):
    print(f"修改风扇风速到{new_percentage}%")
    subprocess.run(f"echo {period} > {get_pwmchip_path()}/pwm0/period", shell=True)
    subprocess.run(
        f"echo {int(period*(0.01*(100.0-new_percentage)))} > {get_pwmchip_path()}/pwm0/duty_cycle",
        shell=True,
    )


def main():
    if not is_pwmchip_enabled():
        enable_pwm_layout()
    while True:
        last_fan_percentage = 0
        current_temp = get_system_core_temperature()

        for temp, fan_percentage in fan_speed_array:
            if current_temp >= temp:
                last_fan_percentage = fan_percentage
        print(f"当前核心温度：{current_temp}° , 调整转速为: {last_fan_percentage}%")
        change_duty_cycle(last_fan_percentage)
        time.sleep(3)
    set_pwm_enabled(1)


if __name__ == "__main__":
    main()
