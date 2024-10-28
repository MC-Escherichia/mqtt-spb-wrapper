#/********************************************************************************
# * Copyright (c) 2014, 2018 Cirrus Link Solutions and others
# *
# * This program and the accompanying materials are made available under the
# * terms of the Eclipse Public License 2.0 which is available at
# * http://www.eclipse.org/legal/epl-2.0.
# *
# * SPDX-License-Identifier: EPL-2.0
# *
# * Contributors:
# *   Cirrus Link Solutions - initial implementation
# ********************************************************************************/

from mqtt_spb_wrapper.spb_core import sparkplug_b_pb2
import time
from .sparkplug_b_pb2 import Payload
from mqtt_spb_wrapper.spb_core.array_packer import *

seqNum = 0
bdSeq = 0

class DataSetDataType:
    Unknown = 0
    Int8 = 1
    Int16 = 2
    Int32 = 3
    Int64 = 4
    UInt8 = 5
    UInt16 = 6
    UInt32 = 7
    UInt64 = 8
    Float = 9
    Double = 10
    Boolean = 11
    String = 12
    DateTime = 13
    Text = 14

class MetricDataType:
    Unknown = 0
    Int8 = 1
    Int16 = 2
    Int32 = 3
    Int64 = 4
    UInt8 = 5
    UInt16 = 6
    UInt32 = 7
    UInt64 = 8
    Float = 9
    Double = 10
    Boolean = 11
    String = 12
    DateTime = 13
    Text = 14
    UUID = 15
    DataSet = 16
    Bytes = 17
    File = 18
    Template = 19

class ParameterDataType:
    Unknown = 0
    Int8 = 1
    Int16 = 2
    Int32 = 3
    Int64 = 4
    UInt8 = 5
    UInt16 = 6
    UInt32 = 7
    UInt64 = 8
    Float = 9
    Double = 10
    Boolean = 11
    String = 12
    DateTime = 13
    Text = 14


######################################################################
# Always request this before requesting the Node Birth Payload
######################################################################
def getNodeDeathPayload(lwtexist = False, isedgenode = False):
    bdseq = getBdSeqNum()
    if lwtexist:
        bdseq -= 1
    if isedgenode:
        bdseq = getBdSeqNum(reset=True)
    payload = sparkplug_b_pb2.Payload()
    payload.seq = getSeqNum()
    addMetric(payload, "bdSeq", None, MetricDataType.Int64, bdseq)
    return payload
######################################################################


######################################################################
# Always request this after requesting the Node Death Payload
######################################################################
def getNodeBirthPayload():
    global seqNum
    seqNum = 0
    payload = sparkplug_b_pb2.Payload()
    payload.timestamp = int(round(time.time() * 1000))
    payload.seq = getSeqNum()
    addMetric(payload, "bdSeq", None, MetricDataType.Int64, bdSeq - 1)
    return payload
######################################################################

######################################################################
# Get the DBIRTH payload
######################################################################
def getDeviceBirthPayload():
    payload = sparkplug_b_pb2.Payload()
    payload.timestamp = int(round(time.time() * 1000))
    payload.seq = getSeqNum()
    return payload
######################################################################


######################################################################
# Get a DDATA payload
######################################################################
def getDdataPayload():
    return getDeviceBirthPayload()
######################################################################


######################################################################
# Helper method for adding dataset metrics to a payload
######################################################################
def initDatasetMetric(payload, name, alias, columns, types):
    metric = payload.metrics.add()
    if name is not None:
        metric.name = name
    if alias is not None:
        metric.alias = alias
    metric.timestamp = int(round(time.time() * 1000))
    metric.datatype = MetricDataType.DataSet

    # Set up the dataset
    metric.dataset_value.num_of_columns = len(types)
    metric.dataset_value.columns.extend(columns)
    metric.dataset_value.types.extend(types)
    return metric.dataset_value
######################################################################


######################################################################
# Helper method for adding dataset metrics to a payload
######################################################################
def initTemplateMetric(payload, name, alias, templateRef):
    metric = payload.metrics.add()
    if name is not None:
        metric.name = name
    if alias is not None:
        metric.alias = alias
    metric.timestamp = int(round(time.time() * 1000))
    metric.datatype = MetricDataType.Template

    # Set up the template
    if templateRef is not None:
        metric.template_value.template_ref = templateRef
        metric.template_value.is_definition = False
    else:
        metric.template_value.is_definition = True

    return metric.template_value
######################################################################


