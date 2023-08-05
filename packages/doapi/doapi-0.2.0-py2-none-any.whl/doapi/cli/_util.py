from   __future__  import print_function
import argparse
from   collections import defaultdict, Iterator
import json
import os
import os.path
import re
import sys
from   ..          import __version__, DOEncoder, doapi, WaitTimeoutError

universal = argparse.ArgumentParser(add_help=False)
tokenopts = universal.add_mutually_exclusive_group()
tokenopts.add_argument('--api-token', metavar='TOKEN',
                       help='DigitalOcean API token')
tokenopts.add_argument('--api-token-file', type=argparse.FileType('r'),
                       metavar='FILE',
                       help='file containing DigitalOcean API token')
universal.add_argument('--timeout', type=float, metavar='SECONDS',
                       help='HTTP request timeout')
universal.add_argument('--endpoint', metavar='URL',
                       help='where to make API requests')
universal.add_argument('-V', '--version', action='version',
                                          version='doapi ' + __version__)

waitbase = argparse.ArgumentParser(add_help=False)
waitbase.add_argument('--wait-time', type=float, metavar='SECONDS',
                      help='maximum length of time to wait')
waitbase.add_argument('--wait-interval', type=float, metavar='SECONDS',
                      help='how often to check progress')

waitopts = argparse.ArgumentParser(parents=[waitbase], add_help=False)
waitopts.add_argument('-w', '--wait', action='store_true',
                      help='Wait for the operation to finish')


class Cache(object):
    ### TODO: When not all objects of a type have been fetched, labels that are
    ### valid IDs (or fingerprints or potential slugs) should not cause
    ### everything to be fetched (but the result should still be cached).

    groupby = {
        "droplet": ("id", "name"),
        "sshkey": ("id", "fingerprint", "name"),
        "image": ("id", "slug", "name"),
        ###"action": ("id",),
    }

    def __init__(self, client):
        self.client = client
        self.caches = {}

    def cache(self, objects, key):
        if key not in self.caches:
            objects = list(objects)
            grouped = {key: objects}
            for attr in self.groupby[key]:
                grouped[attr] = defaultdict(list)
                for obj in objects:
                    if obj.get(attr) is not None:
                        grouped[attr][obj[attr]].append(obj)
            self.caches[key] = grouped

    def get(self, key, label, multiple=True, mandatory=True, hasM=False):
        grouped = self.caches[key]
        matches = []
        for attr in self.groupby[key]:
            if attr == "id":
                try:
                    idno = int(label)
                except ValueError:
                    continue
                else:
                    matches.append(grouped[attr][idno])
            else:
                matches.append(grouped[attr][label])
        matches = [m for m in matches if m != []]
        allmatch = sum(matches, [])
        if matches:
            if multiple:
                return allmatch
            elif len(matches[0]) == 1:
                return matches[0][0]
            else:
                msg = '{0!r}: ambiguous; name used by multiple {1}s: {2}'\
                      .format(label, key, ', '.join(str(o.id)
                                                    for o in allmatch))
                if hasM:
                    msg += '\nUse the -M/--multiple option to specify' \
                           ' all of them at once.'
                die(msg)
        elif mandatory:
            die('{0!r}: no such {1}'.format(label, key))
        else:
            return [] if multiple else None

    def cache_sshkeys(self):
        self.cache(self.client.fetch_all_ssh_keys(), "sshkey")

    def get_sshkey(self, label, multiple=True, mandatory=True, hasM=False):
        self.cache_sshkeys()
        return self.get("sshkey", label, multiple, mandatory, hasM)

    def get_sshkeys(self, labels, multiple=True):
        if multiple:
            objs = [key for l in labels for key in self.get_sshkey(l, True)]
        else:
            objs = [self.get_sshkey(l, False, hasM=True) for l in labels]
        return rmdups(objs, 'SSH key')

    def add_sshkey(self, key):
        cache = self.caches["sshkey"]
        for attr in self.groupby["sshkey"]:
            value = key.get(attr)
            if value is not None:
                cache[attr][value].append(key)

    def cache_droplets(self):
        self.cache(self.client.fetch_all_droplets(), "droplet")

    def get_droplet(self, label, multiple=True, mandatory=True, hasM=False):
        self.cache_droplets()
        return self.get("droplet", label, multiple, mandatory, hasM)

    def get_droplets(self, labels, multiple=True):
        if multiple:
            objs = [drop for l in labels for drop in self.get_droplet(l, True)]
        else:
            objs = [self.get_droplet(l, False, hasM=True) for l in labels]
        return rmdups(objs, 'droplet')

    def cache_images(self):
        self.cache(self.client.fetch_all_images(), "image")

    def get_image(self, label, multiple=True, mandatory=True, hasM=False):
        self.cache_images()
        return self.get("image", label, multiple, mandatory, hasM)

    def get_images(self, labels, multiple=True):
        if multiple:
            objs = [img for l in labels for img in self.get_image(l, True)]
        else:
            objs = [self.get_image(l, False, hasM=True) for l in labels]
        return rmdups(objs, 'image')

    def check_name_dup(self, key, name, fatal):
        if key == "sshkey":
            self.cache_sshkeys()
        elif key == "droplet":
            self.cache_droplets()
        elif key == "image":
            self.cache_images()
        if name in self.caches[key]["name"] or \
                (key == "image" and name in self.caches[key]["slug"]):
            msg = 'There is already another {0} named {1!r}'.format(key, name)
            if fatal:
                die(msg)
            else:
                print('Warning:', msg, file=sys.stderr)


