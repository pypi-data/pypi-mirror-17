# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
QR Code and Micro QR Code implementation.

"QR Code" and "Micro QR Code" are registered trademarks of DENSO WAVE INCORPORATED.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD License
"""
from __future__ import absolute_import, unicode_literals
import sys
from . import encoder
from .encoder import QRCodeError, ErrorLevelError, ModeError, MaskError, \
    VersionError, DataOverflowError
from . import writers, utils

__version__ = '0.1.7'

__all__ = ('make', 'make_qr', 'make_micro', 'QRCode', 'QRCodeError',
           'ErrorLevelError', 'ModeError', 'MaskError', 'VersionError',
           'DataOverflowError')


def make(content, error=None, version=None, mode=None, mask=None, encoding=None,
         eci=False, micro=None, boost_error=True):
    """\
    Creates a (Micro) QR Code.

    This is main entry point to create QR Codes and Micro QR Codes.

    Aside from `content`, all parameters are optional and an optimal (minimal)
    (Micro) QR Code with a maximal error correction level (minimum "M") is
    generated.

    :param content: The data to encode. Either a Unicode string, an integer or
            bytes. If bytes are provided, the `encoding` parameter should be
            used to specify the used encoding.
    :type content: str, int, bytes
    :param error: Error correction level. If ``None`` (default), error
            correction level ``M`` is used (note: Micro QR Code version M1 does
            not support error correction. If an explicit error level is used,
            a M1 QR Code won't be generated).
            Valid values: ``None`` (allowing generation of M1 codes or use error
            correction level "M"), "L", "M", "Q", "H" (error correction level
            "H" isn't available for Micro QR Codes).

            =====================================   ===========================
            Error correction level                  Error correction capability
            =====================================   ===========================
            L                                       recovers  7% of data
            M (Segno's default unless version M1)   recovers 15% of data
            Q                                       recovers 25% of data
            H (not available for Micro QR Codes)    recovers 30% of data
            =====================================   ===========================

            Higher error levels may require larger QR Codes (see also `version`
            parameter).

            The `error` parameter is case insensitive.

            See also the `boost_error` parameter.
    :type error: str or None
    :param version: QR Code version. If the value is ``None`` (default), the
            minimal version which fits for the input data will be used.
            Valid values: "M1", "M2", "M3", "M4" (for Micro QR Codes) or an
            integer between 1 and 40 (for QR Codes).
            The `version` parameter is case insensitive.
    :type version: int, str or None.
    :param mode: "numeric", "alphanumeric", "byte", or "kanji". If the value is
            ``None`` (default) the appropriate mode will automatically be
            determined.
            If `version` refers a to Micro QR Code, this function may raise a
            :py:class:`ModeError` if the provided `mode` is not supported.

            ============    =======================
            Mode            (Micro) QR Code Version
            ============    =======================
            numeric         1 - 40, M1, M2, M3, M4
            alphanumeric    1 - 40,     M2, M3, M4
            byte            1 - 40,         M3, M4
            kanji           1 - 40,         M3, M4
            ============    =======================

            The `mode` parameter is case insensitive.

    :type mode: str or None
    :param mask: Data mask. If the value is ``None`` (default), the
            appropriate data mask is choosen automatically. If the `mask`
            parameter if provided, this function may raise a :py:exc:`MaskError`
            if the mask is invalid.
    :type mask: int or None
    :param encoding: Indicates the encoding in mode "byte". By default
            (`encoding` is ``None``) the implementation tries to use the
            standard conform ISO/IEC 8859-1 encoding and if it does not fit, it
            will use UTF-8. Note that no ECI mode indicator is inserted by
            default (see `eci`).
            The `encoding` parameter is case insensitive.
    :type encoding: str or None
    :param bool eci: Indicates if binary data which does not use the default
            encoding (ISO/IEC 8859-1) should enforce the ECI mode. Since a lot
            of QR Code readers do not support the ECI mode, this feature is
            disabled by default and the data is encoded in the provided
            `encoding` using the usual "byte" mode. Set `eci` to ``True`` if
            an ECI header should be inserted into the QR Code. Note that
            the implementation may not know the ECI designator for the provided
            `encoding` and may raise an exception if the ECI designator cannot
            be found.
            The ECI mode is not supported by Micro QR Codes.
    :param micro: If `version` is ``None`` this parameter can be used
            to allow the creation of a Micro QR Code.
            If set to ``False``, a QR Code is generated. If set to
            ``None`` (default) a Micro QR Code may be generated if applicable.
            If set to ``True`` the algorithm generates a Micro QR Code or
            raises an exception if the `mode` is not compatible or the `content`
            is too large for Micro QR Codes.
    :type micro: bool or None
    :param bool boost_error: Indicates if the error correction level may be
            increased if it does not affect the version (default: ``True``).
            If set to ``True``, the ``error`` parameter is interpreted as
            minimum error level. If set to ``False``, the resulting (Micro) QR
            Code uses the provided ``error`` level (or the default error
            correction level, if error is ``None``)
    :raises: :py:exc:`QRCodeError`: In case of a problem. In fact, it's more
            likely that a derived exception is thrown:
            :py:exc:`ModeError`: In case of problems with the mode (i.e. invalid
            mode or invalid `mode` / `version` combination.
            :py:exc:`VersionError`: In case the `version` is invalid or the
            `micro` parameter contradicts the provided `version`.
            :py:exc:`ErrorLevelError`: In case the error level is invalid or the
            error level is not supported by the provided `version`.
            :py:exc:`DataOverflowError`: In case the data does not fit into a
            (Micro) QR Code or it does not fit into the provided `version`.
            :py:exc:`MaskError`: In case an invalid data mask was specified.
    :rtype: QRCode
    """
    return QRCode(encoder.encode(content, error, version, mode, mask, encoding,
                                 eci, micro, boost_error=boost_error))


def make_qr(content, error=None, version=None, mode=None, mask=None,
            encoding=None, eci=False, boost_error=True):
    """\
    Creates a QR Code (never a Micro QR Code).

    See :py:func:`make` for a description of the parameters.

    :rtype: QRCode
    """
    return make(content, error=error, version=version, mode=mode, mask=mask,
                encoding=encoding, eci=eci, micro=False, boost_error=boost_error)


def make_micro(content, error=None, version=None, mode=None, mask=None,
               encoding=None, boost_error=True):
    """\
    Creates a Micro QR Code.

    See :py:func:`make` for a description of the parameters.

    Note: Error correction level "H" isn't available for Micro QR Codes. If
    used, this function raises a :py:class:`segno.ErrorLevelError`.

    :rtype: QRCode
    """
    return make(content, error=error, version=version, mode=mode, mask=mask,
                encoding=encoding, micro=True, boost_error=boost_error)


class QRCode(object):
    """\
    Represents a (Micro) QR Code.
    """
    def __init__(self, code):
        """\
        Initializes the QR Code object.

        :param code: An object with a ``matrix``, ``version``, ``error``,
            ``mask`` and ``segments`` attribute.
        """
        self.matrix = code.matrix
        """Returns the matrix (tuple of bytearrays)."""
        self.mask = code.mask
        """Returns the data mask pattern reference (an integer)."""
        self._version = code.version
        self._error = code.error
        self._mode = code.segments[0].mode if len(code.segments) == 1 else None

    @property
    def version(self):
        """\
        (Micro) QR Code version. Either a string ("M1", "M2", "M3", "M4") or
        an integer in the range of 1 .. 40.
        """
        return encoder.get_version_name(self._version)

    @property
    def error(self):
        """\
        Error correction level; either a string ("L", "M", "Q", "H") or ``None``
        if the QR Code provides no error correction (Micro QR Code version M1)
        """
        if self._error is None:
            return None
        return encoder.get_error_name(self._error)

    @property
    def mode(self):
        """\
        String indicating the mode ("numeric", "alphanumeric", "byte", "kanji").
        May be ``None`` if multiple modes are used.
        """
        if self._mode is not None:
            return encoder.get_mode_name(self._mode)
        return None

    @property
    def designator(self):
        """\
        Returns the version and error correction level as string `V-E` where
        `V` represents the version number and `E` the error level.
        """
        version = str(self.version)
        return '-'.join((version, self.error) if self.error else (version,))

    @property
    def default_border_size(self):
        """\
        Indicates the default border size aka quiet zone.
        """
        return utils.get_default_border_size(self._version)

    @property
    def is_micro(self):
        """\
        Indicates if this QR Code is a Micro QR Code
        """
        return self._version < 1

    def __eq__(self, other):
        return self.matrix == other.matrix

    def symbol_size(self, scale=1, border=None):
        """\
        Returns the symbol size (width x height) with the provided border and
        scaling factor.

        :param scale: Indicates the size of a single module (default: 1).
                The size of a module depends on the used output format; i.e.
                in a PNG context, a scaling factor of 2 indicates that a module
                has a size of 2 x 2 pixel. Some outputs (i.e. SVG) accept
                floating point values.
        :type scale: int or float
        :param int border: The border size or ``None`` to specify the
                default quiet zone (4 for QR Codes, 2 for Micro QR Codes).
        :rtype: tuple (width, height)
        """
        return utils.get_symbol_size(self._version, scale=scale, border=border)

    def matrix_iter(self, scale=1, border=None):
        """\
        Returns an iterator over the matrix which includes the border.

        The border is interpreted as light module.

        :param int border: The size of border / quiet zone or ``None`` to
                indicate the default border.
        :raises: :py:exc:`ValueError` if the border is invalid (i.e. negative).
        """
        return utils.matrix_iter(self.matrix, self._version, scale, border)

    def show(self, delete_after=20, scale=10, border=None, color='#000',
             background='#fff'):  # pragma: no cover
        """\
        Displays this QR code.

        This method is mainly intended for debugging purposes.

        This method saves the output of the :py:meth:`png` method (by default
        with a scaling factor of 10) to a temporary file and opens it with the
        standard PNG viewer application or within the standard webbrowser.
        The temporary file is deleted afterwards (unless `delete_after` is set
        to ``None``).

        If this method does not show any result, try to increase the
        `delete_after` value or set it to ``None``

        :param delete_after: Time in seconds to wait till the temporary file is
                deleted.
        """
        import os
        import time
        import tempfile
        import webbrowser
        import threading
        try:  # Python 2
            from urlparse import urljoin
            from urllib import pathname2url
        except ImportError:  # Python 3
            from urllib.parse import urljoin
            from urllib.request import pathname2url

        def delete_file(name):
            time.sleep(delete_after)
            try:
                os.unlink(name)
            except OSError:
                pass

        f = tempfile.NamedTemporaryFile('wb', suffix='.png', delete=False)
        try:
            self.save(f, scale=scale, color=color, background=background,
                      border=border)
        except:
            f.close()
            os.unlink(f.name)
            raise
        f.close()
        webbrowser.open_new_tab(urljoin('file:', pathname2url(f.name)))
        if delete_after is not None:
            t = threading.Thread(target=delete_file, args=(f.name,))
            t.start()

    def svg_data_uri(self, scale=1, border=None, color='#000', background=None,
                     xmldecl=False, svgns=True, title=None, desc=None,
                     svgid=None, svgclass='segno', lineclass='qrline',
                     omitsize=False, unit='', encoding='utf-8', svgversion=None,
                     nl=False, encode_minimal=False, omit_charset=False):
        """\
        Converts the QR Code into a SVG data URI.

        The XML declaration is omitted by default (set ``xmldecl`` to ``True``
        to enable it), further the newline is omitted by default (set ``nl`` to
        ``True`` to enable it).

        Aside from the missing ``out`` parameter and the different ``xmldecl``
        and ``nl`` default values and the additional parameter ``encode_minimal``
        and ``omit_charset`` this method uses the same parameters as the
        usual SVG serializer.

        :param bool encode_minimal: Indicates if the resulting data URI should
                        use minimal percent encoding (disabled by default).
        :param bool omit_charset: Indicates if the ``;charset=...`` should be omitted
                        (disabled by default)
        :rtype: str
        """
        return writers.as_svg_data_uri(self.matrix, self._version, scale=scale,
                                border=border, color=color,
                                background=background, xmldecl=xmldecl,
                                svgns=svgns, title=title, desc=desc,
                                svgid=svgid, svgclass=svgclass,
                                lineclass=lineclass, omitsize=omitsize,
                                unit=unit, encoding=encoding,
                                svgversion=svgversion, nl=nl,
                                encode_minimal=encode_minimal,
                                omit_charset=omit_charset)

    def png_data_uri(self, scale=1, border=None, color='#000', background='#fff',
                     compresslevel=9, addad=True):
        """\
        Converts the QR Code into a PNG data URI.

        :rtype: str
        """
        return writers.as_png_data_uri(self.matrix, self._version, scale=scale,
                                border=border, color=color,
                                background=background,
                                compresslevel=compresslevel, addad=addad)

    def terminal(self, out=None, border=None):
        """\
        Serializes the matrix as ANSI escape code.

        :param out: Filename or a file-like object supporting to write text.
                If ``None`` (default), the matrix is written to ``sys.stdout``.
        :param int border: Integer indicating the size of the quiet zone.
                If set to ``None`` (default), the recommended border size
                will be used (``4`` for QR Codes, ``2`` for a Micro QR Codes).
        """
        if out is None and sys.platform == 'win32':  # pragma: no cover
            # Windows < 10 does not support ANSI escape sequences, try to
            # call the a Windows specific terminal output which uses the
            # Windows API.
            try:
                writers.write_terminal_win(self.matrix, self._version, border)
            except OSError:
                # Use the standard output even if it may print garbage
                writers.write_terminal(self.matrix, self._version, sys.stdout,
                                       border)
        else:
            writers.write_terminal(self.matrix, self._version, out or sys.stdout,
                                   border)

    def save(self, out, kind=None, **kw):
        """\
        Serializes the QR Code in one of the supported formats.
        The serialization format depends on the filename extension.

        **Common keywords**


        ==========    ==============================================================
        Name          Description
        ==========    ==============================================================
        scale         Integer or float indicating the size of a single module.
                      Default: 1. The interpretation of the scaling factor depends
                      on the serializer. For pixel-based output (like PNG) the
                      scaling factor is interepreted as pixel-size (1 = 1 pixel).
                      EPS interprets ``1`` as 1 point (1/72 inch) per module.
                      Some serializers (like SVG) accept float values. If the
                      serializer does not accept float values, the value will be
                      converted to an integer value (note: int(1.6) == 1).
        border        Integer indicating the size of the quiet zone.
                      If set to ``None`` (default), the recommended border size
                      will be used (``4`` for QR Codes, ``2`` for a Micro QR Codes).
        color         A string or tuple representing a color value for the dark
                      modules. The default value is "black".  The color can be
                      provided as ``(R, G, B)`` tuple, as web color name
                      (like "red") or in hexadecimal format (``#RGB`` or
                      ``#RRGGBB``). Some serializers (SVG and PNG) accept an alpha
                      transparency value like ``#RRGGBBAA``.
        background    A string or tuple representing a color for the light modules
                      or background. See "color" for valid values.
                      The default value depends on the serializer. SVG uses no
                      background color (``None``) by default, other serializers
                      use "white" as default background color.
        ==========    ==============================================================


        **Scalable Vector Graphics (SVG)**

        =============    ==============================================================
        Name             Description
        =============    ==============================================================
        kind             "svg" or "svgz" (to create a gzip compressed SVG)
        scale            integer or float
        color            Default: "#000" (black)
                         ``None`` is a valid value. If set to ``None``, the resulting
                         path won't have a "stroke" attribute. The "stroke" attribute
                         may be defined via CSS (external).
                         If an alpha channel is defined, the output depends of the
                         used SVG version. For SVG versions >= 2.0, the "stroke"
                         attribute will have a value like "rgba(R, G, B, A)", otherwise
                         the path gets another attribute "stroke-opacity" to emulate
                         the alpha channel.
                         To minimize the document size, the SVG serializer uses
                         automatically the shortest color representation: If
                         a value like "#000000" is provided, the resulting
                         document will have a color value of "#000". If the color
                         is "#FF0000", the resulting color is not "#F00", but
                         the web color name "red".
        background       Default value ``None``. If this paramater is set to another
                         value, the resulting image will have another path which
                         is used to define the background color.
                         If an alpha channel is used, the resulting path may
                         have a "fill-opacity" attribute (for SVG version < 2.0)
                         or the "fill" attribute has a "rgba(R, G, B, A)" value.
                         See keyword "color" for further details.
        xmldecl          Boolean value (default: ``True``) indicating whether the
                         document should have an XML declaration header.
                         Set to ``False`` to omit the header.
        svgns            Boolean value (default: ``True``) indicating whether the
                         document should have an explicit SVG namespace declaration.
                         Set to ``False`` to omit the namespace declaration.
                         The latter might be useful if the document should be
                         embedded into a HTML 5 document where the SVG namespace
                         is implicitly defined.
        title            String (default: ``None``) Optional title of the generated
                         SVG document.
        desc             String (default: ``None``) Optional description of the
                         generated SVG document.
        svgid            A string indicating the ID of the SVG document
                         (if set to ``None`` (default), the SVG element won't have
                         an ID).
        svgclass         Default: "segno". The CSS class of the SVG document
                         (if set to ``None``, the SVG element won't have a class).
        lineclass        Default: "qrline". The CSS class of the path element
                         (which draws the dark modules (if set to ``None``, the path
                         won't have a class).
        omitsize         Indicates if width and height attributes should be
                         omitted (default: ``False``). If these attributes are
                         omitted, a ``viewBox`` attribute will be added to the
                         document.
        unit             Default: ``None``
                         Inidctaes the unit for width / height and other coordinates.
                         By default, the unit is unspecified and all values are
                         in the user space.
                         Valid values: em, ex, px, pt, pc, cm, mm, in, and percentages
                         (any string is accepted, this parameter is not validated
                         by the serializer)
        encoding         Encoding of the XML document. "utf-8" by default.
        svgversion       SVG version (default: ``None``). If specified (a float),
                         the resulting document has an explicit "version" attribute.
                         If set to ``None``, the document won't have a "version"
                         attribute. This parameter is not validated.
        compresslevel    Default: 9. This parameter is only valid, if a compressed
                         SVG document should be created (file extension "svgz").
                         1 is fastest and produces the least compression, 9 is slowest
                         and produces the most. 0 is no compression.
        =============    ==============================================================


        **Portable Network Graphics (PNG)**

        =============    ==============================================================
        Name             Description
        =============    ==============================================================
        kind             "png"
        scale            integer
        color            Default: "#000" (black)
                         ``None`` is a valid value iff background is not ``None``.
        background       Default value ``#fff`` (white)
                         See keyword "color" for further details.
        compresslevel    Default: 9. Integer indicating the compression level
                         for the ``IDAT`` (data) chunk.
                         1 is fastest and produces the least compression, 9 is slowest
                         and produces the most. 0 is no compression.
        addad            Boolean value (default: True) to (dis-)allow a "Software"
                         comment indicating that the file was created by Segno.
        =============    ==============================================================


        **Encapsulated PostScript (EPS)**

        =============    ==============================================================
        Name             Description
        =============    ==============================================================
        kind             "eps"
        scale            integer or float
        color            Default: "#000" (black)
        background       Default value ``#fff`` (white)
        =============    ==============================================================


        **Portable Document Format (PDF)**

        =============    ==============================================================
        Name             Description
        =============    ==============================================================
        kind             "pdf"
        scale            integer or float
        compresslevel    Default: 9. Integer indicating the compression level.
                         1 is fastest and produces the least compression, 9 is slowest
                         and produces the most. 0 is no compression.
        =============    ==============================================================


        **Text (TXT)**

        Does not support the "scale" keyword!

        =============    ==============================================================
        Name             Description
        =============    ==============================================================
        kind             "txt"
        color            Default: "1"
        background       Default: "0"
        =============    ==============================================================


        **ANSI escape code**

        Supports the "border" keyword, only!

        =============    ==============================================================
        Name             Description
        =============    ==============================================================
        kind             "ans"
        =============    ==============================================================


        **Portable Bitmap (PBM)**

        =============    ==============================================================
        Name             Description
        =============    ==============================================================
        kind             "pbm"
        scale            integer
        plain            Default: False. Boolean to switch between the P4 and P1 format.
                         If set to ``True``, the (outdated) P1 serialization format is
                         used.
        =============    ==============================================================


        :param out: A filename or a writable file-like object with a
                ``name`` attribute. Use the `kind` parameter if `out` is
                a :py:class:`io.ByteIO` or :py:class:`io.StringIO` stream which
                don't have a ``name`` attribute.
        :param kind: If the desired output format cannot be determined from
                the ``out`` parameter, this parameter can be used to indicate the
                serialization format (i.e. "svg" to enforce SVG output)
        :param kw: Any of the supported keywords by the specific serialization
                method.
        """
        writers.save(self.matrix, self._version, out, kind, **kw)

    def __getattr__(self, name):
        """\
        This is used to plug-in external serializers.

        When a "to_<name>" method is invoked, this method tries to find
        a ``segno.plugin.converter`` plugin with the provided ``<name>``.
        If such a plugin exists, a callable function is returned. The result
        of invoking the function depends on the plugin.
        """
        if name.startswith('to_'):
            from pkg_resources import iter_entry_points
            from functools import partial
            for ep in iter_entry_points(group='segno.plugin.converter',
                                        name=name[3:]):
                plugin = ep.load()
                return partial(plugin, self)
        raise AttributeError('{0} object has no attribute {1}'
                             .format(self.__class__, name))