######################################################################
# Helper method for adding metrics to a container which can be a
# payload or a template with a timestamp
######################################################################
#def addMetric(container, name, alias, type, value):
#    metric.timestamp = int(round(time.time() * 1000))
#    return addMetric(container, name, alias, type, value, timestamp)

######################################################################
# Helper method for adding metrics to a container which can be a
# payload or a template
######################################################################
def addMetric(container, name, alias, type, value, timestamp=int(round(time.time() * 1000))):
    metric = container.metrics.add()
    if name is not None:
        metric.name = name
    if alias is not None:
        metric.alias = alias
    metric.timestamp = timestamp

    # print( "Type: " + str(type))

    if type == MetricDataType.Int8:
        metric.datatype = MetricDataType.Int8
        if value < 0:
            value = value + 2**8
        metric.int_value = value
    elif type == MetricDataType.Int16:
        metric.datatype = MetricDataType.Int16
        if value < 0:
            value = value + 2**16
        metric.int_value = value
    elif type == MetricDataType.Int32:
        metric.datatype = MetricDataType.Int32
        if value < 0:
            value = value + 2**32
        metric.int_value = value
    elif type == MetricDataType.Int64:
        metric.datatype = MetricDataType.Int64
        if value < 0:
            value = value + 2**64
        metric.long_value = value
    elif type == MetricDataType.UInt8:
        metric.datatype = MetricDataType.UInt8
        metric.int_value = value
    elif type == MetricDataType.UInt16:
        metric.datatype = MetricDataType.UInt16
        metric.int_value = value
    elif type == MetricDataType.UInt32:
        metric.datatype = MetricDataType.UInt32
        metric.int_value = value
    elif type == MetricDataType.UInt64:
        metric.datatype = MetricDataType.UInt64
        metric.long_value = value
    elif type == MetricDataType.Float:
        metric.datatype = MetricDataType.Float
        metric.float_value = value
    elif type == MetricDataType.Double:
        metric.datatype = MetricDataType.Double
        metric.double_value = value
    elif type == MetricDataType.Boolean:
        metric.datatype = MetricDataType.Boolean
        metric.boolean_value = value
    elif type == MetricDataType.String:
        metric.datatype = MetricDataType.String
        metric.string_value = value
    elif type == MetricDataType.DateTime:
        metric.datatype = MetricDataType.DateTime
        metric.long_value = value
    elif type == MetricDataType.Text:
        metric.datatype = MetricDataType.Text
        metric.string_value = value
    elif type == MetricDataType.UUID:
        metric.datatype = MetricDataType.UUID
        metric.string_value = value
    elif type == MetricDataType.Bytes:
        metric.datatype = MetricDataType.Bytes
        metric.bytes_value = value
    elif type == MetricDataType.File:
        metric.datatype = MetricDataType.File
        metric.bytes_value = value
    elif type == MetricDataType.Template:
        metric.datatype = MetricDataType.Template
        metric.template_value = value
    # elif type == MetricDataType.Int8Array:
    #     metric.datatype = MetricDataType.Int8Array
    #     metric.bytes_value = convert_to_packed_int8_array(value)
    # elif type == MetricDataType.Int16Array:
    #     metric.datatype = MetricDataType.Int16Array
    #     metric.bytes_value = convert_to_packed_int16_array(value)
    # elif type == MetricDataType.Int32Array:
    #     metric.datatype = MetricDataType.Int32Array
    #     metric.bytes_value = convert_to_packed_int32_array(value)
    # elif type == MetricDataType.Int64Array:
    #     metric.datatype = MetricDataType.Int64Array
    #     metric.bytes_value = convert_to_packed_int64_array(value)
    # elif type == MetricDataType.UInt8Array:
    #     metric.datatype = MetricDataType.UInt8Array
    #     metric.bytes_value = convert_to_packed_uint8_array(value)
    # elif type == MetricDataType.UInt16Array:
    #     metric.datatype = MetricDataType.UInt16Array
    #     metric.bytes_value = convert_to_packed_uint16_array(value)
    # elif type == MetricDataType.UInt32Array:
    #     metric.datatype = MetricDataType.UInt32Array
    #     metric.bytes_value = convert_to_packed_uint32_array(value)
    # elif type == MetricDataType.UInt64Array:
    #     metric.datatype = MetricDataType.UInt64Array
    #     metric.bytes_value = convert_to_packed_uint64_array(value)
    # elif type == MetricDataType.FloatArray:
    #     metric.datatype = MetricDataType.FloatArray
    #     metric.bytes_value = convert_to_packed_float_array(value)
    # elif type == MetricDataType.DoubleArray:
    #     metric.datatype = MetricDataType.DoubleArray
    #     metric.bytes_value = convert_to_packed_double_array(value)
    # elif type == MetricDataType.BooleanArray:
    #     metric.datatype = MetricDataType.BooleanArray
    #     metric.bytes_value = convert_to_packed_boolean_array(value)
    # elif type == MetricDataType.StringArray:
    #     metric.datatype = MetricDataType.StringArray
    #     metric.bytes_value = convert_to_packed_string_array(value)
    # elif type == MetricDataType.DateTimeArray:
    #     metric.datatype = MetricDataType.DateTimeArray
    #     metric.bytes_value = convert_to_packed_datetime_array(value)
    else:
        print("Invalid: " + str(type))

    # Return the metric
    return metric