def mkclient(args):
    if args.api_token is not None:
        api_token = args.api_token
    elif args.api_token_file is not None:
        with args.api_token_file as fp:
            api_token = fp.read().strip()
    elif "DO_API_TOKEN" in os.environ:
        api_token = os.environ["DO_API_TOKEN"]
    else:
        try:
            with open(os.path.expanduser('~/.doapi')) as fp:
                api_token = fp.read().strip()
        except IOError:
            die('''\
No DigitalOcean API token supplied

Specify your API token via one of the following (in order of precedence):
 - the `--api-token TOKEN` or `--api-token-file FILE` option
 - the `DO_API_TOKEN` environment variable
 - a ~/.doapi file
''')
    client = doapi(api_token, **{param: getattr(args, param)
                                 for param in "timeout endpoint wait_interval"
                                              " wait_time".split()
                                 if getattr(args, param, None) is not None})
    return (client, Cache(client))

def dump(obj, fp=sys.stdout):
    if isinstance(obj, Iterator):
        fp.write('[')
        first = True
        for o in obj:
            if first:
                fp.write('\n')
                first = False
            else:
                fp.write(',\n')
            s = json.dumps(o, cls=DOEncoder, sort_keys=True, indent=4,
                           separators=(',', ': '))
            fp.write(re.sub(r'^', '    ', s, flags=re.M))
            fp.flush()
        if not first:
            fp.write('\n')
        fp.write(']\n')
    else:
        json.dump(obj, fp, cls=DOEncoder, sort_keys=True, indent=4,
                  separators=(',', ': '))
        fp.write('\n')

def die(msg):
    raise SystemExit(sys.argv[0] + ': ' + msg)

def currentActions(objs, withnulls=False):
    for o in objs:
        act = o.fetch_current_action()
        if act:
            yield act
        elif withnulls:
            yield None

