from connect.eaas.core.enums import ResultType


class _Response:
    def __init__(self, status, output=None):
        self.status = status
        self.output = output

    @classmethod
    def done(cls, *args, **kwargs):
        return cls(ResultType.SUCCESS)

    @classmethod
    def fail(cls, output=None):
        return cls(ResultType.FAIL, output=output)


class BackgroundResponse(_Response):

    def __init__(self, status, countdown=30, output=None):
        super().__init__(status, output)
        self.countdown = 30 if countdown < 30 else countdown

    @classmethod
    def skip(cls, output=None):
        return cls(ResultType.SKIP, output=output)

    @classmethod
    def reschedule(cls, countdown=30):
        return cls(ResultType.RESCHEDULE, countdown=countdown)

    @classmethod
    def slow_process_reschedule(cls, countdown=300):
        return cls(
            ResultType.RESCHEDULE,
            countdown=300 if countdown < 300 else countdown,
        )


class ProcessingResponse(BackgroundResponse):
    pass


class InteractiveResponse(_Response):
    def __init__(self, status, http_status, headers, body, output):
        super().__init__(status, output)
        self.http_status = http_status
        self.headers = headers
        self.body = body

    @property
    def data(self):
        return {
            'http_status': self.http_status,
            'headers': self.headers,
            'body': self.body,
        }

    @classmethod
    def done(cls, http_status=200, headers=None, body=None):
        return cls(ResultType.SUCCESS, http_status, headers, body, None)

    @classmethod
    def fail(cls, http_status=400, headers=None, body=None, output=None):
        return cls(ResultType.FAIL, http_status, headers, body, output)


class ValidationResponse(InteractiveResponse):
    def __init__(self, status, data, output=None):
        http_status = 200 if status == ResultType.SUCCESS else 400
        super().__init__(status, http_status, None, data, output)

    @classmethod
    def done(cls, data):
        return cls(ResultType.SUCCESS, data)

    @classmethod
    def fail(cls, data=None, output=None):
        return cls(ResultType.FAIL, data=data, output=output)


class CustomEventResponse(InteractiveResponse):
    pass


class ProductActionResponse(InteractiveResponse):
    pass


class ScheduledExecutionResponse(_Response):
    pass
