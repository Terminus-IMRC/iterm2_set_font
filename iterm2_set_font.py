#!/usr/bin/env python3


# See https://www.iterm2.com/python-api/ for iTerm2 Python API.


import argparse
import iterm2


parser = argparse.ArgumentParser(description = 'iTerm2 font settings')
parser.add_argument('-q', '--quiet', help = 'be quiet', action = 'store_true')
parser.add_argument('-f', '--font', help = 'font name')
parser.add_argument('-s', '--size', help = 'font size', type = int)
args = parser.parse_args()


async def main(connection):

    app = await iterm2.async_get_app(connection)

    session = app.current_terminal_window.current_tab.current_session

    async def get_current_font():
        profile = await session.async_get_profile()
        font, size = profile.normal_font.rsplit(maxsplit = 1)
        size = int(size)
        return font, size

    async def set_font(font, size):
        profile = iterm2.LocalWriteOnlyProfile()
        profile.set_normal_font(f'{font} {size}')
        await session.async_set_profile_properties(profile)

    font, size = await get_current_font()
    if not args.quiet:
        print(f'Current font and size: \'{font}\' {size}')

    if args.font is not None:
        font = args.font
    if args.size is not None:
        size = args.size

    await set_font(font, size)
    if not args.quiet:
        print(f'New font and size: \'{font}\' {size}')


iterm2.run_until_complete(main)
