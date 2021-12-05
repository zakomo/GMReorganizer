#!/bin/env python3

import csv
import os
import sys
import eyed3
import shutil

import utils


def create_directory_tree(folder_tree: dict, base_folder: str) -> dict:
    """
    Creates the directory structure specified in folder_tree into base_folder
    if dry_run is set to True prints the passages but don't create the
    structure itself

    Parameter:
    folder_tree: dict -> the directory structure to be created in the form
                {Artist: [Album, Album], Artist: [Album]}
    base_folder: str -> the parent folder to the directory.
    """

    for artist in folder_tree:
        os.chdir(base_folder)
        if not os.path.isdir(artist):
            print(f"creating {artist} folder")
            os.mkdir(artist.encode('UTF-8'), 0o0775)
        print(f"changing directory to {artist}")
        os.chdir(artist)
        for album in folder_tree[artist]:
            if not album == '':
                print(f"creating {album} folder for {artist}")
                os.mkdir(album.encode('UTF-8'), 0o0775)


def calculate_directory_structure(file_list, directory,  kind="csv"):

    """
    Create a folder structure based on the files in file_list
    Folder structure is a dictionary with Artist: [Album, Album, ..]

    Parameter:
    file_list: list -> List with the files that contain the information
    directory: str -> directory in which the files reside
    kind: str -> either csv or mp3 (source for the Artist name and Album name)

    Return:

    structure: dict -> The structure of the tree in a dictionary:
                {Artist: [Album, Album, ...], Artist:[Album, ...]}
    """
    structure = {}
    os.chdir(directory)

    for f in file_list:
        print(f)
        artist = ""
        album = ""
        if kind == "csv":
            with open(f, newline="") as csv_f:
                reader = csv.DictReader(csv_f)
                for row in reader:
                    artist = row["Artist"]
                    album = row["Album"]
        elif kind == "mp3":
            song = eyed3.load(f)
            artist = song.tag.artist
            album = song.tag.album

        if artist and album:
            artist = utils.sanitize_name(artist)
            album = utils.sanitize_name(album)

            # add artist and album to the structure
            if artist in structure:
                if album not in structure[artist]:
                    structure[artist].append(album)
            else:
                structure[artist] = [album]
        print(artist, album, sep=" - ")
    return structure


def reorganize(mp3_files, origin, destination, structure, move=False):
    """
    Reorganizes the files in mp3_files from origin into destination
    returns a list with the files that couldn't be copied or moved
    on the new list

    Parameter :
    mp3_files: list -> list of the mp3 files to be moved
    origin: str -> folder where the files are stored
    destination: str -> folder where the directory for the files is
    move: bool -> Move the files when true, copy otherwise. Default False

    """
    not_moved = []
    os.chdir(origin)

    for song in mp3_files:
        af = eyed3.load(song)
        artist = af.tag.artist
        album = af.tag.album

        if artist:
            artist.replace("/", "-")
        if album:
            album.replace("/", "-")
        if artist in structure:
            if album in structure[artist]:
                final = os.sep.join([destination, artist, album])
                print(song, final, sep="->")
                if move:
                    shutil.move(song, final)
                elif not move:
                    shutil.copy(song, final)
            else:
                not_moved.append(song)
        else:
            not_moved.append(song)
    return not_moved


def main():
    args = utils.create_cli_parser()

    if not os.path.isdir(args.folder):
        return "The origin folder is not a folder or does not exist"
    else:
        origin = os.path.abspath(args.folder)

    if not os.path.isdir(args.destination):
        return "The destination folder is not a folder or does not exist"
    else:
        destination = os.path.abspath(args.destination)

    dry_run = True if args.dry_run else False
    move = True if args.move else False

    # adapt this to work for sogns in more levels, not only flat directories
    all_files = os.listdir(origin)
    mp3_files = [f for f in all_files if f[-3:] == "mp3"]
    if args.google_music:
        csv_files = [f for f in all_files if f[-3:] == "csv"]
        structure = calculate_directory_structure(csv_files,
                                                  origin,
                                                  kind="csv")
    else:
        structure = calculate_directory_structure(mp3_files,
                                                  origin, 
                                                  kind="mp3")

    if not dry_run:
        create_directory_tree(structure, destination)
        # TODO: reorganize should recreate the structure from the created
        # folders and only in case of dry_run use the structure returned form
        # calculate_directory_structure
        failed = reorganize(mp3_files,
                            origin,
                            destination,
                            structure,
                            move=move)
    else:
        print(structure)

    print(failed)


if __name__ == "__main__":
    sys.exit(main())
