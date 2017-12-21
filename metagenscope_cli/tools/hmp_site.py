"""Upload hmp site results to the MetaGenScope web platform."""

import json

from metagenscope_cli.tools.utils import upload_command


@upload_command(tool_name='hmp_site')
def hmp_site(input_file):
    """Upload hmp site results to the MetaGenScope web platform."""
    data = json.loads(input_file.read())

    # Skip validation until we are sure what are actually expecting for this result...

    return data
