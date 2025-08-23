import os
import re
import xml.etree.ElementTree as ET
from typing import List, Tuple, Union
from pathlib import Path
def parse_available_resources(xml_path: Path):
    available_resources = {}
    tree = ET.parse(xml_path)
    root = tree.getroot()

    x = root.find('AreaEstimates')
    x = x.find('AvailableResources')
    available_resources['FF'] =int(x.find('FF').text)
    available_resources['DSP'] = int(x.find('DSP').text)
    available_resources['LUT'] = int(x.find('LUT').text)
    available_resources['BRAM'] = int(x.find('BRAM_18K').text)
    return available_resources

def parse_hls_utilization_xml(xml_path: Path):
    if os.path.exists(xml_path):
        tree = ET.parse(xml_path)
        root = tree.getroot()
        x = root.find('AreaEstimates').find('Resources')
        ff = int(x.find('FF').text)
        dsp = int(x.find('DSP').text)
        lut = int(x.find('LUT').text)
        bram = int(x.find('BRAM_18K').text)

    else:
        raise Exception(f"****Error in synthesis - NO Synthesis Results in {xml_path}****")
    return lut, bram, ff, dsp
    
def parse_utilization_rpt_xml(rpt_path: Path):
    tree = ET.parse(rpt_path)
    root = tree.getroot()

    lut = root.find('AreaReport/Resources/LUT').text
    bram = root.find('AreaReport/Resources/BRAM').text
    ff = root.find('AreaReport/Resources/FF').text
    dsp = root.find('AreaReport/Resources/DSP').text
    clb = root.find('AreaReport/Resources/CLB').text
    latch = root.find('AreaReport/Resources/LATCH').text

    return {'LUT': int(lut), 'FF': int(ff), 'DSP': int(dsp), 'BRAM': int(bram)}

def _find_line_containing(lines: List[str], *keywords) -> int:
    for i, line in enumerate(lines):
        if all(s in line for s in keywords):
            return i
    return -1
def parse_timing_rpt_xml(rpt_path: Path):
    tree = ET.parse(rpt_path)
    root = tree.getroot()

    wns = root.find('TimingReport/WNS_FINAL').text
    tns = root.find('TimingReport/TNS_FINAL').text
    target_clk = root.find('TimingReport/TargetClockPeriod').text
    achieved_clk = root.find('TimingReport/AchievedClockPeriod').text

    return wns, tns, target_clk, achieved_clk

def parse_utilization_rpt_txt(rpt_path: Path):
    integer_pattern = '-?\d+'
    rx = re.compile(integer_pattern, re.VERBOSE)
    
    lut = bram = ff = dsp = -1
        
    with open(rpt_path, "r") as rpt:
        lines = rpt.readlines()

    lut_line = _find_line_containing(lines, 'CLB LUTs')
    ff_line = _find_line_containing(lines, 'Register as Flip Flop')
    dsp_line = _find_line_containing(lines, 'DSPs')
    bram_line = _find_line_containing(lines, 'Block RAM Tile')

    if lut_line != -1:
        lut = int((rx.findall(lines[lut_line]))[0])
    if ff_line != -1:
        ff = int((rx.findall(lines[ff_line]))[0])
    if dsp_line != -1:
        dsp = int((rx.findall(lines[dsp_line]))[0])
    if bram_line != -1:
        bram = int((rx.findall(lines[bram_line]))[0])
        
    return {'LUT': int(lut), 'FF': int(ff), 'DSP': int(dsp), 'BRAM': int(bram)}

def parse_export_impl_rpt(rpt_path: Path):
    numeric_const_pattern = r'-?\d+'
    rx = re.compile(numeric_const_pattern, re.VERBOSE)

    lut = bram = ff = dsp  = -1
        
    with open(rpt_path, "r") as rpt:
        lines = rpt.readlines()

    for line in lines:
        if line.find('BRAM:') != -1 and bram == -1:
            bram = int((rx.findall(line))[0])
        elif line.find('DSP:') != -1 and dsp == -1:
            dsp = int((rx.findall(line))[0])
        elif line.find('LUT:') != -1 and lut == -1:
            lut = int((rx.findall(line))[0])
        elif line.find('FF:') != -1 and ff == -1:
            ff = int((rx.findall(line))[0])
        
        if lut != -1 and bram != -1 and ff != -1 and dsp != -1:
            break

    return {'LUT': int(lut), 'FF': int(ff), 'DSP': int(dsp), 'BRAM': int(bram)}