######################################################################

######################################################################
# Helper method for adding metrics to a container which can be a
# payload or a template
######################################################################
def addHistoricalMetric(container, name, alias, type, value):
    metric = addMetric(container, name, alias, type, value)
    metric.is_historical = True

    # Return the metric
    return metric
######################################################################

######################################################################
# Helper method for adding metrics to a container which can be a
# payload or a template
######################################################################
def addNullMetric(container, name, alias, type):
    metric = container.metrics.add()
    if name is not None:
        metric.name = name
    if alias is not None:
        metric.alias = alias
    metric.timestamp = int(round(time.time() * 1000))
    metric.is_null = True

    # print( "Type: " + str(type))

    if type == MetricDataType.Int8:
        metric.datatype = MetricDataType.Int8
    elif type == MetricDataType.Int16:
        metric.datatype = MetricDataType.Int16
    elif type == MetricDataType.Int32:
        metric.datatype = MetricDataType.Int32
    elif type == MetricDataType.Int64:
        metric.datatype = MetricDataType.Int64
    elif type == MetricDataType.UInt8:
        metric.datatype = MetricDataType.UInt8
    elif type == MetricDataType.UInt16:
        metric.datatype = MetricDataType.UInt16
    elif type == MetricDataType.UInt32:
        metric.datatype = MetricDataType.UInt32
    elif type == MetricDataType.UInt64:
        metric.datatype = MetricDataType.UInt64
    elif type == MetricDataType.Float:
        metric.datatype = MetricDataType.Float
    elif type == MetricDataType.Double:
        metric.datatype = MetricDataType.Double
    elif type == MetricDataType.Boolean:
        metric.datatype = MetricDataType.Boolean
    elif type == MetricDataType.String:
        metric.datatype = MetricDataType.String
    elif type == MetricDataType.DateTime:
        metric.datatype = MetricDataType.DateTime
    elif type == MetricDataType.Text:
        metric.datatype = MetricDataType.Text
    elif type == MetricDataType.UUID:
        metric.datatype = MetricDataType.UUID
    elif type == MetricDataType.Bytes:
        metric.datatype = MetricDataType.Bytes
    elif type == MetricDataType.File:
        metric.datatype = MetricDataType.File
    elif type == MetricDataType.Template:
        metric.datatype = MetricDataType.Template
    # elif type == MetricDataType.Int8Array:
    #     metric.datatype = MetricDataType.Int8Array
    # elif type == MetricDataType.Int16Array:
    #     metric.datatype = MetricDataType.Int16Array
    # elif type == MetricDataType.Int32Array:
    #     metric.datatype = MetricDataType.Int32Array
    # elif type == MetricDataType.Int64Array:
    #     metric.datatype = MetricDataType.Int64Array
    # elif type == MetricDataType.UInt8Array:
    #     metric.datatype = MetricDataType.UInt8Array
    # elif type == MetricDataType.UInt16Array:
    #     metric.datatype = MetricDataType.UInt16Array
    # elif type == MetricDataType.UInt32Array:
    #     metric.datatype = MetricDataType.UInt32Array
    # elif type == MetricDataType.UInt64Array:
    #     metric.datatype = MetricDataType.UInt64Array
    # elif type == MetricDataType.FloatArray:
    #     metric.datatype = MetricDataType.FloatArray
    # elif type == MetricDataType.DoubleArray:
    #     metric.datatype = MetricDataType.DoubleArray
    # elif type == MetricDataType.BooleanArray:
    #     metric.datatype = MetricDataType.BooleanArray
    # elif type == MetricDataType.StringArray:
    #     metric.datatype = MetricDataType.StringArray
    # elif type == MetricDataType.DateTimeArray:
    #     metric.datatype = MetricDataType.DateTimeArray
    else:
        print( "Invalid: " + str(type))

    # Return the metric
    return metric
