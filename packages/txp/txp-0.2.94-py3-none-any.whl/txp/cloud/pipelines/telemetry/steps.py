import apache_beam as beam
import logging
import txp

class TimeProcessing(beam.DoFn):

    def to_runner_api_parameter(self, unused_context):
        return "beam:transforms:custom_parsing:custom_v0", None

    def process(self, element, timestamp=beam.DoFn.TimestampParam, window=beam.DoFn.WindowParam):
        import google.cloud.firestore as firestore
        from txp.common.utils import firestore_utils
        from txp.common import edge

        firestore_db = firestore.Client()
        mode = firestore_utils.get_signal_mode_from_firestore(element["configuration_id"],
                                                              element["tenant_id"],
                                                              element["edge_logical_id"],
                                                              element["perception_name"], firestore_db)
        if mode is None or not edge.perception_dimensions.SignalMode.is_time(mode):
            return

        yield element


class FftProcessing(beam.DoFn):

    def to_runner_api_parameter(self, unused_context):
        return "beam:transforms:custom_parsing:custom_v0", None

    def process(self, element, timestamp=beam.DoFn.TimestampParam, window=beam.DoFn.WindowParam):
        from scipy.fft import fft
        import google.cloud.firestore as firestore
        from txp.common.utils import firestore_utils
        from txp.common import edge

        firestore_db = firestore.Client()
        mode = firestore_utils.get_signal_mode_from_firestore(element["configuration_id"], element["tenant_id"],
                                                              element["edge_logical_id"], element["perception_name"],
                                                              firestore_db)
        if mode is None or not edge.perception_dimensions.SignalMode.is_fft(mode):
            return
        data = [list(dimension["values"]) for dimension in element["data"]]
        fft_data = []
        for index, dimension_signal_sample in enumerate(data):
            fft_data.append({
                "values": [],
                "index": index
            })
            n = len(fft_data)
            for z in fft(dimension_signal_sample):
                fft_data[n - 1]["values"].append({"real": float(z.real), "imag": float(z.imag)})

        yield {
            "fft": fft_data,
            "package_timestamp": element["package_timestamp"],
            "perception_name": element["perception_name"],
            "edge_logical_id": element["edge_logical_id"],
            "signal_timestamp": element["signal_timestamp"],
            "configuration_id": element["configuration_id"],
            "observation_timestamp": element["observation_timestamp"],
            "gateway_task_id": element["gateway_task_id"],
            "sampling_window_index": element["sampling_window_index"],
            "number_of_sampling_windows": element["number_of_sampling_windows"],
            "tenant_id": element["tenant_id"],
            "partition_timestamp": element["partition_timestamp"]
        }


class PsdProcessing(beam.DoFn):

    def to_runner_api_parameter(self, unused_context):
        return "beam:transforms:custom_parsing:custom_v0", None

    def process(self, element, timestamp=beam.DoFn.TimestampParam, window=beam.DoFn.WindowParam):
        import google.cloud.firestore as firestore
        from txp.common.utils import metrics
        from txp.common.utils import firestore_utils
        from txp.common import edge

        firestore_db = firestore.Client()
        mode = firestore_utils.get_signal_mode_from_firestore(element["configuration_id"],
                                                              element["tenant_id"],
                                                              element["edge_logical_id"],
                                                              element["perception_name"], firestore_db)
        if mode is None or not edge.perception_dimensions.SignalMode.is_psd(mode):
            return
        data = [list(dimension["values"]) for dimension in element["data"]]
        data_psd = []
        for index, dimension_signal_sample in enumerate(data):
            f, psd = metrics.get_psd(dimension_signal_sample,
                                     txp.common.utils.firestore_utils.get_sampling_frequency(element, firestore_db))
            data_psd.append({
                "psd": [float(e) for e in psd],
                "frequency": [float(e) for e in f],
                "index": index,
            })

        yield {
            "data": data_psd,
            "package_timestamp": element["package_timestamp"],
            "perception_name": element["perception_name"],
            "edge_logical_id": element["edge_logical_id"],
            "signal_timestamp": element["signal_timestamp"],
            "configuration_id": element["configuration_id"],
            "observation_timestamp": element["observation_timestamp"],
            "gateway_task_id": element["gateway_task_id"],
            "sampling_window_index": element["sampling_window_index"],
            "number_of_sampling_windows": element["number_of_sampling_windows"],
            "tenant_id": element["tenant_id"],
            "partition_timestamp": element["partition_timestamp"]
        }


