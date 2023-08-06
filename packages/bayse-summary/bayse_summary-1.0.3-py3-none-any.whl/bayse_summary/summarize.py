"""
    Copyright 2022 Bayse, Inc. (maintained by david@bayse.io)
    For license information, please see the accompanying LICENSE file in the top-level directory of this repository.
"""
import ipaddress
import json
import magic
import os
import pathlib
import re
import requests
import time
import validators

BAYSEFLOWS_IDENTIFIER = "BayseFlows"
EXPECTED_FILETYPE_REGEX = r"^JSON (text |)data"
DEFAULT_TIME = float(99999999999)
PUBLIC_SOURCES = "public_sources"
PUBLIC_DESTINATIONS = "public_destinations"
UPLOAD_ENDPOINT = "https://api.bayse.io/stats"
API_KEY_DEFAULT_ENVIRONMENT_VARIABLE = "BAYSE_API_KEY"
MAX_FILE_SIZE_KB = 200  # a bit less than a backend limit, to avoid missing data


def collect_data_from_bayseflow_files(filepaths, verbose):
    """Takes a list of filepaths and iterates through all valid files to collect the fields we care about for follow-on
       summarization steps.
    """
    relevant_bayseflow_data = []
    collected_bayseflow_fields = ["src", "dst", "relativeStart", "duration", "protocolInformation", "label"]
    for p in filepaths:
        path = pathlib.PurePath(p)
        valid_filetype = re.match(EXPECTED_FILETYPE_REGEX, magic.from_file(path))
        data = None
        if not valid_filetype:  # re.match(EXPECTED_FILETYPE_REGEX, magic.from_file(path)):
            if verbose:
                print(f"{path} is not a JSON file. Trying to load anyway.")
            try:
                with open(path, "r") as bfdata:
                    data = json.load(bfdata)
                    valid_filetype = True
            except:
                if verbose:
                    print(f"Failed to load {path}. Skipping.")
                continue
        if valid_filetype:
            with open(path, "r") as bfdata:
                if not data:
                    data = json.load(bfdata)
                try:
                    first_bayseflow = data[BAYSEFLOWS_IDENTIFIER][0]
                    file_start_time = data["trafficDate"]
                except:
                    if verbose:
                        print(f"JSON data at {path} missing {BAYSEFLOWS_IDENTIFIER}. Skipping.")
                    continue
                for bayseflow_field in collected_bayseflow_fields:
                    if bayseflow_field not in first_bayseflow:
                        if verbose:
                            print(f"JSON data at {path} missing required fields. Skipping.")
                        continue
                # otherwise we should collect the data we need to do summarization
                try:
                    relevant_bayseflow_data.append({"file_start_time": file_start_time,
                                                    BAYSEFLOWS_IDENTIFIER: [
                                                        {field: flow[field] for field in collected_bayseflow_fields} for
                                                        flow in data[BAYSEFLOWS_IDENTIFIER]
                                                    ]
                                                    })
                except:
                    if verbose:
                        print(f"One or more BayseFlows in {path} is missing a field required for summarization. "
                              f"Skipping.")
                    continue
    return relevant_bayseflow_data


def collect_bayseflow_data_by_direction(summarized_data, absolute_start, bayseflow, name_or_ip, port, direction,
                                        verbose):
    """now that we have all of the data we really need, go through all of the collected data and summarize how many
       times we've seen each flow that is North-South or South-North. Ignore the others.
    """
    if "label" not in bayseflow:
        bayseflow["label"] = "placeholder"
    if name_or_ip not in summarized_data[direction]:
        summarized_data[direction][name_or_ip] = dict()
    protocol_dict = summarized_data[direction][name_or_ip]
    proto_key = f"{bayseflow['protocolInformation'].upper()}/{port}"
    if proto_key not in protocol_dict:
        protocol_dict[proto_key] = dict()
    label = bayseflow["label"]
    if label not in protocol_dict[proto_key]:
        protocol_dict[proto_key][label] = {"count": 0,
                                           "first_observed": DEFAULT_TIME,
                                           "last_observed": -1
                                           }
    label_details = protocol_dict[proto_key][label]
    # we should now have every level of the dictionary, so populate it
    label_details["count"] += 1
    flowstart = absolute_start + float(bayseflow["relativeStart"])
    flowend = flowstart + float(bayseflow["duration"])
    label_details["first_observed"] = min(label_details["first_observed"], flowstart)
    label_details["last_observed"] = max(label_details["last_observed"], flowend)
    return len(protocol_dict) / 1024  # rough calculation of KB size of entry


