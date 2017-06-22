import time, numpy, sys
import wrapper


if __name__ == '__main__':
    wrapper.initialize()
    wrapper.set_sweep_range(200.0, 300.0)
    wrapper.set_sweep_time(10.0)
    wrapper.set_chopper_sweep_on(False)
    wrapper.set_chopper_frequency(10.0)
    wrapper.start_scan()
    wrapper.trigger_sweep()
    start_time = time.time()
    time.sleep(10)
    wrapper.stop_scan()
    stop_time = time.time()
    wrapper.get_data()
