"""
Trading-Technical-Indicators (tti) python library

File name: exceptions.py
    Implements all the customized exceptions used in the library.
"""


class NotEnoughInputData(Exception):
    def __init__(
        self,
        indicator_name,
        required_data_num,
        input_data_num,
        message="Not enough input data for calculating the "
        + "<ti_name> technical indicator. Minimum required "
        + "data are (<req_data_num>), but (<data_num>) found.",
    ):
        message = message.replace("<ti_name>", indicator_name)
        message = message.replace("<req_data_num>", str(required_data_num))
        message = message.replace("<data_num>", str(input_data_num))

        super().__init__(message)


class WrongValueForInputParameter(Exception):
    def __init__(
        self,
        parameter_value,
        parameter_name,
        parameter_supports,
        message="Wrong value (<p_value>) for input parameter "
        + "(<p_name>). Supported values are (<p_supported>).",
    ):
        message = message.replace("<p_value>", str(parameter_value))
        message = message.replace("<p_name>", parameter_name)
        message = message.replace("<p_supported>", str(parameter_supports))

        super().__init__(message)


class WrongTypeForInputParameter(Exception):
    def __init__(
        self,
        parameter_type,
        parameter_name,
        parameter_supported_type,
        message="Wrong type (<p_type>) for input parameter "
        + "(<p_name>). Supported type is (<p_supported>).",
    ):
        message = message.replace("<p_type>", str(parameter_type))
        message = message.replace("<p_name>", parameter_name)
        message = message.replace("<p_supported>", parameter_supported_type)

        super().__init__(message)


class NotValidInputDataForSimulation(Exception):
    def __init__(
        self,
        input_argument,
        details,
        message="Not valid input data for simulation, input " + "argument: <p_input_argument>. ",
    ):
        message = message.replace("<p_input_argument>", input_argument)
        message += details

        super().__init__(message)


class NoFeaturesSelectedForMLData(Exception):
    def __init__(self, ti_features, include_close_feature, include_volume_feature):
        message = (
            "No features selected for the ML data. ti_features = "
            + str(ti_features)
            + ", include_close_feature = "
            + str(include_close_feature)
            + ", include_volume_feature = "
            + str(include_volume_feature)
        )

        super().__init__(message)


class InputDataMissingForMLData(Exception):
    def __init__(self, column_name):
        message = "Required column `" + column_name + "` is missing from " + "the input data."

        super().__init__(message)


class NotEnoughDataForMachineLearningTraining(Exception):
    def __init__(self, input_data_length, required_data_length):
        message = (
            "Not enough input data for Machine Learning training. "
            + "Required data length is `"
            + str(required_data_length)
            + "` but `"
            + str(input_data_length)
            + "` were given."
        )

        super().__init__(message)


class NotEnoughDataForMachineLearningPrediction(Exception):
    def __init__(self, input_data_length, required_data_length):
        message = (
            "Not enough input data for Machine Learning prediction. "
            + "Required data length is `"
            + str(required_data_length)
            + "` but `"
            + str(input_data_length)
            + "` were given."
        )

        super().__init__(message)


class ModelTrainingIsNotSupported(Exception):
    def __init__(self):
        message = "ML model training is not supported for loaded models."

        super().__init__(message)


class NasdaqAssetsRetrievalError(Exception):
    def __init__(self, url, mc, fs, ie, ins, e):
        message = (
            f"Failed to download NASDAQ assets information from URL = {url}, with filters: "
            f"Market Categories = {mc}, Financial Statuses = {fs}, Ignore ETFs = {ie}, "
            f"Ignore Next Shares = {ins}. Error: {e}."
        )

        super().__init__(message)
