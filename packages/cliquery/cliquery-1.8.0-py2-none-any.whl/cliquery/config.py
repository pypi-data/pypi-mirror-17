"""Read and initialize cliquery configuration"""

import os
import subprocess
import sys
import webbrowser

from six import iteritems, iterkeys
from six.moves import xrange as range


CONFIG_DIR = os.path.dirname(os.path.realpath(__file__))
if os.path.isfile('{0}/.local.cliqrc'.format(CONFIG_DIR)):
    CONFIG_FPATH = '{0}/.local.cliqrc'.format(CONFIG_DIR)
else:
    CONFIG_FPATH = '{0}/.cliqrc'.format(CONFIG_DIR)
CONFIG = {}


def edit_config():
    """Invoke text editor on configuration file."""
    EDITOR = os.environ.get('EDITOR', 'vim')
    subprocess.call([EDITOR, CONFIG_FPATH])
    

def read_config():
    """Read in fields from .cliqrc or .local.cliqrc as a dict."""
    def add_field(line):
        """Read in a configuration field and its value."""
        split_line = line.split(':')
        field = split_line[0]
        if field in fields:
            fields[field] = ':'.join(split_line[1:]).strip()
            return True
        return False

    with open(CONFIG_FPATH, 'r') as cfg:
        fields = {'google_api_key': '',
                  'google_engine_key': '',
                  'wolfram_api_key': '',
                  'browser': ''}

        # Attempt to read configuration fields excluding bookmarks
        lines = []
        bookmarks_reached = False
        for _ in range(len(fields.keys())):
            line = cfg.readline()
            if line.startswith('bookmarks:'):
                bookmarks_reached = True
                break

            if not add_field(line):
                lines.append(line)

        # Try to resolve fields that were found but unassigned
        for i, key in enumerate(iterkeys(fields)):
            if not fields[key] and i < len(lines):
                fields[key] = lines[i].strip()

        # Attempt to read bookmarks
        bkmarks = []
        cfg_bkmarks = cfg.read()

        if cfg_bkmarks.startswith('bookmarks:'):
            cfg_bkmarks = ':'.join(cfg_bkmarks.split(':')[1:]).split('\n')
            bkmarks = [b.strip() for b in cfg_bkmarks if b.strip()]
        elif bookmarks_reached:
            cfg_bkmarks = cfg_bkmarks.split('\n')
            bkmarks = [b.strip() for b in cfg_bkmarks if b.strip()]
        fields['bookmarks'] = bkmarks

        return fields


def set_config():
    """Set optional API keys, browser, and bookmarks in CONFIG."""
    browser_name = ''
    for key, val in iteritems(read_config()):
        if key == 'browser':
            browser_name = val
        else:
            CONFIG[key] = val

    # There may be multiple browser options given, pick the first which works
    if ',' in browser_name:
        browser_names = browser_name.split(',')
    else:
        browser_names = browser_name.split()

    if browser_names:
        for brow_name in browser_names:
            try:
                CONFIG['browser'] = brow_name
                CONFIG['browser_obj'] = webbrowser.get(brow_name)
                return
            except webbrowser.Error:
                pass

    # If no valid browser found then use webbrowser to automatically detect one
    try:
        if sys.platform == 'win32':
            # Windows
            browser_name = 'windows-default'
            browser_obj = webbrowser.get(browser_name)
        elif sys.platform == 'darwin':
            # Mac OSX
            browser_name = 'macosx'
            browser_obj = webbrowser.get(browser_name)
        else:
            browser_name = 'Automatically detected'
            browser_obj = webbrowser.get()
        CONFIG['browser'] = browser_name
        CONFIG['browser_obj'] = browser_obj
    except webbrowser.Error:
        pass
