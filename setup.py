#!/usr/bin/env python3

import argparse
import subprocess

if __name__ == '__main__':
    parser = argparse.ArgumentParser('setup')
    parser.add_argument('--full', help='Install plugins', action='store_true')
    args = parser.parse_args()

    command_chain = ['pip', 'install', 'graph_visualizer_api', 'graph_visualizer_platform', 'graph_visualizer_core']
    if args.full:
        command_chain.extend(['simple_visualizer_plugin', 'block_visualizer_plugin', 'html_data_source_plugin',
                              'json_data_source_plugin'])

    subprocess.call(command_chain)
