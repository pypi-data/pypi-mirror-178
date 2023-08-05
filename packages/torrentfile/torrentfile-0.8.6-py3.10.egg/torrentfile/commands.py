#! /usr/bin/python3
# -*- coding: utf-8 -*-

##############################################################################
#    Copyright (C) 2021-current alexpdev
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
##############################################################################
"""
The commands module contains the Action Commands executed by the CLI script.

Each function pertains to a command line action/subcommand and drives specific
features of the application.

Functions
---------
- create_command
- info_command
- edit_command
- recheck_command
- magnet_command
"""
import logging
import os
import shutil
import sys
from argparse import Namespace
from hashlib import sha1  # nosec
from urllib.parse import quote_plus

import pyben

from torrentfile.edit import edit_torrent
from torrentfile.interactive import select_action
from torrentfile.rebuild import Assembler
from torrentfile.recheck import Checker
from torrentfile.torrent import TorrentAssembler, TorrentFile
from torrentfile.utils import ArgumentError

logger = logging.getLogger(__name__)


def create(args: Namespace) -> Namespace:
    """
    Execute the create CLI sub-command to create a new torrent metafile.

    Parameters
    ----------
    args : Namespace
        positional and optional CLI arguments.

    Returns
    -------
    torrentfile.MetaFile
        object containing the path to created metafile and its contents.
    """
    kwargs = vars(args)
    logger.debug("Creating torrent from %s", args.content)
    if args.meta_version == "1":
        torrent = TorrentFile(**kwargs)
    else:
        torrent = TorrentAssembler(**kwargs)
    outfile, meta = torrent.write()

    if args.magnet:
        magnet(outfile)

    args.torrent = torrent
    args.kwargs = kwargs
    args.outfile = outfile
    args.meta = meta

    print("\nTorrent Save Path: ", os.path.abspath(str(outfile)))
    logger.debug("Output path: %s", str(outfile))
    return args


def info(args: Namespace) -> str:
    """
    Show torrent metafile details to user via stdout.

    Prints full details of torrent file contents to the terminal in
    a clean and readable format.

    Parameters
    ----------
    args : dict
        command line arguements provided by the user.

    Returns
    -------
    str
        The output printed to the terminal.
    """
    metafile = args.metafile
    meta = pyben.load(metafile)
    data = meta["info"]
    del meta["info"]

    meta.update(data)
    if "private" in meta and meta["private"] == 1:
        meta["private"] = "True"
    if "announce-list" in meta:
        lst = meta["announce-list"]
        meta["announce-list"] = ", ".join([j for i in lst for j in i])
    if "url-list" in meta:
        meta["url-list"] = ", ".join(meta["url-list"])
    if "httpseeds" in meta:
        meta["httpseeds"] = ", ".join(meta["httpseeds"])

    text = []
    longest = max(len(i) for i in meta.keys())

    for key, val in meta.items():
        if key not in ["pieces", "piece layers", "files", "file tree"]:
            prefix = longest - len(key) + 1
            string = key + (" " * prefix) + str(val)
            text.append(string)

    most = max(len(i) for i in text)
    text = ["-" * most, "\n"] + text + ["\n", "-" * most]
    output = "\n".join(text)
    print(output)
    return output


def edit(args: Namespace) -> str:
    """
    Execute the edit CLI sub-command with provided arguments.

    Provides functionality that can change the details of a torrentfile
    that preserves all of the hash piece information so as not to break
    the torrentfile.

    Parameters
    ----------
    args : Namespace
        positional and optional CLI arguments.

    Returns
    -------
    str
        path to edited torrent file.
    """
    metafile = args.metafile
    logger.info("Editing %s Meta File", str(args.metafile))
    editargs = {
        "url-list": args.url_list,
        "httpseeds": args.httpseeds,
        "announce": args.announce,
        "source": args.source,
        "private": args.private,
        "comment": args.comment,
    }
    return edit_torrent(metafile, editargs)


def recheck(args: Namespace) -> str:
    """
    Execute recheck CLI sub-command.

    Checks the piece hashes within a pre-existing torrent file
    and does a piece by piece check with the contents of a file
    or directory for completeness and validation.

    Parameters
    ----------
    args : Namespace
        positional and optional arguments.

    Returns
    -------
    str
        The percentage of content currently saved to disk.
    """
    metafile = args.metafile
    content = args.content

    if os.path.isdir(metafile):
        raise ArgumentError(
            f"Error: Unable to parse directory {metafile}. "
            "Check the order of the parameters."
        )

    logger.debug(
        "Validating %s <---------------> %s contents", metafile, content
    )

    msg = f"Rechecking  {metafile} ...\n"
    halfterm = shutil.get_terminal_size().columns / 2
    padding = int(halfterm - (len(msg) / 2)) * " "
    sys.stdout.write(padding + msg)

    checker = Checker(metafile, content)
    logger.debug("Completed initialization of the Checker class")
    result = checker.results()

    message = f"{content} <- {result}% -> {metafile}"
    padding = int(halfterm - (len(message) / 2)) * " "
    sys.stdout.write(padding + message + "\n")
    sys.stdout.flush()
    return result


def magnet(metafile: Namespace) -> str:
    """
    Create a magnet URI from a Bittorrent meta file.

    Parameters
    ----------
    metafile : Namespace
        Namespace class for CLI arguments.

    Returns
    -------
    str
        created magnet URI.
    """
    if hasattr(metafile, "metafile"):
        metafile = metafile.metafile
    if not os.path.exists(metafile):
        raise FileNotFoundError

    meta = pyben.load(metafile)
    data = meta["info"]
    binfo = pyben.dumps(data)
    infohash = sha1(binfo).hexdigest().upper()  # nosec

    logger.info("Magnet Info Hash: %s", infohash)
    scheme = "magnet:"
    hasharg = "?xt=urn:btih:" + infohash
    namearg = "&dn=" + quote_plus(data["name"])

    if "announce-list" in meta:
        announce_args = [
            "&tr=" + quote_plus(url)
            for urllist in meta["announce-list"]
            for url in urllist
        ]
    else:
        announce_args = ["&tr=" + quote_plus(meta["announce"])]

    full_uri = "".join([scheme, hasharg, namearg] + announce_args)
    logger.info("Created Magnet URI %s", full_uri)
    sys.stdout.write("\n" + full_uri + "\n")
    return full_uri


def rebuild(args: Namespace) -> int:
    """
    Attempt to rebuild a torrent based on the a torrent file.

    Recursively look through a directory for files that belong in
    a given torrent file, and rebuild as much of the torrent file
    as possible. Currently only checks if the filename and file
    size are a match.

    #### TODO
    1. Check file hashes to improve accuracy

    Parameters
    ----------
    args : Namespace
        command line arguments including the paths neccessary

    Returns
    -------
    int
        total number of content files copied to the rebuild directory
    """
    metafiles = args.metafiles
    dest = args.destination
    contents = args.contents
    for path in [*metafiles, *contents]:
        if not os.path.exists(path):
            raise FileNotFoundError(path)
    assembler = Assembler(metafiles, contents, dest)
    return assembler.assemble_torrents()


interactive = select_action  # for clean import system
