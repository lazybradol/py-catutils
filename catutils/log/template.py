#!/usr/bin/python3
"""
BSD 2-Clause License

Copyright (c) 2019, wenqian
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from catutils.log.errors import TemplateFormatError, TemplateNotFoundError
from catutils.log.base import Logger
from catutils.log.replace import replace


class TemplateLogger:

    def __init__(self,
                 template_path,
                 logger: Logger):

        if isinstance(template_path, str):
            self.template_paths = [template_path]
        elif hasattr(template_path, '__iter__'):
            self.template_paths = list(template_path)
        else:
            raise AttributeError('template_path should be str or Iterable obj.')

        self.templates = {
            'default_base': '{content}',
            'default_base_with_datetime': '[%DATETIME%] {content}',
            'default_info': '%DATETIME% [INFO]  {content}',
            'default_warn': '%DATETIME% [WARN]  {content}',
            'default_error': '%DATETIME% [ERROR] {content}'
        }
        self.logger = logger

        for path in self.template_paths:

            with open(path, 'r') as f:
                for line in f.readlines():
                    line = line.strip()
                    words = line.split(':')
                    if len(words) < 2:
                        raise TemplateFormatError('Format error [{}]'.format(line))
                    self.templates[words[0]] = ':'.join(words[1:])

    def add_log(self,
                template_id: str,
                replaces: dict = None):
        if template_id not in self.templates:
            raise TemplateNotFoundError('Unknown template {}'.format(template_id))

        log = self.templates[template_id]

        if replaces is not None:
            log = log.format(**replaces)

        log = replace(log)

        self.logger.add_log(log)
