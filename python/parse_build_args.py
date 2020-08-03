
"""Adding this only for displaying command line option
"""

# `parser` var will be given by custom build system
parser.add_argument("--python",
                    required=True,
                    type=str,
                    help="Set Python version to build.")
