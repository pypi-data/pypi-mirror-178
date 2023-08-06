import shlex
import subprocess
from pathlib import PurePath

try:
    import gallery_dl
except ImportError:
    raise ImportError(
        "gallery-dl is not installed, it is required to use this package."
    )


def gallery_dl_wrap(
    url: str = None,
    input_file: str | PurePath = None,
    destination: str | PurePath = ".",
    directory: str | PurePath = None,
    cookies_file: str | PurePath = None,
    cookies_browser: str | PurePath = None,
    quiet: bool = False,
    verbose: bool = False,
    print_urls: bool = False,
    print_resolved_urls: bool = False,
    print_json: bool = False,
    simulate: bool = False,
    extractor_info: bool = False,
    list_keywords: bool = False,
    list_modules: bool = False,
    list_extractors: bool = False,
    retries: int = 4,
    filesize_min: str = None,
    filesize_max: str = None,
    no_part: bool = False,
    no_skip: bool = False,
    no_mtime: bool = False,
    no_download: bool = False,
    no_postprocessors: bool = False,
    no_check_certificate: bool = False,
    config_file: str | PurePath = None,
    username: str = None,
    password: str = None,
    download_archive: str | PurePath = None,
    download_range: str = None,
    download_filter: str = None,
    download_zip: bool = False,
    ugoria_conv: bool = False,
    ugoria_conv_lossless: bool = False,
    ugoria_conv_copy: bool = False,
    write_metadata: bool = False,
    write_info_json: bool = False,
    write_tags: bool = False,
    exec_str: str = None,
    exec_after: str = None,
    postprocesser: str = None,
) -> str:
    """_args_

    'url' (str, optional) : Defaults to None.
        URL to download/scrape.

    'input_file' (str | PurePath, optional) : Defaults to None.
        File with URLs to download/scrape.

    'destination' (str | PurePath, optional) : Defaults to ".".
        Destination folder.

    'directory' (str | PurePath, optional) : Defaults to None.
        Exact location.

    'cookies_file' (str | PurePath, optional) : Defaults to None.
        File with cookies information to use when scraping.

    'cookies_browser' (str | PurePath, optional) : Defaults to None.
        Browser to get cookies from.

    'quiet' (bool, optional) : Defaults to False.
        Download/scrape without showing output.

    'verbose' (bool, optional) : Defaults to False.
        Show more detailed output.

    'print_urls' (bool, optional) : Defaults to False.
        Print the URLs scraped.

    'print_resolved_urls' (bool, optional) : Defaults to False.
        Print the URLs after resolving them.

    'print_json' (bool, optional) : Defaults to False.
        Print JSON information.

    'simulate' (bool, optional) : Defaults to False.
        Simulate run, do not download.

    'extractor_info' (bool, optional) : Defaults to False.
        Print extractor defaults and settings.

    'list_keywords' (bool, optional) : Defaults to False.
        Print a list of keywords and example values for the given URLs.

    'list_modules' (bool, optional) : Defaults to False.
        Print modules.

    'list_extractors' (bool, optional) : Defaults to False.
        Print extractors.

    'retries' (int, optional) : Defaults to 4.
        Maximum number of retries for failed HTTP requests.

    'filesize_min' (str, optional) : Defaults to None.
        Do not download files smaller than SIZE (e.g. 500k or 2.5M).

    'filesize_max' (str, optional) : Defaults to None.
        Do not download files larger than SIZE (e.g. 500k or 2.5M).

    'no_part' (bool, optional) : Defaults to False.
        Do not use .part files.

    'no_skip' (bool, optional) : Defaults to False.
        Do not skip downloads; overwrite existing files.

    'no_mtime' (bool, optional) : Defaults to False.
        Do not set file modification times according to Last-Modified HTTP response headers.

    'no_download' (bool, optional) : Defaults to False.
        Do not download any files.

    'no_postprocessors' (bool, optional) : Defaults to False.
        Do not run any post processors.

    'no_check_certificate' (bool, optional) : Defaults to False.
        Disable HTTPS certificate validation.

    'config_file' (str | PurePath, optional) : Defaults to None.
        Additional configuration files.

    'username' (str, optional) : Defaults to None.
        Username to login with.

    'password' (str, optional) : Defaults to None.
        Password belonging to the given username.

    'download_archive' (str | PurePath, optional) : Defaults to None.
        Record all downloaded files in the archive file and skip downloading any file already in it.

    'download_range' (str, optional) : Defaults to None.
        Index-range(s) specifying which images to download. For example '5-10' or '1,3-5,10-'.

    'download_filter' (str, optional) : Defaults to None.
        Python expression controlling which images to download. Files for which the expression evaluates to False are ignored. Available keys are the filename-specific ones listed by '-K'. Example: --filter "image_width >= 1000 and rating in ('s', 'q')".

    'download_zip' (bool, optional) : Defaults to False.
        Store downloaded files in a ZIP archive.

    'ugoria_conv' (bool, optional) : Defaults to False.
        Convert Pixiv Ugoira to WebM (requires FFmpeg.

    'ugoria_conv_lossless' (bool, optional) : Defaults to False.
        Convert Pixiv Ugoira to WebM in VP9 lossless mode.

    'ugoria_conv_copy' (bool, optional) : Defaults to False.
        Convert Pixiv Ugoira to MKV without re-encoding any frames.

    'write_metadata' (bool, optional) : Defaults to False.
        Write metadata to separate JSON file.

    'write_info_json' (bool, optional) : Defaults to False.
        Write gallery metadata to a info.json file.

    'write_tags' (bool, optional) : Defaults to False.
        Write image tags to separate text files.

    'exec_str' (str, optional) : Defaults to None.
        Execute CMD for each downloaded file. Example: --exec 'convert {} {}.png && rm {}'.

    'exec_after' (str, optional) : Defaults to None.
        Execute CMD after all files were downloaded successfully. Example: --exec-after 'cd {} && convert * ../doc.pdf'.

    'postprocesser' (str, optional) : Defaults to None.
        Activate the specified post processor.
    """

    arg_list = ["gallery-dl"]

    if url:
        arg_list.append(shlex.quote(url))
    if input_file:
        arg_list += ["--input-file", input_file]
    if destination:
        arg_list += ["--destination", destination]
    if directory:
        arg_list += ["--directory", directory]
    if cookies_file:
        arg_list += ["--cookies", cookies_file]
    if cookies_browser:
        arg_list += ["--cookies-from-browser", cookies_browser]
    if quiet:
        arg_list.append("--quiet")
    if verbose:
        arg_list.append("--verbose")
    if print_urls:
        arg_list.append("--get-urls")
    if print_resolved_urls:
        arg_list.append("--resolve-urls")
    if print_json:
        arg_list.append("--dump-json")
    if simulate:
        arg_list.append("--simulate")
    if extractor_info:
        arg_list.append("--extractor_info")
    if list_keywords:
        arg_list.append("--list-keywords")
    if list_modules:
        arg_list.append("--list-modules")
    if list_extractors:
        arg_list.append("--list-extractors")
    if retries:
        arg_list += ["--retries", str(retries)]
    if filesize_min:
        arg_list += ["--filesize-min", filesize_min]
    if filesize_max:
        arg_list += ["--filesize-max", filesize_max]
    if no_part:
        arg_list.append("--no-part")
    if no_skip:
        arg_list.append("--no-skip")
    if no_mtime:
        arg_list.append("--no-mtime")
    if no_download:
        arg_list.append("--no-download")
    if no_postprocessors:
        arg_list.append("--no-postprocesser")
    if no_check_certificate:
        arg_list.append("--no-check-certificate")
    if config_file:
        arg_list += ["--config", config_file]
    if username:
        arg_list += ["--username", username]
    if password:
        arg_list += ["--password", password]
    if download_archive:
        arg_list += ["--download-archive", download_archive]
    if download_range:
        arg_list += ["--range", download_range]
    if download_filter:
        arg_list += ["--filter", download_filter]
    if download_zip:
        arg_list.append("--zip")
    if ugoria_conv:
        arg_list.append("--ugoria-conv")
    if ugoria_conv_lossless:
        arg_list.append("--ugoria-conv-lossless")
    if ugoria_conv_copy:
        arg_list.append("--ugoria-conv-copy")
    if write_metadata:
        arg_list.append("--write_metadata")
    if write_info_json:
        arg_list.append("--write-info-json")
    if write_tags:
        arg_list.append("--write-tags")
    if exec_str:
        arg_list += ["--exec", exec_str]
    if exec_after:
        arg_list += ["--exec-after", exec_after]
    if postprocesser:
        arg_list += ["--postprocesser", postprocesser]

    command = shlex.join(arg_list)
    # command = " ".join(arg_list)

    # completed_process = subprocess.run(command, shell=True)
    # completed_process.check_returncode()

    stdout = ""

    with subprocess.Popen(
        command, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True
    ) as p:
        for line in p.stdout:
            stdout += line
            if not quiet:
                print(line, end="")

    if p.returncode != 0:
        raise subprocess.CalledProcessError(p.returncode, p.args)
    else:
        return stdout


if __name__ == "__main__":
    # gallery_dl_wrap(
    #     url="https://boards.4chan.org/hr/thread/4519156",
    #     print_resolved_urls=True,
    #     no_download=True,
    # )
    # value = gallery_dl_wrap(
    #     url="https://cyberdrop.me/a/UyGwetQ7",
    #     print_resolved_urls=True,
    #     no_download=True,
    #     quiet=True,
    # )
    # print(len(value))
    # print(len([x[2:] for x in value.split("\n") if x.startswith("|")]))
    pass
