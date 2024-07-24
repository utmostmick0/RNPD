import os
import subprocess
from urllib.request import urlopen, Request
import gdown
from urllib.parse import urlparse
from tqdm import tqdm

def install_dependencies():
    deps = [
        "accelerate==0.12.0",
        # add more dependencies here if needed
    ]
    for dep in deps:
        subprocess.call(f"pip install --root-user-action=ignore --no-deps -q {dep}", shell=True)

def setup_workspace():
    if not os.path.exists('/models'):
        os.makedirs('/models')
    if not os.path.exists('/workspace/models'):
        os.symlink('/models', '/workspace/models')
    if not os.path.exists('/deps'):
        os.makedirs('/deps')
    if not os.path.exists('cache'):
        os.makedirs('cache')

def ntbk():
    workspace_dir = '/workspace'
    os.chdir(workspace_dir)
    if not os.path.exists('Latest_Notebooks'):
        os.makedirs('Latest_Notebooks')
    os.chdir('Latest_Notebooks')
    subprocess.call('wget -q -i https://github.com/utmostmick0/RNPD/raw/main/Notebooks.txt', shell=True)
    subprocess.call('rm Notebooks.txt', shell=True)
    os.chdir(workspace_dir)

def repo():
    print('Installing/Updating the repo...')
    workspace_dir = '/workspace'
    os.chdir(workspace_dir)
    if not os.path.exists('sd'):
        os.makedirs('sd')
    os.chdir('sd')

    if not os.path.exists('stablediffusiond'):
        subprocess.call('wget -q -O npddeps-t2.tar.zst https://github.com/utmostmick0/sd_dependencies/raw/main/r', shell=True)
        # Use tar -xf to handle various formats
        subprocess.call('tar -xf sd_mrep.tar.zst', shell=True)
        subprocess.call('rm sd_mrep.tar.zst', shell=True)

    if not os.path.exists('stable-diffusion-webui'):
        subprocess.call('git clone -q --depth 1 --branch master https://github.com/AUTOMATIC1111/stable-diffusion-webui', shell=True)

    os.chdir('stable-diffusion-webui')
    subprocess.call('git reset --hard', shell=True, stdout=open(os.devnull, 'w'))
    subprocess.call('git checkout master', shell=True, stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w'))
    subprocess.call('git pull', shell=True, stdout=open(os.devnull, 'w'))

    if not os.path.exists('repositories'):
        os.makedirs('repositories')
    os.chdir('repositories')
    subprocess.call('git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui-assets stable-diffusion-webui-assets', shell=True, stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w'))

    os.chdir(workspace_dir)
    print("Repository setup completed.")

def download_file(url, dst, msg):
    req = Request(url, headers={"User-Agent": "torch.hub"})
    with urlopen(req) as u, open(dst, 'wb') as f, tqdm(
        total=int(u.info().get("Content-Length")), unit='B', unit_scale=True, desc=msg
    ) as pbar:
        while True:
            chunk = u.read(8192)
            if not chunk:
                break
            f.write(chunk)
            pbar.update(len(chunk))

def setup_models(Original_Model_Version, Path_to_MODEL, MODEL_LINK, Temporary_Storage):
    model = ""
    if Path_to_MODEL and os.path.exists(Path_to_MODEL):
        model = Path_to_MODEL
    elif MODEL_LINK:
        modelname = os.path.basename(urlparse(MODEL_LINK).path)
        if Temporary_Storage:
            model = f'/models/{modelname}'
        else:
            model = f'/workspace/sd/stable-diffusion-webui/models/Stable-diffusion/{modelname}'
        if not os.path.exists(model):
            gdown.download(url=MODEL_LINK, output=model, quiet=False, fuzzy=True)
    else:
        models = {
            "v1.5": "/workspace/sd/stable-diffusion-webui/models/Stable-diffusion/SDv1.5.ckpt",
            "v2-512": "/workspace/sd/stable-diffusion-webui/models/Stable-diffusion/v2-1_512-nonema-pruned.safetensors",
            "v2-768": "/workspace/sd/stable-diffusion-webui/models/Stable-diffusion/v2-1_768-nonema-pruned.safetensors",
            "SDXL": "/workspace/sd/stable-diffusion-webui/models/Stable-diffusion/sd_xl_base_1.0.safetensors"
        }
        model = models.get(Original_Model_Version, "")
    return model

def done():
    print("Setup is complete.")

def main():
    force_reinstall = False  # set based on your requirements
    if not force_reinstall and os.path.exists('/usr/local/lib/python3.9/dist-packages/safetensors'):
        ntbk()
        os.environ['TORCH_HOME'] = '/workspace/cache/torch'
        os.environ['PYTHONWARNINGS'] = 'ignore'
        print('Modules and workspace updated, dependencies already installed')
    else:
        install_dependencies()
        setup_workspace()
        ntbk()
        repo()

    done()

if __name__ == "__main__":
    main()
