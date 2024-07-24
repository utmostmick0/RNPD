import os
from IPython.display import clear_output
from subprocess import call, getoutput, run
import time
import sys
import fileinput
import ipywidgets as widgets
from torch.hub import download_url_to_file
from urllib.parse import urlparse, parse_qs, unquote
import re
import requests
import six

from urllib.request import urlopen, Request
import tempfile
from tqdm import tqdm 



def Deps(force_reinstall):

    if not force_reinstall and os.path.exists('/usr/local/lib/python3.9/dist-packages/safetensors'):
        ntbk()
        os.environ['TORCH_HOME'] = '/notebooks/cache/torch'
        os.environ['PYTHONWARNINGS'] = 'ignore'        
        print('[1;32mModules and notebooks updated, dependencies already installed')

    else:
        call("pip install --root-user-action=ignore --no-deps -q accelerate==0.12.0", shell=True, stdout=open('/dev/null', 'w'))
        if not os.path.exists('/usr/local/lib/python3.9/dist-packages/safetensors'):
            os.chdir('/usr/local/lib/python3.9/dist-packages')
            call("rm -r torch torch-1.12.1+cu116.dist-info torchaudio* torchvision* PIL Pillow* transformers* numpy* gdown*", shell=True, stdout=open('/dev/null', 'w'))
        ntbk()
        if not os.path.exists('/models'):
            call('mkdir /models', shell=True)
        if not os.path.exists('/notebooks/models'):
            call('ln -s /models /notebooks', shell=True)
        if os.path.exists('/deps'):
            call("rm -r /deps", shell=True)
        call('mkdir /deps', shell=True)
        if not os.path.exists('cache'):
            call('mkdir cache', shell=True)
        os.chdir('/deps')
        call('wget -q -i https://raw.githubusercontent.com/utmostmick0/fast-stable-diffusion/main/Dependencies/aptdeps.txt', shell=True)
        call('dpkg -i *.deb', shell=True, stdout=open('/dev/null', 'w'))
        depsinst("https://github.com/utmostmick0/sd_dependencies/blob/f2216938549c58f6d16363cdbe8650960839bc7e/rnpddeps-t2.tar.zst", "/deps/rnpggeps-t2.tar.zst")
        call('tar -C / --zstd -xf npggeps-t2.tar.zst', shell=True, stdout=open('/dev/null', 'w'))
        call("sed -i 's@~/.cache@/notebooks/cache@' /usr/local/lib/python3.9/dist-packages/transformers/utils/hub.py", shell=True)
        os.chdir('/notebooks')
        call("git clone --depth 1 -q --branch main https://github.com/utmostmick0/diffusers /diffusers", shell=True, stdout=open('/dev/null', 'w'), stderr=open('/dev/null', 'w'))
        os.environ['TORCH_HOME'] = '/notebooks/cache/torch'
        os.environ['PYTHONWARNINGS'] = 'ignore'
        call("sed -i 's@text = _formatwarnmsg(msg)@text =\"\"@g' /usr/lib/python3.9/warnings.py", shell=True)
        if not os.path.exists('/notebooks/diffusers'):
            call('ln -s /diffusers /notebooks', shell=True)
        call("rm -r /deps", shell=True)
        os.chdir('/notebooks')
        clear_output()

        done()



def depsinst(url, dst):
    file_size = None
    req = Request(url, headers={"User-Agent": "torch.hub"})
    u = urlopen(req)
    meta = u.info()
    if hasattr(meta, 'getheaders'):
        content_length = meta.getheaders("Content-Length")
    else:
        content_length = meta.get_all("Content-Length")
    if content_length is not None and len(content_length) > 0:
        file_size = int(content_length[0])

    with tqdm(total=file_size, disable=False, mininterval=0.5,
              bar_format='Installing dependencies |{bar:20}| {percentage:3.0f}%') as pbar:
        with open(dst, "wb") as f:
            while True:
                buffer = u.read(8192)
                if len(buffer) == 0:
                    break
                f.write(buffer)
                pbar.update(len(buffer))
            f.close()



