# -*- coding: utf-8 -*-
"""Writing of VCF files to ``file``-like objects

Currently, only writing to plain-text files is supported
"""

from . import parser

__author__ = 'Manuel Holtgrewe <manuel.holtgrewe@bihealth.de>'


def format_atomic(value):
    """Format atomic value"""
    if value is None:
        return '.'
    else:
        return str(value)


def format_value(field_info, value):
    """Format possibly compound value given the FieldInfo"""
    if field_info.number == 1:
        if value is None:
            return '.'
        else:
            return format_atomic(value)
    else:
        if not value:
            return '.'
        else:
            return ','.join(map(format_atomic, value))


class Writer:
    """Class for writing VCF files to ``file``-like objects

    Instead of using the constructor, use the class methods
    :py:meth:`~Writer.from_file` and
    :py:meth:`~Writer.from_path`.

    The writer has to be constructed with a :py:class:`~vcfpy.header.Header`
    and a :py:class:`~vcfpy.header.SamplesInfos` object and the full VCF
    header will be written immediately on construction.  This, of course,
    implies that modifying the header after construction is illegal.
    """

    @classmethod
    def from_file(klass, header, samples, stream, path=None):
        """Create new :py:class:`Writer` from file

        :param header: VCF header to use
        :param samples: SamplesInfos to use
        :param stream: ``file``-like object to write to
        :param path: optional string with path to store (for display only)
        """
        return Writer(header, samples, stream, path)

    @classmethod
    def from_path(klass, header, samples, path):
        """Create new :py:class:`Writer` from path

        :param header: VCF header to use
        :param samples: SamplesInfos to use
        :param path: the path to load from (converted to ``str`` for
            compatibility with ``path.py``)
        """
        path = str(path)
        if path.endswith('.gz'):
            raise NotImplementedError('Writing to bgzf not supported')
        else:
            f = open(path, 'wt')
        return klass.from_file(header, samples, f, path)

    def __init__(self, header, samples, stream, path=None):
        #: the :py:class:~vcfpy.header.Header` written out
        self.header = header
        #: the :py:class:~vcfpy.header.SamplesInfos` written out
        self.samples = samples
        #: stream (``file``-like object) to read from
        self.stream = stream
        #: optional ``str`` with the path to the stream
        self.path = path
        # write out headers
        self._write_header()

    def _write_header(self):
        """Write out the header"""
        for line in self.header.lines:
            print(line.serialize(), sep='', file=self.stream)
        if self.samples.names:
            print('\t'.join(
                list(parser.REQUIRE_SAMPLE_HEADER) + self.samples.names),
                file=self.stream)
        else:
            print('\t'.join(
                parser.REQUIRE_NO_SAMPLE_HEADER), file=self.stream)

    def close(self):
        """Close underlying stream"""
        self.stream.close()

    def write_record(self, record):
        """Write out the given :py:class:`vcfpy.record.Record` to this
        Writer"""
        self._serialize_record(record)

    def _serialize_record(self, record):
        """Serialize whole Record"""
        f = self._empty_to_dot
        row = [record.CHROM, record.POS]
        row.append(f(';'.join(record.ID)))
        row.append(f(record.REF))
        if not record.ALT:
            row.append('.')
        else:
            row.append(','.join([f(a.value) for a in record.ALT]))
        row.append(f(record.QUAL))
        row.append(f(';'.join(record.FILTER)))
        row.append(f(self._serialize_info(record)))
        row.append(':'.join(record.FORMAT))
        row += [self._serialize_call(record.FORMAT, c) for c in record.calls]
        print(*row, sep='\t', file=self.stream)

    def _serialize_info(self, record):
        """Return serialized version of record.INFO"""
        result = []
        for key, value in record.INFO.items():
            info = self.header.get_info_field_info(key)
            if info.type == 'Flag':
                result.append(key)
            else:
                result.append('{}={}'.format(key, format_value(info, value)))
        return ';'.join(result)

    def _serialize_call(self, format, call):
        """Return serialized version of the Call using the record's FORMAT'"""
        result = [format_value(self.header.get_format_field_info(key),
                               call.data[key]) for key in format]
        return ':'.join(result)

    def _empty_to_dot(self, val):
        """Return val or '.' if empty value"""
        if val == '' or val is None or val == []:
            return '.'
        else:
            return val
