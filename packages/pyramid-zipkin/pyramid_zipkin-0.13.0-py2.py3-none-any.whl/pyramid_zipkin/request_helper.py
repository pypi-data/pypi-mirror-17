# -*- coding: utf-8 -*-

import re

import six
from py_zipkin.zipkin import ZipkinAttrs
from py_zipkin.util import generate_random_64bit_string
from pyramid.interfaces import IRoutesMapper


DEFAULT_REQUEST_TRACING_PERCENT = 0.5


def get_trace_id(request):
    """Gets the trace id based on a request. If not present with the request,
    create a custom (depending on config: `zipkin.trace_id_generator`) or a
    completely random trace id.

    :param: current active pyramid request
    :returns: a 64-bit hex string
    """
    if 'X-B3-TraceId' in request.headers:
        trace_id = request.headers['X-B3-TraceId']
    elif 'zipkin.trace_id_generator' in request.registry.settings:
        trace_id = request.registry.settings[
            'zipkin.trace_id_generator'](request)
    else:
        trace_id = generate_random_64bit_string()

    return trace_id


def should_not_sample_path(request):
    """Decided whether current request path should be sampled or not. This is
    checked previous to `should_not_sample_route` and takes precedence.

    :param: current active pyramid request
    :returns: boolean whether current request path is blacklisted.
    """
    blacklisted_paths = request.registry.settings.get(
        'zipkin.blacklisted_paths', [])
    # Only compile strings, since even recompiling existing
    # compiled regexes takes time.
    regexes = [
        re.compile(r) if isinstance(r, six.string_types) else r
        for r in blacklisted_paths
    ]
    return any(r.match(request.path) for r in regexes)


def should_not_sample_route(request):
    """Decided whether current request route should be sampled or not.

    :param: current active pyramid request
    :returns: boolean whether current request route is blacklisted.
    """
    blacklisted_routes = request.registry.settings.get(
        'zipkin.blacklisted_routes', [])

    if not blacklisted_routes:
        return False
    route_mapper = request.registry.queryUtility(IRoutesMapper)
    route_info = route_mapper(request).get('route')
    return (route_info and route_info.name in blacklisted_routes)


def should_sample_as_per_zipkin_tracing_percent(tracing_percent, req_id):
    """Calculate whether the request should be traced as per tracing percent.

    :param tracing_percent: value between 0.0 to 100.0
    :type tracing_percent: float
    :param req_id: unique request id of the request
    :returns: boolean whether current request should be sampled.
    """
    if tracing_percent == 0.0:  # Prevent the ZeroDivision
        return False
    inverse_frequency = int((1.0 / tracing_percent) * 100)
    return int(req_id, 16) % inverse_frequency == 0


def is_tracing(request):
    """Determine if zipkin should be tracing
    1) Check whether the current request path is blacklisted.
    2) If not, check whether the current request route is blacklisted.
    3) If not, check if specific sampled header is present in the request.
    4) If not, Use a tracing percent (default: 0.5%) to decide.

    :param request: pyramid request object

    :returns: boolean True if zipkin should be tracing
    """
    if should_not_sample_path(request):
        return False
    elif should_not_sample_route(request):
        return False
    elif 'X-B3-Sampled' in request.headers:
        return request.headers.get('X-B3-Sampled') == '1'
    else:
        zipkin_tracing_percent = request.registry.settings.get(
            'zipkin.tracing_percent', DEFAULT_REQUEST_TRACING_PERCENT)
        return should_sample_as_per_zipkin_tracing_percent(
            zipkin_tracing_percent, request.zipkin_trace_id)


def create_zipkin_attr(request):
    """Create ZipkinAttrs object from a request with sampled flag as True.
    Attaches lazy attribute `zipkin_trace_id` with request which is then used
    throughout the tween.

    :param request: pyramid request object
    :rtype: :class:`pyramid_zipkin.request_helper.ZipkinAttrs`
    """
    request.set_property(get_trace_id, 'zipkin_trace_id', reify=True)

    trace_id = request.zipkin_trace_id
    is_sampled = is_tracing(request)
    span_id = request.headers.get(
        'X-B3-SpanId', generate_random_64bit_string())
    parent_span_id = request.headers.get('X-B3-ParentSpanId', None)
    flags = request.headers.get('X-B3-Flags', '0')
    return ZipkinAttrs(
        trace_id=trace_id,
        span_id=span_id,
        parent_span_id=parent_span_id,
        flags=flags,
        is_sampled=is_sampled,
    )


def get_binary_annotations(request, response):
    """Helper method for getting all binary annotations from the request.

    :param request: the Pyramid request object
    :param response: the Pyramid response object
    :returns: binary annotation dict of {str: str}
    """
    annotations = {
        'http.uri': request.path,
        'http.uri.qs': request.path_qs,
        'response_status_code': str(response.status_code),
    }
    settings = request.registry.settings
    if 'zipkin.set_extra_binary_annotations' in settings:
        annotations.update(
            settings['zipkin.set_extra_binary_annotations'](request, response)
        )
    return annotations