def dwn(url, dst, msg):
    file_size = None
    req = Request(url, headers={"User-Agent": "torch.hub"})
    u = urlopen(req)
    meta = u.info()
    if hasattr(meta, 'getheaders'):
        content_length = meta.getheaders("Content-Length")
    else:
        content_length = meta.get_all("Content-Length")
    if content_length is not None and len(content_length) > 0:
        file_size = int(content_length[0])

    with tqdm(total=file_size, disable=False, mininterval=0.5,
              bar_format=msg+' |{bar:20}| {percentage:3.0f}%') as pbar:
        with open(dst, "wb") as f:
            while True:
                buffer = u.read(8192)
                if len(buffer) == 0:
                    break
                f.write(buffer)
                pbar.update(len(buffer))
            f.close()



def ntbk():

    os.chdir('/notebooks')
    if not os.path.exists('Latest_Notebooks'):
        call('mkdir Latest_Notebooks', shell=True)
    else:
        call('rm -r Latest_Notebooks', shell=True)
        call('mkdir Latest_Notebooks', shell=True)
    os.chdir('/notebooks/Latest_Notebooks')
    call('wget -q -i https://github.com/utmostmick0/RNPD/blob/da5c8d8f6d76cacf7c7293836ef6b0a32151aacf/Notebooks.txt', shell=True)
    call('rm Notebooks.txt', shell=True)
    os.chdir('/notebooks')



def repo():

    print('[1;32mInstalling/Updating the repo...')
    os.chdir('/notebooks')
    if not os.path.exists('/notebooks/sd/stablediffusiond'): #reset later
       call('wget -q -O sd_mrep.tar.zst https://github.com/utmostmick0/dependencies/blob/3d4911654a6939e676f4353806b16beeb08c89fd/sd_mrep.tar.zst', shell=True)
       call('tar --zstd -xf sd_mrep.tar.zst', shell=True)
       call('rm sd_mrep.tar.zst', shell=True)        

    os.chdir('/notebooks/sd')
    if not os.path.exists('stable-diffusion-webui'):
        call('git clone -q --depth 1 --branch master https://github.com/AUTOMATIC1111/stable-diffusion-webui', shell=True)

    os.chdir('/notebooks/sd/stable-diffusion-webui/')
    call('git reset --hard', shell=True, stdout=open('/dev/null', 'w'))
    print('[1;32m')
    call('git checkout master', shell=True, stdout=open('/dev/null', 'w'), stderr=open('/dev/null', 'w'))
    call('git pull', shell=True, stdout=open('/dev/null', 'w'))
    os.makedirs('/notebooks/sd/stable-diffusion-webui/repositories', exist_ok=True)
    call('git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui-assets /notebooks/sd/stable-diffusion-webui/repositories/stable-diffusion-webui-assets', shell=True, stdout=open('/dev/null', 'w'), stderr=open('/dev/null', 'w'))
    os.chdir('/notebooks')
    clear_output()
    done()





