def _wget(url, output_dir):
    import sys
    import os
    import shutil
    try:
        from urllib.request import urlopen  # Python 3
    except ImportError:
        from urllib2 import urlopen  # Python 2

    basename = os.path.basename(url)
    output_file = os.path.join(output_dir, basename)
    response = urlopen(url)
    length = 16*1024
    with open(output_file, 'wb') as fh:
        shutil.copyfileobj(response, fh, length)

def _upgrade_1_to_2(model):
    # Convert from schema version 1 to 2
    new_model = {}
    # Optional
    if "reference" in model:
        new_model["reference"] = model["reference"]
    new_model["potential"] = []
    for potential in model["potential"]:
        new_potential = {}
        new_potential["type"] = potential["type"]
        new_potential["parameters"] = {}
        db = {}
        for key in potential["parameters"]:
            db[key] = {}
            nsp = len(potential["parameters"][key])
            for i in range(nsp):
                for j in range(nsp):
                    if j<i: continue
                    pair = f'{i+1}-{j+1}'
                    db[key][pair] = potential["parameters"][key][i][j]
        last_key = key
        for pair in db[last_key].keys():
            new_potential["parameters"][pair] = {key:db[key][pair] for key in db.keys()}
        new_model["potential"].append(new_potential)

    new_cutoffs = []
    for cutoff in model["cutoff"]:
        new_cutoff = {}
        new_cutoff["type"] = cutoff["type"]
        new_cutoff["parameters"] = {}
        db = {}
        for key in cutoff["parameters"]:
            db[key] = {}
            nsp = len(cutoff["parameters"][key])
            for i in range(nsp):
                for j in range(nsp):
                    if j<i: continue
                    pair = f'{i+1}-{j+1}'
                    db[key][pair] = cutoff["parameters"][key][i][j]
        last_key = key
        for pair in db[last_key].keys():
            new_cutoff["parameters"][pair] = {key:db[key][pair] for key in db.keys()}
        new_cutoffs.append(new_cutoff)
    for i, new_cutoff in enumerate(new_cutoffs):
        new_model["potential"][i]["cutoff"] = new_cutoff
    return new_model