def summarize_bayseflow_files(filepaths, verbose=False):
    """Takes a list of one or more filepaths to BayseFlow (.bf) files and summarizes all of the non E-W content as
       follows:
       {
            "public_sources": { <name_or_IP>:
                                    { <protocol/port>:
                                        { <BayseFlow_label> :
                                            { "count": x,
                                              "first_observed": <min_timestamp_as_epoch>,
                                              "last_observed": <max_timestamp_as_epoch>
                                            }
                                        }
                                    }
                               },
            "public_destinations": { <name_or_IP>:
                                        { <protocol/port>:
                                            { <BayseFlow_label> :
                                                { "count": x,
                                                  "first_observed": <min_timestamp_as_epoch>,
                                                  "last_observed": <max_timestamp_as_epoch>
                                                }
                                            }
                                        }
                                    }
       }

       This data is saved to a timestamped summary.json file, whose filepath is returned to the caller.
    """
    relevant_bayseflow_data = collect_data_from_bayseflow_files(filepaths, verbose)
    summarized_data = {PUBLIC_SOURCES: dict(),
                       PUBLIC_DESTINATIONS: dict()
    }
    """Now that we have all of the data we really need, go through all of the collected data and summarize how many 
       times we've seen each flow that is North-South or South-North. Ignore the others.
    """
    data_size_kb = 0
    saved_files = []
    file_count = 1
    for contents in relevant_bayseflow_data:
        absolute_start = float(contents["file_start_time"])
        if absolute_start == DEFAULT_TIME:
            if verbose:
                print(f"Invalid start time for file. Skipping.")
            continue
        for bayseflow in contents[BAYSEFLOWS_IDENTIFIER]:
            global_source = False
            global_destination = False
            split_data_src = bayseflow["src"].split(":")
            split_data_dst = bayseflow["dst"].split(":")
            # ICMP isn't conveyed in the src/dst fields, so handle appropriately
            if bayseflow["protocolInformation"].upper() == "ICMP":
                source = ":".join(split_data_src)
                source_port = bayseflow["protocolInformation"].upper()
                destination = ":".join(split_data_dst)
                destination_port = bayseflow["protocolInformation"].upper()
            else:
                source = ":".join(split_data_src[:-1])
                source_port = "".join(split_data_src[-1])
                destination = ":".join(split_data_dst[:-1])
                destination_port = "".join(split_data_dst[-1])
            # get an appropriately-typed source or destination, as well as identify if it's local or global
            try:
                source = ipaddress.ip_address(source)
            except:
                if validators.domain(source):
                    global_source = True  # set this by default when it's a domain for now
                else:
                    if verbose:
                        print(f"{bayseflow['src']} not recognized as a valid IP address or domain. Skipping this"
                              f"{BAYSEFLOWS_IDENTIFIER}.")
                    continue
            # domains are more common for destinations, so try first.
            if validators.domain(destination):
                global_destination = True  # set by default when it's a domain for now
            else:
                try:
                    destination = ipaddress.ip_address(destination)
                except:
                    if verbose:
                        print(f"{bayseflow['dst']} not recognized as a valid IP address or domain. Skipping this"
                              f"{BAYSEFLOWS_IDENTIFIER}.")
                    continue
            if type(source) in [ipaddress.IPv4Address, ipaddress.IPv6Address]:
                global_source = source.is_global and not source.is_multicast
            if type(destination) in [ipaddress.IPv4Address, ipaddress.IPv6Address]:
                global_destination = destination.is_global and not destination.is_multicast
            # make sure at least one of the sources or destinations is NOT local
            if global_source or global_destination:
                # now make sure that both sides are NOT global IPs...if they are, maybe we're getting customer traffic
                if (global_source and global_destination
                    and type(source) in [ipaddress.IPv4Address, ipaddress.IPv6Address]
                    and type(destination) in [ipaddress.IPv4Address, ipaddress.IPv6Address]
                   ):
                    # Note: using DEFAULT subnet masks for IPv4 (/24) and IPv6 (/64) here since we have no NW info...
                    if type(source) == ipaddress.IPv4Address:  # assume source and dest are same IPvX types
                        if ipaddress.ip_network(f"{source}/24",
                                                strict=False).overlaps(ipaddress.ip_network(f"{destination}/24",
                                                                                            strict=False)
                                                                       ):
                            if verbose:
                                print(f"Not adding BayseFlow {bayseflow.items()} to summary because it may be "
                                      f"customer-owned public IPs talking to each other.")  # maybe push into logging?
                            continue
                    else:  # should be IPv6 if it's not IPv4...
                        if ipaddress.ip_network(f"{source}/64",
                                                strict=False).overlaps(ipaddress.ip_network(f"{destination}/64",
                                                                                            strict=False)
                                                                       ):
                            if verbose:
                                print(f"Not adding BayseFlow {bayseflow.items()} to summary because it may be "
                                      f"customer-owned public IPs talking to each other.")  # maybe push into logging?
                            continue
                # anything global that is still processing at this point should be captured for summarization.
                if global_source:
                    data_size_kb += collect_bayseflow_data_by_direction(summarized_data, absolute_start, bayseflow,
                                                                        str(source), source_port, PUBLIC_SOURCES,
                                                                        verbose)
                if global_destination:
                    data_size_kb += collect_bayseflow_data_by_direction(summarized_data, absolute_start, bayseflow,
                                                                        str(destination), destination_port,
                                                                        PUBLIC_DESTINATIONS, verbose)
                if data_size_kb > MAX_FILE_SIZE_KB:
                    saved_files += [save_stats_file(summarized_data, file_count, verbose)]  # save current file now
                    data_size_kb = 0  # reset KB count
                    summarized_data = {PUBLIC_SOURCES: dict(),
                                       PUBLIC_DESTINATIONS: dict()
                                       }  # reset these too
                    file_count += 1
            # we implicitly ignore summarizing E-W data
    saved_files += [save_stats_file(summarized_data, file_count, verbose)]
    return saved_files