def mdls(Original_Model_Version, Path_to_MODEL, MODEL_LINK, Temporary_Storage):

    import gdown
   
    
    src=getsrc(MODEL_LINK)


    call('ln -s /datasets/stable-diffusion-classic/SDv1.5.ckpt /notebooks/sd/stable-diffusion-webui/models/Stable-diffusion', shell=True, stdout=open('/dev/null', 'w'), stderr=open('/dev/null', 'w'))
    call('ln -s /datasets/stable-diffusion-v2-1-base-diffusers/stable-diffusion-2-1-base/v2-1_512-nonema-pruned.safetensors /notebooks/sd/stable-diffusion-webui/models/Stable-diffusion', shell=True, stdout=open('/dev/null', 'w'), stderr=open('/dev/null', 'w'))
    call('ln -s /datasets/stable-diffusion-v2-1/stable-diffusion-2-1/v2-1_768-nonema-pruned.safetensors /notebooks/sd/stable-diffusion-webui/models/Stable-diffusion', shell=True, stdout=open('/dev/null', 'w'), stderr=open('/dev/null', 'w'))
    call('ln -s /datasets/stable-diffusion-xl/sd_xl_base_1.0.safetensors /notebooks/sd/stable-diffusion-webui/models/Stable-diffusion', shell=True, stdout=open('/dev/null', 'w'), stderr=open('/dev/null', 'w'))

    if Path_to_MODEL !='':
      if os.path.exists(str(Path_to_MODEL)):
        print('[1;32mUsing the custom model.')
        model=Path_to_MODEL
      else:
          print('[1;31mWrong path, check that the path to the model is correct')

    elif MODEL_LINK !="":
         
      if src=='civitai':
         modelname=get_name(MODEL_LINK, False)
         if Temporary_Storage:
            model=f'/models/{modelname}'
         else:
            model=f'/notebooks/sd/stable-diffusion-webui/models/Stable-diffusion/{modelname}'
         if not os.path.exists(model):
            dwn(MODEL_LINK, model, 'Downloading the custom model')
            clear_output()
         else:
            print('[1;33mModel already exists')
      elif src=='gdrive':
         modelname=get_name(MODEL_LINK, True)
         if Temporary_Storage:
            model=f'/models/{modelname}'
         else:
            model=f'/notebooks/sd/stable-diffusion-webui/models/Stable-diffusion/{modelname}'
         if not os.path.exists(model):
            gdown.download(url=MODEL_LINK, output=model, quiet=False, fuzzy=True)
            clear_output()
         else:
            print('[1;33mModel already exists')
      else:
         modelname=os.path.basename(MODEL_LINK)
         if Temporary_Storage:
            model=f'/models/{modelname}'
         else:
            model=f'/notebooks/sd/stable-diffusion-webui/models/Stable-diffusion/{modelname}'
         if not os.path.exists(model):
            gdown.download(url=MODEL_LINK, output=model, quiet=False, fuzzy=True)
            clear_output()
         else:
            print('[1;33mModel already exists')

      if os.path.exists(model) and os.path.getsize(model) > 1810671599:
        print('[1;32mModel downloaded, using the custom model.')
      else:
        call('rm '+model, shell=True, stdout=open('/dev/null', 'w'), stderr=open('/dev/null', 'w'))
        print('[1;31mWrong link, check that the link is valid')

    else:
        if Original_Model_Version == "v1.5":
           model="/notebooks/sd/stable-diffusion-webui/models/Stable-diffusion/SDv1.5.ckpt"
           print('[1;32mUsing the original V1.5 model')
        elif Original_Model_Version == "v2-512":
            model="/notebooks/sd/stable-diffusion-webui/models/Stable-diffusion/v2-1_512-nonema-pruned.safetensors"
            print('[1;32mUsing the original V2-512 model')
        elif Original_Model_Version == "v2-768":
           model="/notebooks/sd/stable-diffusion-webui/models/Stable-diffusion/v2-1_768-nonema-pruned.safetensors"
           print('[1;32mUsing the original V2-768 model')
        elif Original_Model_Version == "SDXL":
            model="/notebooks/sd/stable-diffusion-webui/models/Stable-diffusion/sd_xl_base_1.0.safetensors"
            print('[1;32mUsing the original SDXL model')
        else:
            model="/notebooks/sd/stable-diffusion-webui/models/Stable-diffusion"
            print('[1;31mWrong model version, try again')
    try:
        model
    except:
        model="/notebooks/sd/stable-diffusion-webui/models/Stable-diffusion"

    return model




def loradwn(LoRA_LINK):

    import gdown

    if LoRA_LINK=='':
        print('[1;33mNothing to do')
    else:
        os.makedirs('/notebooks/sd/stable-diffusion-webui/models/Lora', exist_ok=True)

        src=getsrc(LoRA_LINK)

        if src=='civitai':
            modelname=get_name(LoRA_LINK, False)
            loramodel=f'/notebooks/sd/stable-diffusion-webui/models/Lora/{modelname}'
            if not os.path.exists(loramodel):
              dwn(LoRA_LINK, loramodel, 'Downloading the LoRA model')
              clear_output()
            else:
              print('[1;33mModel already exists')
        elif src=='gdrive':
            modelname=get_name(LoRA_LINK, True)
            loramodel=f'/notebooks/sd/stable-diffusion-webui/models/Lora/{modelname}'
            if not os.path.exists(loramodel):
              gdown.download(url=LoRA_LINK, output=loramodel, quiet=False, fuzzy=True)
              clear_output()
            else:
              print('[1;33mModel already exists')
        else:
            modelname=os.path.basename(LoRA_LINK)
            loramodel=f'/notebooks/sd/stable-diffusion-webui/models/Lora/{modelname}'
            if not os.path.exists(loramodel):
              gdown.download(url=LoRA_LINK, output=loramodel, quiet=False, fuzzy=True)
              clear_output()
            else:
              print('[1;33mModel already exists')

        if os.path.exists(loramodel) :
          print('[1;32mLoRA downloaded')
        else:
          print('[1;31mWrong link, check that the link is valid')