def parse_timing_rpt_txt(rpt_path: Path):
    numeric_const_pattern = r'-?[0-9]\d*(\.\d+)?'
    rx = re.compile(numeric_const_pattern, re.VERBOSE)

    wns = tns = achieved_clk = -1.0
    target_clk = 8.0

    with open(rpt_path, "r") as rpt:
        lines = rpt.readlines()

    n_lines = len(lines)
    i = 0
    while i < n_lines and \
        (wns == -1.0 or tns == -1.0 or achieved_clk == -1.0):
        line = lines[i]
        if line.find('WNS(ns)') != -1 and line.find('TNS(ns)') != -1:
            line = lines[i+2]
            wns = float((rx.findall(line))[0])
            tns = float((rx.findall(line))[1])
            achieved_clk = target_clk - wns
            break
        i += 1

    return wns, tns, target_clk, achieved_clk


def extract_timing_summary(
    solution_path: Union[Path, str], 
    filtered: bool = False
) -> Tuple[float, float, float, float]:
    if filtered:
        path = f'{solution_path}/reports/'
    else:
        path = f'{solution_path}/impl/report/verilog/'

    rpt_path = Path(f'{path}export_impl.xml')
    if rpt_path.is_file() == False:
        rpt_path = Path(f'{path}impl_timing_summary.rpt')
        if rpt_path.is_file() == False:
            return -1.0, -1.0, -1.0, -1.0
        
        wns, tns, target_clk, achieved_clk = parse_timing_rpt_txt(rpt_path)
    else:
        wns, tns, target_clk, achieved_clk = parse_timing_rpt_xml(rpt_path)

    {
        "wns": float(wns),
        "tns": float(tns),
        "target_clk": float(target_clk),
        "achieved_clk": float(achieved_clk),
    }

def extract_impl_utilization(
    solution_path: Union[Path, str], 
    filtered: bool = False,
    top_function: str = None,
) -> Tuple[int, int, int, int, int, int]:
    if filtered:
        path = f'{solution_path}/reports/'
    else:
        path = f'{solution_path}/impl/report/verilog/'

    lut = bram = ff = dsp = clb = latch = -1
    rpt_path = Path(f'{path}export_impl.xml')
    if rpt_path.is_file() == False:
        rpt_path = Path(f'{path}export_impl.rpt')
        if rpt_path.is_file():
            return parse_export_impl_rpt(rpt_path)
        if top_function:
            rpt_path = Path(f'{path}{top_function}_export.rpt')
            if rpt_path.is_file():
                return parse_export_impl_rpt(rpt_path)
        rpt_path = Path(path + 'impl_utilization_placed.rpt')
        if rpt_path.is_file():
            return parse_utilization_rpt_txt(rpt_path)
    else:
        return parse_utilization_rpt_xml(rpt_path)
    return {
        "LUT": int(lut),
        "BRAM": int(bram),
        "FF": int(ff),
        "DSP": int(dsp),
        #"CLB": int(clb),
        #"latch": int(latch),
    }


def extract_hls_utilization(
    solution_path: Union[Path, str], 
    filtered: bool = False,
) -> Tuple[int, int, int, int, int, int]:

    if filtered:
        path = f'{solution_path}/reports/'
    else:
        path = f'{solution_path}/syn/report/'

    rpt_path = Path(f'{path}csynth.xml')
    if rpt_path.is_file() == False:
        lut = bram = ff = dsp = -1  
    else:
        lut, bram, ff, dsp = parse_hls_utilization_xml(rpt_path)

    return {
        "LUT": int(lut),
        "BRAM": int(bram),
        "FF": int(ff),
        "DSP": int(dsp),
    }

def extract_hls_cc_report(
    solution_path: Union[Path, str],
    filtered: bool = False
) -> int:
    if filtered:
        rpt_path = f'{solution_path}/reports/csynth.xml'
    else:
        rpt_path = f'{solution_path}/syn/report/csynth.xml'

    if Path(rpt_path).is_file() == False:
        return -1

    tree = ET.parse(rpt_path)
    root = tree.getroot()

    cc = root.find(
        'PerformanceEstimates/SummaryOfOverallLatency/Average-caseLatency'
    ).text

    return int(cc)

def compute_snru(results, vitis_solution_path, filtered: bool = False):
    """
    Returns the Sum of Normalized Resource Use of a solution, based on the results and the values of resources.
    Note that its basically a snru, but we multiply the resources by the most abundant resource
    """
    available_resources= get_available_resources(vitis_solution_path,filtered)
    most_abundant_resource = max(available_resources, key=available_resources.get)
    resources = 0
    for resource in available_resources:
        resources += results[resource] * (available_resources[most_abundant_resource] / available_resources[resource])
    return resources
def get_available_resources(
    solution_path: Union[Path, str],
    filtered: bool = False
):
    if filtered:
        rpt_path = f'{solution_path}/reports/csynth.xml'
    else:
        rpt_path = f'{solution_path}/syn/report/csynth.xml'
    return parse_available_resources(rpt_path)