def add_actioncmds(cmds, objtype, multiple=True, taggable=False):
    cmd_act = cmds.add_parser('act', parents=[waitopts],
                              help='Perform an arbitrary action',
                              description='Perform an arbitrary action')
    cmd_act.add_argument('-p', '--params', metavar='JSON|@file',
                         type=str_or_file,
                         help='JSON object of action arguments')
    if multiple:
        cmd_act.add_argument('-M', '--multiple', action='store_true',
                             help='Act on multiple resources with the same ID'
                                  ' or name')
    if taggable:
        cmd_act.add_argument('--tag',
                             help='Operate on all droplets with the given tag')
    cmd_act.add_argument('type', help='type of action to perform')
    cmd_act.add_argument(objtype, nargs='*' if taggable else '+',
                         help='identifier for a resource to act on')

    cmd_actions = cmds.add_parser('actions',
                                  help='List actions performed on resources',
                                  description='List actions performed on'
                                              ' resources')
    latestopts = cmd_actions.add_mutually_exclusive_group()
    latestopts.add_argument('--last', action='store_true',
                            help='Show only the most recent action on each'
                                 ' resource')
    latestopts.add_argument('--in-progress', action='store_true',
                            help='Show only in-progress actions')
    if multiple:
        cmd_actions.add_argument('-M', '--multiple', action='store_true',
                                 help='Act on multiple resources with the same'
                                      ' ID or name')
    cmd_actions.add_argument(objtype, nargs='+',
                             help='identifier for a resource to fetch data for')

    cmd_wait = cmds.add_parser('wait', parents=[waitbase],
                               help="Wait for resources' most recent actions"
                                    " to complete",
                               description="Wait for resources' most recent"
                                           " actions to complete")
    if objtype == 'droplet':
        dropopts = cmd_wait.add_mutually_exclusive_group()
        dropopts.add_argument('-S', '--status', type=str.lower,
                              choices=['active', 'new', 'off', 'archive'],
                              help="Wait for the droplets to reach the given"
                                   " status")
        dropopts.add_argument('--locked', action='store_true',
                              help='Wait for the droplets to become locked')
        dropopts.add_argument('--unlocked', action='store_true',
                              help='Wait for the droplets to become unlocked')
    if multiple:
        cmd_wait.add_argument('-M', '--multiple', action='store_true',
                              help='Act on multiple resources with the same ID'
                                   ' or name')
    cmd_wait.add_argument(objtype, nargs='+',
                          help='identifier for a resource to wait on')

def do_actioncmd(args, client, objects):
    if args.cmd == 'act':
        if args.params is not None:
            params = json.loads(args.params)
            if not isinstance(params, dict):
                die('--params must be a JSON dictionary/object')
        else:
            params = {}
        actions = [obj.act(type=args.type, **params) for obj in objects]
        if args.wait:
            actions = catch_timeout(client.wait_actions(actions))
        dump(actions)
    elif args.cmd == 'actions':
        if args.in_progress:
            dump(currentActions(objects, withnulls=True))
        elif args.last:
            dump(obj.fetch_last_action() for obj in objects)
        else:
            dump(obj.fetch_all_actions() for obj in objects)
    elif args.cmd == 'wait':
        if getattr(args, "status", None) is not None:
            waiter = client.wait_droplets(objects, status=args.status)
        elif getattr(args, "locked", None) is not None:
            waiter = client.wait_droplets(objects, locked=True)
        elif getattr(args, "unlocked", None) is not None:
            waiter = client.wait_droplets(objects, locked=False)
        else:
            actions = list(currentActions(objects))
            waiter = client.wait_actions(actions)
        dump(catch_timeout(waiter))
    else:
        assert False, 'do_actioncmd called with invalid command'

def str_or_file(arg):
    if arg.startswith("@") and len(arg) > 1:
        if arg[1:] == '-':
            return sys.stdin.read()
        else:
            with open(arg[1:]) as fp:
                return fp.read()
    else:
        return arg

def rmdups(objs, objtype, idfield='id'):
    ### TODO: Rethink whether this should return a list or a generator (Would I
    ### want a generator for any non-showing operation?)
    seen = set()
    uniq = []
    for o in objs:
        idval = o[idfield]
        if idval in seen:
            print('Warning: {0} {1!r} specified multiple times'\
                  .format(objtype, idval), file=sys.stderr)
            print('Warning: ignoring later occurrence', file=sys.stderr)
        else:
            seen.add(idval)
            uniq.append(o)
    return uniq

def catch_timeout(gen):
    try:
        for obj in gen:
            yield obj
    except WaitTimeoutError as e:
        for obj in e.in_progress:
            yield obj