def CN(ControlNet_Model, ControlNet_XL_Model):
    
    def download(url, model_dir):

        filename = os.path.basename(urlparse(url).path)
        pth = os.path.abspath(os.path.join(model_dir, filename))
        if not os.path.exists(pth):
            print('Downloading: '+os.path.basename(url))
            download_url_to_file(url, pth, hash_prefix=None, progress=True)
        else:
          print(f"[1;32mThe model {filename} already exists[0m")    

    wrngv1=False
    os.chdir('/notebooks/sd/stable-diffusion-webui/extensions')
    if not os.path.exists("sd-webui-controlnet"):
      call('git clone https://github.com/Mikubill/sd-webui-controlnet.git', shell=True)
      os.chdir('/notebooks')
    else:
      os.chdir('sd-webui-controlnet')
      call('git reset --hard', shell=True, stdout=open('/dev/null', 'w'), stderr=open('/dev/null', 'w'))
      call('git pull', shell=True, stdout=open('/dev/null', 'w'), stderr=open('/dev/null', 'w'))
      os.chdir('/notebooks')

    mdldir="/notebooks/sd/stable-diffusion-webui/extensions/sd-webui-controlnet/models"
    for filename in os.listdir(mdldir):
      if "_sd14v1" in filename:
        renamed = re.sub("_sd14v1", "-fp16", filename)
        os.rename(os.path.join(mdldir, filename), os.path.join(mdldir, renamed))

    call('wget -q -O CN_models.txt https://github.com/utmostmick0/fast-stable-duffusion/blob/0d7471937a131aa52e61992715c40ca56573cbd9/AUTOMATIC1111_files/CN_models.txt', shell=True)
    call('wget -q -O CN_models_XL.txt https://github.com/utmostmick0/fast-stable-duffusion/blob/0d7471937a131aa52e61992715c40ca56573cbd9/AUTOMATIC1111_files/CN_models_XL.txt', shell=True)
      
    with open("CN_models.txt", 'r') as f:
        mdllnk = f.read().splitlines()
    with open("CN_models_XL.txt", 'r') as d:
        mdllnk_XL = d.read().splitlines()
    call('rm CN_models.txt CN_models_XL.txt', shell=True)
    
    os.chdir('/notebooks')

    if ControlNet_Model == "All" or ControlNet_Model == "all" :     
      for lnk in mdllnk:
          download(lnk, mdldir)
      clear_output()

      
    elif ControlNet_Model == "15":
      mdllnk=list(filter(lambda x: 't2i' in x, mdllnk))
      for lnk in mdllnk:
          download(lnk, mdldir)
      clear_output()        


    elif ControlNet_Model.isdigit() and int(ControlNet_Model)-1<14 and int(ControlNet_Model)>0:
      download(mdllnk[int(ControlNet_Model)-1], mdldir)
      clear_output()
      
    elif ControlNet_Model == "none":
       pass
       clear_output()

    else:
      print('[1;31mWrong ControlNet V1 choice, try again')
      wrngv1=True


    if ControlNet_XL_Model == "All" or ControlNet_XL_Model == "all" :
      for lnk_XL in mdllnk_XL:
          download(lnk_XL, mdldir)
      if not wrngv1:
        clear_output()
      done()

    elif ControlNet_XL_Model.isdigit() and int(ControlNet_XL_Model)-1<5:
      download(mdllnk_XL[int(ControlNet_XL_Model)-1], mdldir)
      if not wrngv1:
        clear_output()
      done()
    
    elif ControlNet_XL_Model == "none":
       pass
       if not wrngv1:
        clear_output()
       done()       

    else:
      print('[1;31mWrong ControlNet XL choice, try again')



