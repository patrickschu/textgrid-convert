import logging
log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())

from textgrid_convert.ttextgrid_convert import main
from textgrid_convert.ArgParser import  arg_parser

current_args = arg_parser.parse_args()
log.debug("Current args %s " %current_args)
main(**vars(current_args))
