def custom_error(name, msgs):
    return{
        "errors": {
            name: msgs
        }
    }

class ErrorCode:
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    OUT_OF_QUOTA = 402
    NO_DATA = 403