class TimeMetrics(beam.DoFn):

    def to_runner_api_parameter(self, unused_context):
        return "beam:transforms:custom_parsing:custom_v0", None

    def process(self, element, timestamp=beam.DoFn.TimestampParam, window=beam.DoFn.WindowParam):
        from txp.common.utils import metrics
        import google.cloud.firestore as firestore
        from txp.common.utils import firestore_utils
        from txp.common import edge

        firestore_db = firestore.Client()
        mode = firestore_utils.get_signal_mode_from_firestore(element["configuration_id"],
                                                              element["tenant_id"],
                                                              element["edge_logical_id"],
                                                              element["perception_name"], firestore_db)
        if mode is None or edge.perception_dimensions.SignalMode.is_image(mode):
            return

        for dimension in range(0, len(element["data"])):
            yield {
                "observation_timestamp": element["observation_timestamp"],
                "edge_logical_id": element["edge_logical_id"],
                "perception_name": element["perception_name"],
                "signal_timestamp": element["signal_timestamp"],
                "package_timestamp": element["package_timestamp"],
                "dimension": dimension,
                "configuration_id": element["configuration_id"],
                "peak": float(metrics.peak(element["data"][dimension]["values"])),
                "rms": float(metrics.rms(element["data"][dimension]["values"])),
                "standard_deviation": float(metrics.standard_deviation(element["data"][dimension]["values"])),
                "crest_factor": float(metrics.crest_factor(element["data"][dimension]["values"])),
                "gateway_task_id": element["gateway_task_id"],
                "sampling_window_index": element["sampling_window_index"],
                "number_of_sampling_windows": element["number_of_sampling_windows"],
                "tenant_id": element["tenant_id"],
                "partition_timestamp": element["partition_timestamp"]
            }


class FftMetrics(beam.DoFn):

    def to_runner_api_parameter(self, unused_context):
        return "beam:transforms:custom_parsing:custom_v0", None

    def process(self, element, timestamp=beam.DoFn.TimestampParam, window=beam.DoFn.WindowParam):
        from txp.common.utils import metrics
        from txp.common.utils import signals_utils

        data_per_dimension = signals_utils.get_fft_as_np_array(element["fft"])
        for dimension in range(0, len(data_per_dimension)):
            data = data_per_dimension[dimension].real
            yield {
                "edge_logical_id": element["edge_logical_id"],
                "perception_name": element["perception_name"],
                "signal_timestamp": element["signal_timestamp"],
                "package_timestamp": element["package_timestamp"],
                "dimension": dimension,
                "configuration_id": element["configuration_id"],
                "peak": float(metrics.peak(data)),
                "rms": float(metrics.rms(data)),
                "standard_deviation": float(metrics.standard_deviation(data)),
                "crest_factor": float(metrics.crest_factor(data)),
                "observation_timestamp": element["observation_timestamp"],
                "gateway_task_id": element["gateway_task_id"],
                "sampling_window_index": element["sampling_window_index"],
                "number_of_sampling_windows": element["number_of_sampling_windows"],
                "tenant_id": element["tenant_id"],
                "partition_timestamp": element["partition_timestamp"]
            }


class PsdMetrics(beam.DoFn):

    def to_runner_api_parameter(self, unused_context):
        return "beam:transforms:custom_parsing:custom_v0", None

    def process(self, element, timestamp=beam.DoFn.TimestampParam, window=beam.DoFn.WindowParam):
        from txp.common.utils import metrics
        import numpy as np

        for dimension in range(0, len(element["data"])):
            f = element["data"][dimension]["frequency"]
            psd = element["data"][dimension]["psd"]
            integrated_psd = metrics.integrate(psd, x=f)
            yield {
                "observation_timestamp": element["observation_timestamp"],
                "edge_logical_id": element["edge_logical_id"],
                "perception_name": element["perception_name"],
                "signal_timestamp": element["signal_timestamp"],
                "package_timestamp": element["package_timestamp"],
                "dimension": dimension,
                "configuration_id": element["configuration_id"],
                "rms": float(np.sqrt(integrated_psd[-1])),
                "standard_deviation": float(metrics.standard_deviation(psd)),
                "crest_factor": float(metrics.crest_factor(psd)),
                "peak_frequency": float(metrics.peak(f)),
                "peak_amplitude": float(metrics.peak(psd)),
                "gateway_task_id": element["gateway_task_id"],
                "sampling_window_index": element["sampling_window_index"],
                "number_of_sampling_windows": element["number_of_sampling_windows"],
                "tenant_id": element["tenant_id"],
                "partition_timestamp": element["partition_timestamp"]
            }


class WriteToBigQuery(beam.DoFn):

    def to_runner_api_parameter(self, unused_context):
        return "beam:transforms:custom_parsing:custom_v0", None

    def process(self, element, table_id, timestamp=beam.DoFn.TimestampParam, window=beam.DoFn.WindowParam):
        from google.cloud import bigquery
        from datetime import datetime
        import json

        keys_to_ignore = ["gateway_task_id", "sampling_window_index", "number_of_sampling_windows"]
        bigquery_element = {k: element[k] for k in element if k not in keys_to_ignore}
        client = bigquery.Client()
        table_id = table_id.replace(":", ".")
        errors = client.insert_rows_json(table_id, [bigquery_element])
        message = f"""Edge: {element["edge_logical_id"]}
        Perception: {element["perception_name"]}
        """
        if not errors:
            logging.info(f"""Storing in {table_id}: {message} """)

            res = {
                "table_id": table_id,
                "edge_logical_id": element["edge_logical_id"],
                "perception_name": element["perception_name"],
                "observation_timestamp": element["observation_timestamp"],
                "configuration_id": element["configuration_id"],
                "tenant_id": element["tenant_id"],
                "partition_timestamp": element["partition_timestamp"]
            }
            if "previous_part_index" in element:
                res["previous_part_index"] = element["previous_part_index"]
            if "part_index" in element:
                res["part_index"] = element["part_index"]
            if "dimension" in element:
                res["dimension"] = element["dimension"]

            res = json.dumps(res).encode('utf-8')

            yield res
        else:
            logging.error(f"""Could not store in {table_id}: {message}, ERROR: {errors} """)


