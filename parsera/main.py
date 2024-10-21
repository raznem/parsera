import argparse
import asyncio
import json
import os

import colorama
from colorama import Fore, Style
from dotenv import load_dotenv
from playwright.async_api import Page

from parsera import ParseraScript
from parsera.engine.model import GPT4oMiniModel


def validate_file(file_path):
    """Validate if the file exists and contains a valid JSON scheme."""
    # Check if the file exists
    if not os.path.isfile(file_path):
        raise argparse.ArgumentTypeError(f"The file {file_path} does not exist.")

    # Try to open and parse the file content as JSON
    try:
        with open(file_path, "r") as f:
            scheme = json.load(f)

            # Ensure the scheme is a dictionary
            if not isinstance(scheme, dict):
                raise argparse.ArgumentTypeError(
                    "The scheme in the file must be a valid JSON object (dict)."
                )

            return scheme
    except json.JSONDecodeError:
        raise argparse.ArgumentTypeError(f"Invalid JSON format in {file_path}.")


def validate_scheme(scheme_string):
    """Validate and parse the scheme dictionary (passed as a JSON string)."""
    try:
        return json.loads(scheme_string)
    except json.JSONDecodeError:
        raise argparse.ArgumentTypeError(
            "Invalid scheme format. Must be a valid JSON string."
        )


def validate_args(args):
    """Custom validation to ensure either scheme or file is provided."""
    if args.scheme is None and args.file is None:
        raise argparse.ArgumentError(
            None, "You must provide either --scheme or --file."
        )
    return args


def fancy_parser():
    parser = argparse.ArgumentParser(
        description=Fore.CYAN
        + "🎯 Welcome to the Parsera CLI!"
        + Style.RESET_ALL
        + "\n"
        + "This tool allows you to parse a website using a provided URL and either a scheme or a file.\n"
        + "Follow the options below to get started.",
        epilog=Fore.YELLOW
        + "Example usage:\n"
        + Style.RESET_ALL
        + '  python -m parsera.main https://example.com --scrolls 5 --scheme \'{"title":"h1"}\'\n '
        + "  python -m parsera.main https://example.com --scrolls 5 --file path/to/elements.json",
    )

    # URL argument
    parser.add_argument(
        "url",
        type=str,
        help=Fore.GREEN + "The URL of the website to parse." + Style.RESET_ALL,
    )

    # Scheme argument (parsed as a dictionary)
    parser.add_argument(
        "--scheme",
        type=validate_scheme,
        help=Fore.GREEN
        + 'Provide a JSON string as the scheme definition (e.g., \'{"key": "value"}\').'
        + Style.RESET_ALL,
        required=False,
    )

    # Scrolls argument
    parser.add_argument(
        "--scrolls",
        type=int,
        help=Fore.GREEN
        + "Add amount of scrolls for the page on the url."
        + Style.RESET_ALL,
        required=False,
        default=0
    )

    # File argument (with validation for file)
    parser.add_argument(
        "--file",
        type=validate_file,
        help=Fore.GREEN
        + "Path to the file with parsing elements (used if --scheme is not provided)."
        + Style.RESET_ALL,
        required=False,
    )

    # Output file argument
    parser.add_argument(
        "--output",
        type=str,
        help="Path to output the parsed results as a JSON file.",
        required=False,
        default="output.json",
    )

    return parser.parse_args()


async def get_url_data(url, scheme, scrolls):
    model = GPT4oMiniModel()

    # This script is executed after the url is opened
    async def repeating_script(page: Page) -> Page:
        await page.wait_for_timeout(1000)  # Wait one second for page to load
        return page

    parsera = ParseraScript(model=model)
    return await parsera.arun(
        url=url, elements=scheme, playwright_script=repeating_script, scrolls_limit=scrolls
    )


if __name__ == "__main__":
    # To load API_KEY from environment
    load_dotenv()

    colorama.init(autoreset=True)
    # Parse arguments
    args = fancy_parser()

    # Validate that either scheme or file is provided
    args = validate_args(args)

    # Now you can proceed with the rest of the script
    print(Fore.CYAN + "Parsing the website:" + Style.RESET_ALL, args.url)

    if args.scheme:
        print(
            Fore.CYAN + "Scheme (from command-line argument):" + Style.RESET_ALL,
            args.scheme,
        )
    if args.file:
        print(Fore.CYAN + "Scheme (from file):" + Style.RESET_ALL, args.file)
    if args.scrolls:
        print(Fore.CYAN + "Amount of scrolls on the page:" + Style.RESET_ALL, args.scrolls)

    # Determine the scheme to use (from scheme argument or file)
    scheme = args.scheme if args.scheme else args.file

    result = asyncio.run(get_url_data(args.url, scheme, args.scrolls))

    # Print the result to the console
    print(Fore.GREEN + "Parsed result:" + Style.RESET_ALL, result)

    # Write the result to a JSON file
    output_file = args.output
    with open(output_file, "w") as f:
        json.dump(result, f, indent=4)
        print(
            Fore.YELLOW
            + f"Result successfully written to {output_file}"
            + Style.RESET_ALL
        )
