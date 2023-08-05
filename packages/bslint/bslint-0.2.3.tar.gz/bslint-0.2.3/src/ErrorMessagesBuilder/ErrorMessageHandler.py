import src.ErrorMessagesBuilder.ErrorBuilder.ErrorMessagesConstants as Err


class ErrorMessageHandler:
    @staticmethod
    def get(key, params=[]):
        if key not in Err.ERROR_TABLE:
            raise ValueError("No Error with such key")
        return Err.ERROR_TABLE[key].get_message(params)