class VibrationProcessing(beam.DoFn):
    """This step is used to generate the RMS smoothed wave given an input signal.

    It's the first step required to generate the vibration data analysis.
    """
    def to_runner_api_parameter(self, unused_context):
        return "beam:transforms:custom_parsing:custom_v0", None

    def process(self, elements, timestamp=beam.DoFn.TimestampParam, window=beam.DoFn.WindowParam):
        import txp.common.utils.metrics as metrics
        from scipy.fft import fft
        import google.cloud.firestore as firestore
        from txp.common.utils import firestore_utils
        from txp.common import edge
        from iCOMOXSDK.sensors import BMM150
        import numpy as np

        element = elements[0]

        # Only process Vibration data from Icomox box
        if element['device_type'] not in {
            "Icomox"
        }:
            return

        # Todo: here we should pull from DB the window size for the given motor/sensor.
        # firestore_db = firestore.Client()
        # mode = firestore_utils.get_signal_mode_from_firestore(element["configuration_id"], element["tenant_id"],
        #                                                       element["edge_logical_id"], element["perception_name"],
        #                                                       firestore_db)

        vibration_speed_data = None
        vibration_acceleration_data = None
        magnetometer_data = None

        for e in elements:
            logging.info(f"Iterating over {e['perception_name']}")
            if e['perception_name'] == edge.VibrationSpeedSignal.perception_name():
                vibration_speed_data = e['data']
                logging.info(f"Vibration processing found signal for VibrationSpeedSignal")

            elif e['perception_name'] == edge.VibrationAccelerationSignal.perception_name():
                vibration_acceleration_data = e['data']
                logging.info(f"Vibration processing found signal for VibrationAcceleration")

            elif e['perception_name'] == edge.MagnetometerSignal.perception_name():
                magnetometer_data = e['data']
                logging.info(f"Vibration processing found signal for Magnetometer")

        data = vibration_speed_data
        data = [list(dimension["values"]) for dimension in data]
        magnetometer_data = [list(dimension["values"]) for dimension in magnetometer_data]

        # COMPUTE RMS SMOOTH
        rms_data_axis = []
        for index, single_axis_sample in enumerate(data):
            rms_data_axis.append({
                "values": [],
                "index": index
            })
            n = len(rms_data_axis)
            rms_data_axis[n - 1]["values"] = metrics.rolling_rms(np.asarray(single_axis_sample)).tolist()

        # COMPUTE FFT
        fft_data = []
        for index, dimension_signal_sample in enumerate(data):
            fft_data.append({
                "values": [],
                "index": index
            })
            n = len(fft_data)
            for z in fft(dimension_signal_sample):
                fft_data[n - 1]["values"].append({"real": float(z.real), "imag": float(z.imag)})

        # Compute RPM for X-axis

        BMM150_quantile_for_noise_floor_estimator = 0.25
        BMM150_minimum_SNR_for_speed_detection_dB = 20
        BMM150_ = BMM150.class_BMM150(
            quantile_for_noise_floor_estimator=BMM150_quantile_for_noise_floor_estimator,
            minimum_SNR_for_speed_detection_dB=BMM150_minimum_SNR_for_speed_detection_dB)

        ASYNC_MOTOR_number_of_poles_pairs = 2
        ASYNC_MOTOR_slip_factor_percentages = 0.0
        network_frequency_Hz = BMM150_.maximum_of_PSD(magnetometer_data[0])
        synchronous_frequency_Hz = network_frequency_Hz / ASYNC_MOTOR_number_of_poles_pairs
        rotor_frequency_Hz = synchronous_frequency_Hz * (1 - ASYNC_MOTOR_slip_factor_percentages / 100)
        rpm = rotor_frequency_Hz * 60

        logging.info(f"{type(data)}")
        logging.info(f"{type(rms_data_axis)}")
        logging.info(f"{type(fft_data)}")
        logging.info(f"{type(rpm)}")

        data_formatted = []
        for i, dimension_signal_sample in enumerate(data):
            data_formatted.append({
                "values": list(dimension_signal_sample),
                "index": i
            })
            i += 1

        yield {
            "signal": data_formatted,
            "rms_smoothed_signal": rms_data_axis,
            "fft": fft_data,
            "rpm": rpm,
            "perception_name": element["perception_name"],
            "edge_logical_id": element["edge_logical_id"],
            "configuration_id": element["configuration_id"],
            "observation_timestamp": element["observation_timestamp"],
            "tenant_id": element["tenant_id"],
            "partition_timestamp": element["partition_timestamp"]
        }