######################################################################


######################################################################
# Helper method for getting the next sequence number
######################################################################
def getSeqNum():
    global seqNum
    retVal = seqNum
    # print("seqNum: " + str(retVal))
    seqNum += 1
    if seqNum == 256:
        seqNum = 0
    return retVal
######################################################################


######################################################################
# Helper method for getting the next birth/death sequence number
######################################################################
def getBdSeqNum(reset = False):
    global bdSeq
    if reset:
        bdSeq = 0
    retVal = bdSeq
    # print("bdSeqNum: " + str(retVal))
    bdSeq += 1
    if bdSeq == 256:
        bdSeq = 0
    return retVal
######################################################################


def addMetricDataset_from_dict(payload, name, alias, data):
    """
    Converts a dictionary into a Sparkplug B dataset metric.

    Args:
        payload (Payload): The payload to add the dataset metric to.
        name (str): The name of the dataset metric.
        alias (int): The alias for the metric.
        data (dict): The dictionary containing columns as keys and lists of values.

    Returns:
        The initialized dataset metric.

    Example:

        # Sample dictionary data
        data = {
            "Temperature": [23.5, 22.0, 21.8],
            "Humidity": [60.2, 58.9, 59.5],
            "Status": ["Normal", "Warning", "Alert"]
        }

        # Create a new Sparkplug B payload
        payload = Payload()

        # Convert the dictionary into a dataset metric
        dict_to_dataset_metric(payload, "environmental_data", 1, data)

    """
<<<<<<< HEAD:src/mqtt_spb_wrapper/spb_protobuf/sparkplug_b.py

=======
    
>>>>>>> 7035778 (update: adding in current changes to mqtt-spb-wrapper. fixed issue where int arrays caused exceptions):src/mqtt_spb_wrapper/spb_core/sparkplug_b.py
    # Extract columns and data types
    columns = list(data.keys())

    # Check for consistent column dimensions
    lengths = [len(v) for v in data.values()]
    if len(set(lengths)) > 1:
        raise ValueError(f"All columns must have the same number of rows, but got lengths: {lengths}")

    # Determine types based on the first row's types.
    first_row = [v[0] for v in data.values()]
    types = []
    for value in first_row:
        if isinstance(value, int):
<<<<<<< HEAD:src/mqtt_spb_wrapper/spb_protobuf/sparkplug_b.py
            types.append(DataSetDataType.Int64)
=======
            types.append(DataSetDataType.Int32)
>>>>>>> 7035778 (update: adding in current changes to mqtt-spb-wrapper. fixed issue where int arrays caused exceptions):src/mqtt_spb_wrapper/spb_core/sparkplug_b.py
        elif isinstance(value, float):
            types.append(DataSetDataType.Float)
        elif isinstance(value, str):
            types.append(DataSetDataType.String)
        else:
            raise ValueError(f"Unsupported data type: {type(value)}")

    # Initialize the dataset metric using the provided function
    dataset = initDatasetMetric(payload, name, alias, columns, types)

    # Get the number of rows from the data values
    num_rows = lengths[0]

    # Add rows to the dataset
    for i in range(num_rows):
        dataset_row = dataset.rows.add()
        for col in columns:
            element = dataset_row.elements.add()
            value = data[col][i]
            # Add the value based on its type
            if isinstance(value, int):
<<<<<<< HEAD:src/mqtt_spb_wrapper/spb_protobuf/sparkplug_b.py
                element.long_value = value
=======
                element.int_value = value
>>>>>>> 7035778 (update: adding in current changes to mqtt-spb-wrapper. fixed issue where int arrays caused exceptions):src/mqtt_spb_wrapper/spb_core/sparkplug_b.py
            elif isinstance(value, float):
                element.float_value = value
            elif isinstance(value, str):
                element.string_value = value
            else:
                raise ValueError(f"Unsupported value type: {type(value)}")

<<<<<<< HEAD:src/mqtt_spb_wrapper/spb_protobuf/sparkplug_b.py
    return dataset
=======
    return dataset
>>>>>>> 7035778 (update: adding in current changes to mqtt-spb-wrapper. fixed issue where int arrays caused exceptions):src/mqtt_spb_wrapper/spb_core/sparkplug_b.py
