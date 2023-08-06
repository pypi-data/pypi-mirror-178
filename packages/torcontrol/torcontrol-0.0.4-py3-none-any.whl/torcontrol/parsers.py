'''
Minimalistic Tor Controller

This module contains reply parsers.

Many parts of this code are based on Stem:
:copyright 2012-2020, Damian Johnson and The Tor Project

:copyright: Copyright 2022 AXY axy@declassed.art
:license: LGPLv3, see LICENSE for details.
'''

import base64
import binascii


def safe_b64decode(s):
    '''
    Restore padding and decode.
    '''
    return base64.b64decode(s + ('=' * (len(s) % 4)))

def base64_to_hex(s):
    '''
    Decode a base64 value to uppercase hex.
    '''
    return binascii.hexlify(
        safe_b64decode(s)
    ).decode('ascii').upper()

def _parse_r_line(parts):
    # Parses a RouterStatusEntry's 'r' line. They're very nearly identical for
    # all current entry types (v2, v3, and microdescriptor v3) with one little
    # wrinkle: only the microdescriptor flavor excludes a 'digest' field.
    #
    # For v2 and v3 router status entries:
    #   "r" nickname identity digest publication IP ORPort DirPort
    #   example: r mauer BD7xbfsCFku3+tgybEZsg8Yjhvw itcuKQ6PuPLJ7m/Oi928WjO2j8g 2012-06-22 13:19:32 80.101.105.103 9001 0
    #
    # For v3 microdescriptor router status entries:
    #   "r" nickname identity publication IP ORPort DirPort
    #   example: r Konata ARIJF2zbqirB9IwsW0mQznccWww 2012-09-24 13:40:40 69.64.48.168 9001 9030

    if len(parts) < 8:
        raise ValueError(f"'r' line must have eight values: {parts}")

    return dict(
        nickname    = parts[0],
        fingerprint = base64_to_hex(parts[1]),
        digest      = base64_to_hex(parts[2]),
        published   = f'{parts[3]}T{parts[4]}',
        address     = parts[5],
        or_port     = int(parts[6]),
        dir_port    = int(parts[7])
    )

def _parse_a_line(parts):
    # "a" SP address ":" portlist
    # example: a [2001:888:2133:0:82:94:251:204]:9001

    if ':' not in parts[0]:
        raise ValueError(f"'a' line must be of the form '[address]:[ports]': {parts[0]}")

    address, port = parts[0].rsplit(':', 1)
    return dict(
        or_addresses = [address.lstrip('[').rstrip(']')],
        port = int(port)
    )

def _parse_s_line(parts):
    # "s" Flags
    # example: s Named Running Stable Valid

    return dict(
        flags = set(parts)
    )

def _parse_v_line(parts):
    # "v" version
    # example: v Tor 0.2.2.35
    #
    # The spec says that if this starts with "Tor " then what follows is a
    # tor version. If not then it has "upgraded to a more sophisticated
    # protocol versioning system".

    return dict(
        version = parts
    )

def _parse_w_line(parts):
    # "w" "Bandwidth=" INT ["Measured=" INT] ["Unmeasured=1"]
    # example: w Bandwidth=7980

    result = dict()
    for item in parts:
        if '=' in item:
            k, v = item.split('=', 1)
            if v.isdigit():
                v = int(v)
        else:
            k, v = item, None
        result[k] = v
    return dict(
        w = result
    )

def _parse_p_line(parts):
    # "p" ("accept" / "reject") PortList
    #
    # examples:
    #
    #   p accept 80,110,143,443,993,995,6660-6669,6697,7000-7001
    #   p reject 1-65535

    if parts[0] not in ['accept', 'reject']:
        raise ValueError(f"Exit policy must be either 'accept' or 'reject': {parts}")
    if len(parts) != 2:
        raise ValueError(f"Exit policy must include port ranges: {parts}")

    port_range = []
    for port_entry in parts[1].split(','):
        if '-' in port_entry:
            min_port, max_port = port_entry.split('-', 1)
        else:
            min_port = max_port = port_entry
        port_range.append((int(min_port), int(max_port)))

    return dict(
        exit_policy = {parts[0]: port_range}
    )

def _parse_id_line(parts):
    # "id" "ed25519" ed25519-identity
    #
    # examples:
    #
    #   id ed25519 none
    #   id ed25519 8RH34kO07Pp+XYwzdoATVyCibIvmbslUjRkAm7J4IA8

    if len(parts) < 2:
        raise ValueError(f"'id' lines should contain both the key type and digest: {parts}")

    return dict(
        identifier_type = parts[0],
        identifier = parts[1]
    )

def _parse_m_line(parts):
    # "m" methods 1*(algorithm "=" digest)
    # example: m 8,9,10,11,12 sha256=g1vx9si329muxV3tquWIXXySNOIwRGMeAESKs/v4DWs
    #
    # for micridescriptors:
    #
    # "m" digest
    # example: m aiUklwBrua82obG5AsTX+iEpkjQA2+AQHxZ7GwMfY70

    if len(parts) == 1:
        # assume the line is a microdescriptor digest
        return dict(
            microdescriptor_digest = parts[0]
        )
    else:
        try:
            methods = [int(entry) for entry in parts[0].split(',')]
        except ValueError:
            raise ValueError(f'microdescriptor methods should be a series of comma separated integers: {parts}')

        hashes = {}
        for entry in parts[1:]:
            if '=' not in entry:
                raise ValueError(f"m line can only have a series of 'algorithm=digest' mappings after the methods: {parts}")

            hash_name, digest = entry.split('=', 1)
            hashes[hash_name] = digest

        return dict(
            microdescriptor_hashes = [(methods, hashes)]
        )

def parse_circuit_status(line):
    parts = line.split()
    path = []
    params = dict()
    if len(parts) >= 3:
        for item in parts[2].split(','):
            if '~' in item:
                fingerprint = item.split('~', 1)[0]  # drop nickname
            else:
                fingerprint = item
            if fingerprint.startswith('$'):
                fingerprint = fingerprint[1:]
            path.append(fingerprint)

        for item in parts[3:]:
            if '=' in item:
                k, v = item.split('=', 1)
                params[k.lower()] = v

        if 'build_flags' in params:
            params['build_flags'] = set(params['build_flags'].split(','))

        # XXX unescape socks_username, socks_password if any

    return dict(
        id     = parts[0],
        status = parts[1],
        path   = path,
        **params
    )

def extract_event_type(event):
    '''
    Extract type from event.
    '''
    if len(event[0]) < 4:
        return None
    else:
        return event[0][4:].split(' ', 1)[0]

def concat_circ_event(lines):
    '''
    Concatenate CIRC event lines as if it was a single line.
    '''
    parts = [lines[0][len('650 CIRC '):]]
    for line in lines[1:]:
        if line[3] == '-':
            parts.append(line[4:])
    return ' '.join(parts)

def parse_circuit_event(event):
    '''
    Parse CIRC event.
    '''
    return parse_circuit_status(concat_circ_event(event))

def parse_stream_event(event):
    '''
    Parse STREAM event.
    '''
    parts = event[0].split(' ')
    params = dict()
    for item in parts[6:]:
        if '=' in item:
            k, v = item.split('=', 1)
            params[k.lower()] = v

    return dict(
        id         = parts[2],
        status     = parts[3],
        circuit_id = parts[4],
        target     = parts[5],
        **params
    )