def save_stats_file(summarized_data, file_count, verbose=False):
    """Temporarily saves a stats file. Returns the location of the file. File_count var helps to make sure we can
       capture when we actually need to save multiple to fit within backend limitations.
    """
    summarized_data_location = pathlib.PurePath(f"{str(time.time()).split('.')[0]}_{file_count}_summary.json")  # ts
    with open(summarized_data_location, "w") as out:
        json.dump(summarized_data, out)
        if verbose:
            print(f"Final summarized data stored at {summarized_data_location}")
    return summarized_data_location


def upload_stats(summarized_data_locations, api_key=None, api_key_environment_variable=None):
    """Send the stats data to the server for a given user. Expects API key (i.e. the user's identifier) to be either
       passed in, to have the name of an environment variable, or to be in the default environment value location. If
       none of these exist, upload fails. Otherwise success is dependent on whether the data is accepted server-side.
    """
    upload_info = {"status": "Failed", "errors": "", "text": ""}
    locations = []
    for data_loc in summarized_data_locations:
        locations += [pathlib.PurePath(data_loc)]
    summary_data = None
    if api_key is None and api_key_environment_variable is None:
        api_key = os.environ.get(API_KEY_DEFAULT_ENVIRONMENT_VARIABLE)
        if api_key is None:
            upload_info["errors"] += f"No API key passed in nor found at environment variable" \
                                     f" {API_KEY_DEFAULT_ENVIRONMENT_VARIABLE}.\n"
    elif api_key_environment_variable is not None:
        api_key = os.environ.get(api_key_environment_variable)
        if api_key is None:
            upload_info["errors"] += f"No API key found at supplied environment variable" \
                                     f" {api_key_environment_variable}.\n"
    if api_key is None:
        upload_info["errors"] += f"No API key found.\n"
        for location in locations:
            pathlib.Path(location).unlink(missing_ok=True)
        return upload_info  # short-circuit here

    s = requests.Session()
    for location in locations:
        if not re.match(EXPECTED_FILETYPE_REGEX, magic.from_file(location)):
            try:  # Some OSes fail to capture JSON as JSON, so try to load data. Server-side validates data passed to it
                with open(location, "r") as summary_datafile:
                    summary_data = json.load(summary_datafile)
            except Exception as e:
                upload_info["errors"] += f"{location} is not a JSON file.\n"
                continue
        else:
            try:
                with open(location, "r") as summary_datafile:
                    summary_data = json.load(summary_datafile)
            except Exception as e:
                upload_info["errors"] += f"{e}\n"
                continue
        if not summary_data:
            upload_info["errors"] += f"No data found when trying to open and load {location}.\n"
            continue
        elif PUBLIC_SOURCES not in summary_data or PUBLIC_DESTINATIONS not in summary_data:
            upload_info["errors"] += f"{PUBLIC_SOURCES} and/or {PUBLIC_DESTINATIONS} missing from {location}\n"
        else:  # the remainder of error cases needs to be handled server-side, so prep the upload
            headers = {"X-API-KEY": api_key}
            # Prepare to use a session
            req = requests.Request("POST", url=UPLOAD_ENDPOINT, headers=headers, json=summary_data)
            prepped = req.prepare()
            response = s.send(prepped)
            if not response.ok:
                upload_info["errors"] += f"{response.text}\n"
            else:
                upload_info["status"] = f"Success"
                upload_info["text"] = response.text
        pathlib.Path(location).unlink(missing_ok=True)
    return upload_info


if __name__ == "__main__":
    outputs = summarize_bayseflow_files(["../../tests/valid_file1.bf", "../../tests/valid_file2.bf",
                                        "../../tests/valid_file3.bf",
                                        "../../tests/invalid_file1.bf"], verbose=True)
    print(f"Saved files at {outputs}")
