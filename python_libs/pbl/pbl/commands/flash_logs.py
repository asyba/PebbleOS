from __future__ import absolute_import, print_function

from libpebble2.services.getbytes import GetBytesService
from libpebble2.exceptions import GetBytesError
from libpebble2.protocol.transfers import GetBytesInfoResponse

from pebble_tool.commands.base import PebbleCommand
from pebble_tool.exceptions import ToolError

import os

class FlashLogsCommand(PebbleCommand):
    """Dump flash logs (PBL_LOG) from the watch."""
    command = 'flash_logs'

    def __call__(self, args):
        super(FlashLogsCommand, self).__call__(args)
        get_bytes = GetBytesService(self.pebble)

        # Flash log region: FLASH_REGION_DEBUG_DB_BEGIN to FLASH_REGION_DEBUG_DB_END
        # Platform-specific addresses (from src/fw/flash_region/flash_region_*.h):
        # - ASTERIX (gd25lq255e): 0x1FD0000 to 0x1FF0000 (128KB) - see flash_region_gd25lq255e.h:28,49-50
        # - TINTIN (n25q): 0x3e0000 to 0x400000 (128KB) - see flash_region_n25q.h:62-63
        # - SNOWY/SPALDING (s29vs): 0x0 to 0x20000 (128KB) - see flash_region_s29vs.h:24-25
        # - SILK (mx25u): Calculated dynamically - see flash_region_mx25u.h
        # - CALCULUS/ROBERT (mt25q): Calculated dynamically
        # - OBELIX (gd25q256e): Calculated dynamically
        #
        # For ASTERIX, use 0x1FD0000 (from flash_region_gd25lq255e.h line 28 comment)
        FLASH_LOG_START = 0x1FD0000  # ASTERIX address (from flash_region_gd25lq255e.h)
        FLASH_LOG_SIZE = 0x20000  # 128KB

        print("Reading flash log region: 0x{:X} - 0x{:X} ({} KB)".format(
            FLASH_LOG_START, FLASH_LOG_START + FLASH_LOG_SIZE, FLASH_LOG_SIZE // 1024))
        
        try:
            flash_data = get_bytes.get_flash_region(FLASH_LOG_START, FLASH_LOG_SIZE)
            print("Read {} bytes from flash".format(len(flash_data)))
            
            # Save to file
            import datetime
            filename = datetime.datetime.now().strftime("flash_logs_%Y-%m-%d_%H-%M-%S.bin")
            filepath = os.path.abspath(filename)
            with open(filename, "wb") as log_file:
                log_file.write(flash_data)
            print("Saved flash logs to {}".format(filepath))
            
            print("\nTo parse and dehash the logs:")
            print("  tools/dehash_flash_logs.py {}".format(filename))
            
        except GetBytesError as ex:
            if ex.code == GetBytesInfoResponse.ErrorCode.DoesNotExist:
                raise ToolError('Could not read flash region. This may require non-release firmware.')
            else:
                raise

    @classmethod
    def add_parser(cls, parser):
        parser = super(FlashLogsCommand, cls).add_parser(parser)
        return parser