def sdui(User, Password, model):

    auth=f"--gradio-auth {User}:{Password}"
    if User =="" or Password=="":
      auth=""

    call('wget -q -O /notebooks/sd/stable-diffusion-webui/modules/styles.py https://github.com/utmostmick0/fast-stable-diffusion/raw/main/AUTOMATIC1111_files/styles.py', shell=True)
    call('wget -q -O /usr/local/lib/python3.9/dist-packages/gradio/blocks.py https://raw.githubusercontent.com/utmostmick0/fast-stable-diffusion/main/AUTOMATIC1111_files/blocks.py', shell=True)
    
    localurl="tensorboard-"+os.environ.get('RNPD_FQDN')
    
    for line in fileinput.input('/usr/local/lib/python3.9/dist-packages/gradio/blocks.py', inplace=True):
      if line.strip().startswith('self.server_name ='):
          line = f'            self.server_name = "{localurl}"\n'
      if line.strip().startswith('self.protocol = "https"'):
          line = '            self.protocol = "https"\n'
      if line.strip().startswith('if self.local_url.startswith("https") or self.is_colab'):
          line = ''
      if line.strip().startswith('else "http"'):
          line = ''
      sys.stdout.write(line)

     
    os.chdir('/notebooks/sd/stable-diffusion-webui/modules')
    
    call("sed -i 's@possible_sd_paths =.*@possible_sd_paths = [\"/notebooks/sd/stablediffusion\"]@' /notebooks/sd/stable-diffusion-webui/modules/paths.py", shell=True)
    call("sed -i 's@\.\.\/@src/@g' /notebooks/sd/stable-diffusion-webui/modules/paths.py", shell=True)
    call("sed -i 's@src\/generative-models@generative-models@g' /notebooks/sd/stable-diffusion-webui/modules/paths.py", shell=True)
    
    call("sed -i 's@-> Network | None@@g' /notebooks/sd/stable-diffusion-webui/extensions-builtin/Lora/network.py", shell=True)
    call("sed -i 's@|@or@' /notebooks/sd/stable-diffusion-webui/extensions/adetailer/aaaaaa/helper.py", shell=True, stdout=open('/dev/null', 'w'), stderr=open('/dev/null', 'w'))
    
    call("sed -i 's@\"quicksettings\": OptionInfo(.*@\"quicksettings\": OptionInfo(\"sd_model_checkpoint,  sd_vae, CLIP_stop_at_last_layers, inpainting_mask_weight, initial_noise_multiplier\", \"Quicksettings list\"),@' /notebooks/sd/stable-diffusion-webui/modules/shared.py", shell=True)
    os.chdir('/notebooks/sd/stable-diffusion-webui')
    clear_output()


    if model=="":
        mdlpth=""
    else:
        if os.path.isfile(model):
            mdlpth="--ckpt "+model
        else:
            mdlpth="--ckpt-dir "+model


    configf="--disable-console-progressbars --no-gradio-queue --no-hashing --no-half-vae --disable-safe-unpickle --api --no-download-sd-model --xformers --enable-insecure-extension-access --port 6006 --listen --skip-version-check --ckpt-dir /models "+auth+" "+mdlpth

    return configf    
    
    

def getsrc(url):
    parsed_url = urlparse(url)
    if parsed_url.netloc == 'civitai.com':
        src='civitai'
    elif parsed_url.netloc == 'drive.google.com':
        src='gdrive'
    elif parsed_url.netloc == 'huggingface.co':
        src='huggingface'
    else:
        src='others'
    return src



def get_name(url, gdrive):

    from gdown.download import get_url_from_gdrive_confirmation

    if not gdrive:
        response = requests.get(url, allow_redirects=False)
        if "Location" in response.headers:
            redirected_url = response.headers["Location"]
            quer = parse_qs(urlparse(redirected_url).query)
            if "response-content-disposition" in quer:
                disp_val = quer["response-content-disposition"][0].split(";")
                for vals in disp_val:
                    if vals.strip().startswith("filename="):
                        filenm=unquote(vals.split("=", 1)[1].strip())
                        return filenm.replace("\"","")
    else:
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}
        lnk="https://drive.google.com/uc?id={id}&export=download".format(id=url[url.find("/d/")+3:url.find("/view")])
        res = requests.session().get(lnk, headers=headers, stream=True, verify=True)
        res = requests.session().get(get_url_from_gdrive_confirmation(res.text), headers=headers, stream=True, verify=True)
        content_disposition = six.moves.urllib_parse.unquote(res.headers["Content-Disposition"])
        filenm = re.search(r"filename\*=UTF-8''(.*)", content_disposition).groups()[0].replace(os.path.sep, "_")
        return filenm
    
    
    
def done():
    done = widgets.Button(
        description='Done!',
        disabled=True,
        button_style='success',
        tooltip='',
        icon='check'
    )
    display(done)
