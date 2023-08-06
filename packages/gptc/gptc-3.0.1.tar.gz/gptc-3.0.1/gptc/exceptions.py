# SPDX-License-Identifier: GPL-3.0-or-later


class GPTCError(BaseException):
    pass


class ModelError(GPTCError):
    pass


class InvalidModelError(ModelError):
    pass
